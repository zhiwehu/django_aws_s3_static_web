from django.conf import settings

MAX_ZIP_FILE_SIZE = getattr(settings, 'MAX_ZIP_FILE_SIZE', 2*1024*1024)
AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
