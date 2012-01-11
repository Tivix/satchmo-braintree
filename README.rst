

=================
satchmo-braintree
=================

Satchmo is a pretty solid open-source application for building Django powered eCommerce applications. It comes out of the box with support for Authorize.net.

Braintree Payment Solutions ( http://www.braintreepaymentsolutions.com/ ) is an alternative to it, and has amazing customer service, online interface and most importantly a very solid (and well documented) API. Braintree also has a well maintained Python wrapper ( https://github.com/braintree/braintree_python ) which makes it a breeze to integrate with it.


Installation
------------

- Install satchmo_braintree (ideally in your virtualenv!) using pip or simply getting a copy of the code and putting it in a directory in your codebase.

- Add ``satchmo_braintree`` to your Django settings ``INSTALLED_APPS``::
	
	INSTALLED_APPS = [
        # ...
        "satchmo_braintree",
    ]

- You can edit the Merchant ID, Public/Private key values from Braintree within the Satchmo settings screen at http://your-site.com/settings/


This opensource app is brought to you by Tivix, Inc. ( http://tivix.com/ )


========
Versions
========

0.1 - First merge

0.2 - Configuration group naming fixes + others (in urls.py for example) that use "satchmo_braintree" everywhere rather than just "braintree"
