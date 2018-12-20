===============================
Python
===============================

Python is a widely used high-level programming language for general-purpose programming, created by Guido van Rossum and first released in 1991. An interpreted language, Python has a design philosophy which emphasizes code readability (notably using whitespace indentation to delimit code blocks rather than curly brackets or keywords), and a syntax which allows programmers to express concepts in fewer lines of code than might be used in languages such as C++ or Java.The language provides constructs intended to enable writing clear programs on both a small and large scale.

Python features a dynamic type system and automatic memory management and supports multiple programming paradigms, including object-oriented, imperative, functional programming, and procedural styles. It has a large and comprehensive standard library.

Python interpreters are available for many operating systems, allowing Python code to run on a wide variety of systems. CPython, the reference implementation of Python, is open source software and has a community-based development model, as do nearly all of its variant implementations. CPython is managed by the non-profit Python Software Foundation.

===============================
Boto 3 - The AWS SDK for Python
===============================

|Build Status| |Version| |Gitter|

Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for
Python, which allows Python developers to write software that makes use
of services like Amazon S3 and Amazon EC2. You can find the latest, most
up to date, documentation at our `doc site`_, including a list of
services that are supported.


.. _boto: https://docs.pythonboto.org/
.. _`doc site`: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
.. |Build Status| image:: http://img.shields.io/travis/boto/boto3/develop.svg?style=flat
    :target: https://travis-ci.org/boto/boto3
    :alt: Build Status
.. |Gitter| image:: https://badges.gitter.im/boto/boto3.svg
   :target: https://gitter.im/boto/boto3
   :alt: Gitter
.. |Downloads| image:: http://img.shields.io/pypi/dm/boto3.svg?style=flat
    :target: https://pypi.python.org/pypi/boto3/
    :alt: Downloads
.. |Version| image:: http://img.shields.io/pypi/v/boto3.svg?style=flat
    :target: https://pypi.python.org/pypi/boto3/
    :alt: Version
.. |License| image:: http://img.shields.io/pypi/l/boto3.svg?style=flat
    :target: https://github.com/boto/boto3/blob/develop/LICENSE
    :alt: License

Quick Start
-----------
First, install the library and set a default region:

.. code-block:: sh

    $ pip install boto3

Next, set up credentials (in e.g. ``~/.aws/credentials``):

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET

Then, set up a default region (in e.g. ``~/.aws/config``):

.. code-block:: ini

    [default]
    region=us-east-1

Then, from a Python interpreter:

.. code-block:: python

    >>> import boto3
    >>> s3 = boto3.resource('s3')
    >>> for bucket in s3.buckets.all():
            print(bucket.name)

Getting started with Boto 3 is easy, but requires a few steps.

Installation
------------
Install the latest Boto 3 release via pip:

pip install boto3
You may also install a specific version:

pip install boto3==1.0.0

Configuration
-------------
Before you can begin using Boto 3, you should set up authentication credentials. Credentials for your AWS account can be found in the IAM Console. You can create or use an existing user. Go to manage access keys and generate a new set of keys.

If you have the AWS CLI installed, then you can use it to configure your credentials file:

aws configure
-------------
Alternatively, you can create the credential file yourself. By default, its location is at ~/.aws/credentials:

[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
You may also want to set a default region. This can be done in the configuration file. By default, its location is at ~/.aws/config:

[default]
region=us-east-1
Alternatively, you can pass a region_name when creating clients and resources.

This sets up credentials for the default profile as well as a default region to use when creating connections. See Credentials for in-depth configuration sources and options.
