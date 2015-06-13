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

Installation
------------

Just type: ``pip install django_vest``

Contributing
------------

1. Fork the `django-vest` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/django-vest.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv django-vest
    $ cd django-vest/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests, including testing other Python versions with tox::

    $ python setup.py test
    $ make test-all

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


Licence && Authors
-------------------
The MIT License (MIT)

Copyright (c) 2015 `Vladimir Savin <zero13cool@yandex.ru>`_.
