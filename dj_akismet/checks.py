class AkismetCheck(object):
    """ Base class for spam checks. Subclass this to create spam checks for
        your models.
    """
    #: Should the object be saved after the check is complete?
    should_save = True
    #: Should the comment be automatically checked on init?
    auto_check = True
    #: Should mark_as_spam|ham be added to this model's admin page?
    patch_admin = True

    def __init__(self, object):
        self.object = object

    def get_data(self):
        """ Returns the data dict that will be sent to Akismet. See:
            http://www.voidspace.org.uk/python/akismet_python.html#comment-check
        """
        raise NotImplemented()

    def get_content(self):
        """ Returns the content of the comment.
        """
        raise NotImplemented()

    def is_spam(self):
        """ Called when a comment is spam.
        """
        pass
    
    def is_ham(self):
        """ Called when a comment is ham.
        """
        pass
