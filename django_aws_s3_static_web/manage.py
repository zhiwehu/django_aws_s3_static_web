#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_aws_s3_static_web.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)