#!/usr/bin/python3.6
"""Create a new Django webapp with a virtualenv.  Defaults to
your free domain, the latest version of Django and Python 3.6

Usage:
  pa_start_django_webapp_with_virtualenv.py [--domain=<domain> --django=<django-version> --python=<python-version>] [--nuke]

Options:
  --domain=<domain>         Domain name, eg www.mydomain.com   [default: your-username.pythonanywhere.com]
  --django=<django-version> Django version, eg "1.8.4"  [default: latest]
  --python=<python-version> Python version, eg "2.7"    [default: 3.6]
  --nuke                    *Irrevocably* delete any existing web app config on this domain. Irrevocably.
"""

from docopt import docopt
import getpass

from pythonanywhere.snakesay import snakesay
from pythonanywhere.api import (
    add_static_file_mappings,
    create_webapp,
    reload_webapp,
)

from pythonanywhere.django_project import DjangoProject


def main(domain, django_version, python_version, nuke):
    if domain == 'your-username.pythonanywhere.com':
        username = getpass.getuser().lower()
        domain = f'{username}.pythonanywhere.com'

    project = DjangoProject(domain)
    project.python_version = python_version

    project.sanity_checks(nuke=nuke)
    project.create_virtualenv(django_version, nuke=nuke)
    project.run_startproject(nuke=nuke)
    project.update_settings_file()
    project.run_collectstatic()

    create_webapp(domain, python_version, project.virtualenv_path, project.project_path, nuke=nuke)
    add_static_file_mappings(domain, project.project_path)

    project.update_wsgi_file()

    reload_webapp(domain)

    print(snakesay(f'All done!  Your site is now live at https://{domain}'))



if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments['--domain'], arguments['--django'], arguments['--python'], nuke=arguments.get('--nuke'))

