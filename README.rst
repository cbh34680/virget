virget
=======

Runs some commands similar to virsh and returns the results in JSON format.
Therefore, it can be conveniently used for batch processing in shell scripts.

For example ``virsh list``, ``virsh domblklist`` etc.

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

.. note::
    ``virget`` was tested with version python3.11.

Installation
~~~~~~~~~~~

Here, the path is set to bin in the directory obtained from github.

::

    $ sudo -i
    # git clone https://github.com/cbh34680/virget.git
    # chmod u+x ./virget/bin/virget
    # export PATH="${PWD}/virget/bin:${PATH}"
    # which virget


Examples
---------------

See help for all available commands.

::

    # virget help

or have a look at this `command-files <virpy/command>`_

Comparison with virsh.

*list*
::

    # virsh list 
     Id   Name         State
    ----------------------------
     1    vhcalnplci   running
    
    # virget --pretty list 
    {
      "data": [
        {
          "id": 1,
          "name": "vhcalnplci",
          "state": "running"
        }
      ]
    }

*domblklist*
::

    # virsh domblklist 1
     Target   Source
    -----------------------------------------------------
     vda      /disk/2/clone.d/ubuntu16/vhcalnplci.qcow2
    
    # virget --pretty domblklist 1
    {
      "data": [
        {
          "target": "vda",
          "source": "/disk/2/clone.d/ubuntu16/vhcalnplci.qcow2"
        }
      ]
    }

