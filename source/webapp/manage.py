#!/usr/bin/env python

# pylint: skip-file  (django boilerplate)

"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quafel_web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
            "Did you maybe forget to use \"poetry run\" before the command?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
