from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from dj_akismet.registry import spam_checks
import akismet


try:
    API_KEY = getattr(settings, 'AKISMET_API_KEY')
    DOMAIN = getattr(settings, 'AKISMET_DOMAIN')
except AttributeError:
    msg = 'You need to set AKISMET_API_KEY and AKISMET_DOMAIN in settings.py'
    raise ImproperlyConfigured(msg)

# Setup the Akismet api and verify the key
# should this happen here? or when the first item is checked?
api = akismet.Akismet(API_KEY, DOMAIN)
if not api.verify_key():
    raise akismet.APIKeyError('Invalid AKIMET_API_KEY')

class AkismetCheckItem(models.Model):
    """ This model is used to call the Akismet API. Saving is optional.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_obj = generic.GenericForeignKey('content_type', 'object_id')
    #timestamp = models.DateTimeField(auto_now=True)
    spam = models.NullBooleanField()

    def __init__(self, auto_check=None, should_save=None, *args, **kwargs):
        super(AkismetCheckItem, self).__init__(*args, **kwargs)

        if not self.content_obj:
            # If a content_obj has not been set, we are probably being loaded
            # via the admin interface
            return

        # look up the AkismetCheck subclass for this model
        self.check_cls = spam_checks.get_instance(self.content_obj)

        # Get some settings from init args, or use the check_cls settings
        # Ternary operators: ugly, but useful.
        self.auto_check = self.check_cls.auto_check if auto_check is None else auto_check
        self.should_save = self.check_cls.should_save if should_save is None else should_save

        # look up the model type and set content type/obj
        self.content_type = ContentType.objects.get_for_model(self.content_obj)
        self.object_id = self.content_obj.id

        if self.auto_check:
            self.check()

    def check(self):
        """ Checks the comment by submitting it to Akismet.
        """
        self.spam = api.comment_check(self.check_cls.get_content(), 
                                      data=self.check_cls.get_data())

        if self.should_save:
            self.save()

        if self.spam:
            self.check_cls.is_spam()
        else:
            self.check_cls.is_ham()

        return self.spam

    def mark_as_spam(self):
        """ Submits a comment as spam to train Akismet.
        """
        api.submit_spam(self.check_cls.get_content(),
                        data=self.check_cls.get_data())

    def mark_as_ham(self):
        """ Submits a comment as ham to train Akismet.
        """
        api.submit_ham(self.check_cls.get_content(),
                        data=self.check_cls.get_data())
