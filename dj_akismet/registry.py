from django.contrib import admin

class SpamCheckItems(object):
    """ A simple registry, based on Django's admin.site.
    """
    def __init__(self):
        self._registry = {}

    def register(self, model, check_cls):
        """ Registers the model/check_cls, and modifies the model's Django
            admin page.
        """
        if model in self._registry:
            # raise error here, or just ignore?
            return
        self.model = model
        # Add the model/check_cls to the registry
        self._registry[model] = check_cls

        # Patch the Django admin for this model, if necessary
        if check_cls.patch_admin:
            admin.autodiscover() # is doing this here correct?
            if model in admin.site._registry:
                self.patch_admin()

    def patch_admin(self):
        """ Adds 'mark as spam|ham' options to the model's admin page.
        """
        # Import utils here to prevent circular imports
        from dj_akismet import utils
        admin_cls = admin.site._registry[self.model]
        admin_cls.actions.append(utils.mark_as_spam)
        admin_cls.actions.append(utils.mark_as_ham)
        admin.site._registry[self.model] = admin_cls

    def get_instance(self, model):
        """ Returns an instance of the AkismetCheck subclass for the given
            model.
        """
        cls = self._registry.get(model.__class__)
        return cls(model)

spam_checks = SpamCheckItems()
