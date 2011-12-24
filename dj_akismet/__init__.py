# do autodiscovery on spam_checks
# look at the akismet_check sources setting and import all modules
# that contain spam checks, so they get added to the registry and
# their signals are registered
from django.conf import settings

SOURCES = getattr(settings, 'AKISMET_CHECK_SOURCES', [])
for source in SOURCES:
    __import__(source)
