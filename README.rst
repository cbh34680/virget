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
    $ chmod a+x ./virget/bin/virget
    $ export PATH="${PWD}/virget/bin:${PATH}"
    $ which virget


Examples
---------------

You can get similar results to some commands in virsh.

::

    $ sudo -E virget help

.. note::
    ``sudo -E`` is required to connect to libvirtd

Comparison with virsh

::

    $ sudo -E virget --pretty list 
    {
      "data": [
        {
          "id": 1,
          "name": "vhcalnplci",
          "state": "running"
        }
      ]
    }
    $ LANG=C sudo -E virsh list 
     Id   Name         State
    ----------------------------
     1    vhcalnplci   running

    $ sudo -E virget --pretty domblklist 1
    {
      "data": [
        {
          "target": "vda",
          "source": "/disk/2/clone.d/ubuntu16/vhcalnplci.qcow2"
        }
      ]
    }
    $ LANG=C sudo -E virsh domblklist 1
     Target   Source
    -----------------------------------------------------
     vda      /disk/2/clone.d/ubuntu16/vhcalnplci.qcow2

