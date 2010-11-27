import os
import sys

def setup_django(script_file, relpath=None):
    ROOT = os.path.dirname(os.path.realpath(script_file))
    if relpath:
        ROOT = os.path.join(ROOT, relpath)
    os.chdir(ROOT)
    sys.path.append(ROOT)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
