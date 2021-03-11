# Gunicorn configuration file.
# This file can be used from the Gunicorn cli with the ``-c`` paramater.
# Eg. ``gunicorn -c <config_file>``
import multiprocessing
import os

bind = "0.0.0.0:10779"
workers = multiprocessing.cpu_count()