virget
=======

It behaves similar to virsh for some commands.
The output is in JSON format, so it can be used for batch processing, etc.

.. note::
    ``virget`` was tested with version python3.11.

Jump to:

-  `Getting Started <#getting-started>`__
-  `Examples <#examples>`__

Getting Started
---------------

To make installation easier, grab the file and add the path to ``bin``

Dependencies
~~~~~~~~~~~

- Linux virtualization environment with libvirt
- ``jmespath``: 1.0.1 or greater
- ``xmltodict``: 0.13.0 or greater

Installation
~~~~~~~~~~~

Here, the path is set to bin in the directory obtained from github.

::

    $ git clone https://github.com/cbh34680/virget.git
    $ export PATH="${PWD}/virget/bin:${PATH}"
    $ which virget


Examples
---------------

You can get similar results to some commands in virsh.

::

    $ sudo -E virget help

.. note::
    ``sudo -E`` is required to connect to libvirt

