valve |valve_icon|
##################
|PyPI-Status| |PyPI-Versions| |Build-Status| |Codecov| |LICENCE|

Automate and version datasets generation from data sources.

.. |valve_icon| image:: https://github.com/shaypal5/birch/blob/cc5595bbb78f784a3174a07157083f755fc93172/birch.pn://github.com/shaypal5/valve/blob/63d09d8e950bf889372f3a0bda30d47348d6c13d/valve.png  
   
.. code-block:: python

  import valve
  # mystery code

.. contents::

.. section-numbering::


Installation
============

.. code-block:: bash

  pip install valve


Setting up valve
===================

valve uses a couple of simple conventions to handle credentials and refer to MongoDB servers:

Credentials file
----------------

You must set up a credentials file for valve to use. Create a ``.valve/valve_credentials.yml`` file in your home folder, populating it with your MongoDB credentials, using an identical structure to the inner structure of the ``envs`` configuration parameters:

.. code-block:: python

  environment_name:
    server_name:
      reading:
        username: reading_username
        password: password1
      writing:
        username: writing_username
        password: password2

You can extend this to include any number of environments and servers.


Basic Use
=========

Pass.


Contributing
============

Package author and current maintainer is Shay Palachy (shay.palachy@gmail.com); You are more than welcome to approach him for help. Contributions are very welcomed.

Installing for development
----------------------------

Clone:

.. code-block:: bash

  git clone git@github.com:shaypal5/valve.git


Install in development mode:

.. code-block:: bash

  cd valve
  pip install -e .


Running the tests
-----------------

To run the tests use:

.. code-block:: bash

  pip install pytest pytest-cov coverage
  cd valve
  pytest


Adding documentation
--------------------

The project is documented using the `numpy docstring conventions`_, which were chosen as they are perhaps the most widely-spread conventions that are both supported by common tools such as Sphinx and result in human-readable docstrings. When documenting code you add to this project, follow `these conventions`_.

.. _`numpy docstring conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`these conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


Credits
=======

Created by Shay Palachy (shay.palachy@gmail.com).


.. |PyPI-Status| image:: https://img.shields.io/pypi/v/valve.svg
  :target: https://pypi.python.org/pypi/valve

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/valve.svg
   :target: https://pypi.python.org/pypi/valve

.. |Build-Status| image:: https://travis-ci.org/shaypal5/valve.svg?branch=master
  :target: https://travis-ci.org/shaypal5/valve

.. |LICENCE| image:: https://img.shields.io/github/license/shaypal5/valve.svg
  :target: https://github.com/shaypal5/valve/blob/master/LICENSE

.. |Codecov| image:: https://codecov.io/github/shaypal5/valve/coverage.svg?branch=master
   :target: https://codecov.io/github/shaypal5/valve?branch=master
