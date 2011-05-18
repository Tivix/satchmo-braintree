from xml.dom import minidom
import random
import urllib2
from datetime import datetime
from decimal import Decimal

from django.conf import settings as django_settings
from django.template import loader, Context
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from braintree import Configuration, Environment, Transaction

from payment.modules.base import BasePaymentProcessor, ProcessorResult
from satchmo_store.shop.models import Config
from satchmo_utils.numbers import trunc_decimal
from tax.utils import get_tax_processor
from livesettings import config_get_group


class PaymentProcessor(BasePaymentProcessor):
    """
    Braintree payment processing module ( http://www.braintreepaymentsolutions.com/ )
    You must have an account with Braintree in order to use this module.
    """
    def __init__(self, settings):
        super(PaymentProcessor, self).__init__('satchmo_braintree', settings)
    
    def can_authorize(self):
        return False    # disabled for now
    
    def can_recur_bill(self):
        return False    # disabled. Recurring should be handled by the app using the Vault, and not be left to Braintree.
    
    def capture_payment(self, testing=False, order=None, amount=None):
        """Process payments without an authorization step."""
        braintree_settings = config_get_group('PAYMENT_SATCHMO_BRAINTREE')
        
        # Configure Braintree
        Configuration.configure(
            Environment.Production if django_settings.IS_PROD else Environment.Sandbox,
            braintree_settings.MERCHANT_ID.value,
            braintree_settings.PUBLIC_KEY.value,
            braintree_settings.PRIVATE_KEY.value
        )
        
        if order:
            self.prepare_data(order)
        else:
            order = self.order
        
        if order.paid_in_full:
            self.log_extra('%s is paid in full, no capture attempted.', order)
            results = ProcessorResult(self.key, True, _("No charge needed, paid in full."))
            self.record_payment()
        else:
            self.log_extra('Capturing payment for %s', order)
            amount = order.balance
            
            result = Transaction.sale({
                "amount": amount,
                # "order_id": "123",
                "credit_card": {
                    "number": order.credit_card.decryptedCC,
                    "expiration_date": order.credit_card.expirationDate,    # 05/2012 ?
                    "cvv": order.credit_card.ccv
                },
                "customer": {
                    "first_name": order.contact.first_name,
                    "last_name": order.contact.last_name,
                },
                "billing": {
                    "first_name": order.contact.first_name,
                    "last_name": order.contact.last_name,
                    "street_address": order.full_bill_street,
                    "locality": order.bill_city,
                    "region": order.bill_state,
                    "postal_code": order.bill_postal_code,
                },
                "options": {
                    "submit_for_settlement": True
                }
            })
            
            if result.is_success:
                payment = self.record_authorization(order=order, amount=amount, transaction_id=result.transaction.id)
                response_text = 'Success'
            else:
                response_text = 'Fail'
                payment = self.record_failure(amount=amount)
            
            return ProcessorResult(self.key, result.is_success, response_text, payment=payment)
            # standard = self.get_standard_charge_data(amount=amount)
            # results = self.send_post(standard, testing)
        
        return results

if __name__ == "__main__":
    """
    This is for testing - enabling you to run from the command line and make
    sure everything is ok
    """
    import os
    
    # Set up some dummy classes to mimic classes being passed through Satchmo
    class testContact(object):
        pass
    class testCC(object):
        pass
    class testOrder(object):
        def __init__(self):
            self.contact = testContact()
            self.credit_card = testCC()
        def order_success(self):
            pass

    if not os.environ.has_key("DJANGO_SETTINGS_MODULE"):
        os.environ["DJANGO_SETTINGS_MODULE"]="satchmo_store.settings"

    settings_module = os.environ['DJANGO_SETTINGS_MODULE']
    settingsl = settings_module.split('.')
    settings = __import__(settings_module, {}, {}, settingsl[-1])

    sampleOrder = testOrder()
    sampleOrder.contact.first_name = 'Chris'
    sampleOrder.contact.last_name = 'Smith'
    sampleOrder.contact.primary_phone = '801-555-9242'
    sampleOrder.full_bill_street = '123 Main Street'
    sampleOrder.bill_postal_code = '12345'
    sampleOrder.bill_state = 'TN'
    sampleOrder.bill_city = 'Some City'
    sampleOrder.bill_country = 'US'
    sampleOrder.total = "27.01"
    sampleOrder.balance = "27.01"
    sampleOrder.credit_card.decryptedCC = '6011000000000012'
    sampleOrder.credit_card.expirationDate = "10/11"
    sampleOrder.credit_card.ccv = "144"

    authorize_settings = config_get_group('PAYMENT_SATCHMO_BRAINTREE')
    if authorize_settings.LIVE.value:
        print "Warning.  You are submitting a live order.  AUTHORIZE.NET system is set LIVE."

    processor = PaymentProcessor(authorize_settings)
    processor.prepare_data(sampleOrder)
    results = processor.process(testing=True)
    print results
