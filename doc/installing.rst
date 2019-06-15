Installing Adventurelib
=======================


With pip
--------

Adventurelib is pip-installable. If you have a working pip, you should be able
to simply type (at a command prompt)::

    pip install adventurelib


Single file
-----------

adventurelib is a single file. If you download the package from PyPI_ or browse
the project on GitHub_, ``adventurelib.py`` is all you need. You can save this
file alongside your game script and use it directly.

Optional Prompt Toolkit Support
-------------------------------

Adventurelib can make use of the prompt toolkit library to allow users to edit
commands as they enter them.  It is not required, but will be used if it is
installed in the Python environment. If you have a working pip, you should be
able to install both adventurelib and prompt toolkit with the command:

.. code-block:: console

    pip install adventurelib[prompt_toolkit]


.. _PyPI: https://pypi.python.org/pypi/adventurelib
.. _GitHub: https://github.com/lordmauve/adventurelib
