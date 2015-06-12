# coding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Django>=1.5.1',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name="django-vest",
    version="0.1.0",

    author="Vladimir Savin",
    author_email="zero13cool@yandex.ru",
    url="https://github.com/zerc/django-vest",

    description="Extension for default template system for making inheritance more flexible. Adding some kind of themes.",
    long_description=readme,

    packages=[
        'django_vest',
    ],
    package_dir={'django_vest':
                 'django_vest'},
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='django-vest',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
