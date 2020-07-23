from django.apps import AppConfig


class ecommerceConfig(AppConfig):
    name = 'ecom'

    def ready(self):
    	import ecom.signals