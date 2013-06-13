import os
from setuptools import setup, find_packages

from feeds import __doc__, __version__, __author__, __email__


desc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name='django-generic-feeds',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url='https://bitbucket.org/wearefarm/django-generic-feeds',
    description=__doc__,
    long_description=desc,
    license='BSD',
    packages=find_packages(),
    install_requires=['Django >= 1.5'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django'
    ]
)
