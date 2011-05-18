from livesettings import *
from django.utils.translation import ugettext_lazy as _


# this is so that the translation utility will pick up the string
gettext = lambda s: s
_strings = (gettext('CreditCard'), gettext('Credit Card'))

PAYMENT_GROUP = ConfigurationGroup('PAYMENT_SATCHMO_BRAINTREE',
    _('Braintree Payment Settings'),
    ordering=102)

config_register_list(
    BooleanValue(PAYMENT_GROUP,
        'LIVE',
        description=_("Accept real payments"),
        help_text=_("False if you want to submit to the test urls.  NOTE: If you are testing, then you can use the cc# 4222222222222 to force a bad credit card response.  If you use that number and a ccv of 222, that will force a bad ccv response from authorize.net"),
        default=False),

    ModuleValue(PAYMENT_GROUP,
        'MODULE',
        description=_('Implementation module'),
        hidden=True,
        default = 'satchmo_braintree'),

    StringValue(PAYMENT_GROUP,
        'KEY',
        description=_("Module key"),
        hidden=True,
        default = 'SATCHMO_BRAINTREE'),

    StringValue(PAYMENT_GROUP,
        'LABEL',
        description=_('English name for this group on the checkout screens'),
        default = 'Credit Cards',
        help_text = _('This will be passed to the translation utility')),

    StringValue(PAYMENT_GROUP,
        'URL_BASE',
        description=_('The url base used for constructing urlpatterns which will use this module'),
        default = r'^credit/'),

    MultipleStringValue(PAYMENT_GROUP,
        'CREDITCHOICES',
        description=_('Available credit cards'),
        choices = (
            (('American Express', 'American Express')),
            (('Visa','Visa')),
            (('Mastercard','Mastercard')),
            (('Discover','Discover'))),
        default = ('Visa', 'Mastercard', 'Discover')),

    StringValue(PAYMENT_GROUP,
        'MERCHANT_ID',
        description=_('Your Braintree Merchant ID'),
        default=""),
    
    StringValue(PAYMENT_GROUP,
        'PUBLIC_KEY',
        description=_('Your Braintree Public Key'),
        default=""),

    StringValue(PAYMENT_GROUP,
        'PRIVATE_KEY',
        description=_('Your Braintree Private Key'),
        default=""),

    BooleanValue(PAYMENT_GROUP,
        'CAPTURE',
        description=_('Capture Payment immediately?'),
        default=True,
        help_text=_('IMPORTANT: If false, a capture attempt will be made when the order is marked as shipped."')),

    BooleanValue(PAYMENT_GROUP,
        'EXTRA_LOGGING',
        description=_("Verbose logs"),
        help_text=_("Add extensive logs during post."),
        default=False)
)
