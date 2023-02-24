``stac-check`` documentation
############################

``stac-check`` is a linting and validation tool for STAC assets.

``stac-check`` is both a CLI tool and Python library. It adds additional linting and validation to the `stac-validator <https://github.com/stac-utils/stac-validator>`_ project.

The intent of this project is to provide a linting tool that also follows the official `STAC Best Practices document <https://github.com/radiantearth/stac-spec/blob/master/best-practices.md>`_.

This project was originally built with funding from the `Radiant Earth Foundation <https://radiant.earth/>`_ and ongoing support is provided by `Sparkgeo <https://sparkgeo.com/>`_ as well as other contributors.

Installation
------------

``stac-check`` can be installed from `pypi <https://pypi.org/project/stac-check/>`_:        

.. code-block:: bash

   $ pip install stac-check  

to install for local development:

.. code-block:: bash

   $ pip install -e . 


CLI Usage
---------

``stac-check`` can be used as a Python library or a command line tool.

.. code-block:: shell

   $ stac-check --help
   
   Usage: stac-check [OPTIONS] FILE

   Options:
      --version                Show the version and exit.
      -l, --links              Validate links for format and response.
      -a, --assets             Validate assets for format and response.
      -m, --max-depth INTEGER  Maximum depth to traverse when recursing. Omit this
                               argument to get full recursion. Ignored if
                              `recursive == False`.
      -r, --recursive          Recursively validate all related stac objects.
      --help                   Show this message and exit.

Examples
~~~~~~~~

.. code-block:: shell

   $ stac-check sample_files/0.9.0/landsat8-sample.json


Python Library Usage
--------------------

``stac-check`` can be used as a library to validate and lint STAC Items, Collections, and Catalogs. 
It can be used with local or remotely-hosted STAC objects as well as STAC objects represented as a Python dictionary.

Example - lint dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   from stac_check.lint import Linter

   dict = {
      "stac_version": "1.0.0",
      "stac_extensions": [],
      "type": "Feature",
      "id": "20201211_223832_CS2",
      "bbox": [
         172.91173669923782,
         1.3438851951615003,
         172.95469614953714,
         1.3690476620161975
      ],
      "geometry": {
      ...
   }
   linter = Linter(file, assets=True)

   for k,v in linter.create_best_practices_dict().items():
      print(k,":",v)

STAC Versions supported
~~~~~~~~~~~~~~~~~~~~~~~

``stac-check`` supports the following STAC versions:

``[0.8.0, 0.8.1, 0.9.0, 1.0.0-beta.1, 1.0.0-beta.2, 1.0.0-rc.1, 1.0.0-rc.2, 1.0.0-rc.3, 1.0.0-rc.4, 1.0.0]``

.. toctree::
   :maxdepth: 1
   
   api
   cli



.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
