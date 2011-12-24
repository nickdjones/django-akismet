from dj_akismet.models import AkismetCheckItem


def do_spam_check(sender, instance, created, *args, **kwargs):
    """ Performs a spam check on the instance.
    """
    if created:
        # auto_check is true by default, so creating the AkismetCheckItem will
        # cause it to be submitted to Akismet for checking
        item = AkismetCheckItem(content_obj=instance)

def mark_as_spam(modeladmin, request, queryset, **kwargs):
    """ Mark an item as spam - used in admin actions.
    """
    for obj in queryset:
        item = AkismetCheckItem(content_obj=obj, auto_check=False)
        item.mark_as_spam()

def mark_as_ham(modeladmin, request, queryset, **kwargs):
    """ Mark an item as ham - used in admin actions.
    """
    for obj in queryset:
        item = AkismetCheckItem(content_obj=obj, auto_check=False)
        item.mark_as_ham()
