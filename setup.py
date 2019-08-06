import re

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('prometheus_http_sdk/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

packages = [
    'prometheus_http_sdk',
]

requires = [
    "requests"
]

setup(
    name='prometheus_http_sdk',
    description='prometheus http sdk',
    author='Redheat',
    url='https://github.com/RedheatWei/prometheus_http_sdk_py',
    download_url='https://github.com/RedheatWei/prometheus_http_sdk_py',
    author_email='qjyyn@qq.com',
    version=version,
    long_description_content_type='text/markdown',
    package_dir={'prometheus_http_sdk': 'prometheus_http_sdk'},
    packages=packages,
    install_requires=requires,
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description=readme,
    package_data={'': ['README.md']},
    include_package_data=True,
)
