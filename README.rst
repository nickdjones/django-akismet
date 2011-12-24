django-akismet
==============

django-akismet lets you use Akismet's spam checks without requiring any
modification to your models. It provides a signal receiver which will
check comments as they are created, although you can also check comments
with a management command or Celery task.

By default it will update the admin interface for your comment model to add
'mark as spam' and 'mark as ham' actions, which are used to train Akismet on
existing messages.

Example::

    # models.py
    class MyComment(models.Model):
        comment = models.CharField(.....)
        user = models.ForeignKey(User)
    
    # someapp/spam_checks.py
    from dj_akismet import spam_checks
    from dj_akismet.utils import do_spam_check
    
    class MyCommentCheck(AkismetCheck):
    
        def get_data(self):
            return {'comment_author': self.object.author.username,
                    'comment_author_email': self.object.author.email,
                    ...
                    }
    
        def get_content(self):
            return self.object.comment

        def is_spam(self):
            self.object.delete()

        def is_ham(self):
            self.object.publish()
    spam_checks.register(MyCommentCheck, model=MyComment)
    
    # Set up a signal to check for spam when comments are posted (optional)
    post_save.connect(spam_check, 
                      sender=MyComment,
                      dispatch_uid='do_spam_check')
    
    # settings.py
    # List of modules to search for AkismetCheck subclasses
    AKISMET_CHECK_SOURCES = (
        'someapp.spam_checks',
    )
    AKISMET_API_KEY = 'your key'
    AKISMET_DOMAIN = 'your domain'


TODO
----

* Management command to check multiple items from command line
* Fix admin interface for AkismetCheckItems
