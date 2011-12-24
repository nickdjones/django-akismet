from django.db.models.signals import post_save
from dj_akismet.checks import AkismetCheck
from dj_akismet.registry import spam_checks
from dj_akismet.utils import do_spam_check
from main.models import Comment

class CommentCheck(AkismetCheck):

    def get_data(self):
        return {'user_ip': '127.0.0.1',
                'user_agent': 'user agent',
                'referrer': 'test referrer',
                'permalink': 'http://example.com/absolute/url/',
                'comment_type': 'comment',
                'comment_author': self.object.author.username,
                'comment_author_email': self.object.author.email,
                'comment_author_url': 'http://example.com/user/url/'}

    def get_content(self):
        return self.object.text

    def is_spam(self):
        print 'spam'

    def is_ham(self):
        print 'not spam'

spam_checks.register(Comment, CommentCheck)
post_save.connect(do_spam_check, sender=Comment, dispatch_uid='do_spam_check')
