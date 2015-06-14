django-vest
===========

.. image:: https://pypip.in/v/django-vest/badge.png
    :target: https://pypi.python.org/pypi/django-vest
    :alt: Latest PyPI version

Extension for default template system for making inheritance more flexible. Adding some kind of themes.

Usage
-----
Imagine you have several sites on different hosts. They differ by visually and small functional. ``django-vest`` this is a way to use one code base for this situation.

He allowing to split templates on ``themes`` - one per site. We also have extended inheritance between themes - we have `DEFAULT_THEME` and we can override each template in `CURRENT_THEME`. Exmaple:

.. code:: html

    {% extends 'DEFAULT_THEME/index.html' %}
    {% block page_title %}Dark theme{% endblock %}

``django-vest`` have some tools for logic splitting according by ``CURRENT_THEME`` in views. Assume we have some ``form`` class who is different in each theme. Then our code may looks like:


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


In example bellow ``Form`` class will be alias for DarkThemeForm if ``settings.CURRENT_THEME == 'dark_theme'`` otherwise it is ``DefaultForm``.

**Extends for default templates**

Version 0.1.3 has a new template loader ``django_vest.templates_loaders.AppsLoader`` and new keyword ``DJANGO_ORIGIN``.

Now we can override default django admin template without copy past of full origin file.

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

And add next setting options to your ``settings.py``:

.. code:: python

    TEMPLATE_LOADERS = (
        'django_vest.templates_loaders.Loader',
        'django_vest.templates_loaders.AppsLoader',
    )

    DEFAULT_THEME = 'main_theme'

    # Unique for each host
    CURRENT_THEME = 'dark_theme'


Then update structure of your templates like this:

.. code:: bash

    exampleproject/templates/
    | - dark_theme
        | - index.html
    | - main_theme
        | - index.html

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

    $ python setup.py test
    $ make test-all

6. Commit your changes and push your branch to GitHub:

.. code:: bash

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


Licence && Authors
-------------------
The MIT License (MIT)

Copyright (c) 2015 `Vladimir Savin <zero13cool@yandex.ru>`_.
