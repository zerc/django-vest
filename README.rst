django-vest
===========

.. image:: https://img.shields.io/pypi/v/django-vest.svg
    :target: https://pypi.python.org/pypi/django-vest
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/zerc/django-vest.svg?branch=master
    :target: https://travis-ci.org/zerc/django-vest
    :alt: Build status

Extension of default template system what makes inheritance more flexible through add themes.

Usage
-----
Imagine that you have several sites on different hosts. They differ by visually and functionally a bit. ``django-vest`` provides the way to use the same code base in such kind of situations.

It allows splitting templates into ``themes`` - for one per site. Also, it provides the extended inheritance between these themes through `DEFAULT_THEME` keyword. Using this keyword in templates we can override each template. For example:

.. code:: html

    {% extends 'DEFAULT_THEME/index.html' %}
    {% block page_title %}Dark theme{% endblock %}

``django-vest`` has several ways to split a logic according to ``CURRENT_THEME`` in views. Assume that you have some ``form`` class which is different for each theme. Then your code may look like:


.. code:: python

    # forms.py
    from django_vest.decorators import themeble

    @themeble(name='Form', themes=('dark_theme',))
    class DarkThemeForm(object):
        ''' Some kind of logic/fields for dark_theme form
        '''
        name = 'DarkThemeForm'


    @themeble(name='Form')
    class DefaultForm(object):
        ''' Default logic/fields for all themes
        '''
        name = 'Default form'


    # views.py
    from .forms import Form


In example above ``Form`` class will be an alias for DarkThemeForm if ``settings.CURRENT_THEME == 'dark_theme'``, otherwise it is ``DefaultForm``.

You can use ``only_for`` decorator to restrict access to particular view according to value of ``CURRENT_THEME``:

.. code:: python

    # views.py
    from django.http import Http404
    from django.views.generic.base import TemplateView

    from django_vest import only_for

    @only_for('black_theme')
    def my_view(request):
        ...

    # Redirect for special page
    dark_theme_page = only_for('dark_theme', redirect_to='restict_access')(
        TemplateView.as_view(template_name='dark_theme_page.html'))

    # Raise Http404 when user trying to open page with invalid theme
    dark_theme_page_not_found = \
        only_for('dark_theme', raise_error=Http404)(
            TemplateView.as_view(template_name='dark_theme_page.html'))


**Extends of default templates**

Version 0.1.3 has a new template loader ``django_vest.templates_loaders.AppsLoader`` and new keyword ``DJANGO_ORIGIN``.

Now you can override default django admin template without copy&pasting of whole origin file.

Example:

File: ``templates/main_theme/admin/change_list.html``

.. code:: html

    {% extends "DJANGO_ORIGIN/admin/change_list.html" %}
    {% load i18n admin_urls admin_static admin_list %}

    {% block breadcrumbs %}
      <div>Template has been overridden</div>
      {{ block.super }}
    {% endblock %}


Installation
------------

.. code:: bash

    $ pip install django_vest

Add next setting options to your ``settings.py``:

.. code:: python

    TEMPLATE_LOADERS = (
        'django_vest.templates_loaders.Loader',
        'django_vest.templates_loaders.AppsLoader',
    )

    DEFAULT_THEME = 'main_theme'

    # Unique for each host
    CURRENT_THEME = 'dark_theme'

Or you can set the OS environment:

.. code:: bash

    export DJANGO_VEST_CURRENT_THEME=dark_theme

You can specify a list of backends for getting settings. Default is:

.. code:: python

    VEST_SETTINGS_BACKENDS_LIST = (
        'django_vest.config.backends.simple',
        'django_vest.config.backends.env'
    )

* django_vest.config.backends.simple - getting settings about theme from project`s settings file.
* django_vest.config.backends.env - from os envirom

Then you need to update a structure of your templates like this:

.. code:: bash

    exampleproject/templates/
    | - dark_theme
        | - index.html
    | - main_theme
        | - index.html

**IMPORTANT**: theme folder must ends with *_theme* suffix (example: my_super_mega_theme)

Other config backends (Experimental)
------------------------------------
Django-vest have are several other backends like:

``django_vest.config.backends.database``. If you have some singleton model to store settings of your site you can use ``django_vest.fields.VestField`` to store value of  ``CURRENT_THEME`` in database.

To activate this feature you have to do next:

* Add ``django_vest.fields.VestField`` to your settings model and do migrate.
* Add ``django_vest.config.backends.database`` backend to the top of ``VEST_SETTINGS_BACKENDS_LIST`` setting. Example:

.. code:: python

    VEST_SETTINGS_BACKENDS_LIST = (
        'django_vest.config.backends.database',
        'django_vest.config.backends.simple',
        'django_vest.config.backends.env',
    )


Contributing
------------

1. Fork the `django-vest` repo on GitHub.
2. Clone your fork locally:

.. code:: bash

    $ git clone git@github.com:your_name_here/django-vest.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

.. code:: bash

    $ mkvirtualenv django-vest
    $ cd django-vest/
    $ python setup.py develop

4. Create a branch for local development:

.. code:: bash

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests, including testing other Python versions with tox:

.. code:: bash

    $ make test-all

6. Commit your changes and push your branch to GitHub:

.. code:: bash

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


Licence & Authors
-------------------
The MIT License (MIT)

Copyright (c) 2015 `Vladimir Savin <zero13cool@yandex.ru>`_.
