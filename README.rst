sketchduino
===========

The next version of this tool on 07/16/2013 previta to be published at any time, provided that all requirements for the next release is reached.

|Build Status| |PyPy compatible|

.. |Build Status| image:: https://travis-ci.org/rodrigopmatias/sketchduino.png
   :target: https://travis-ci.org/rodrigopmatias/sketchduino
.. |PyPy compatible| image:: https://pypip.in/v/sketchduino/badge.png
   :target: https://pypi.python.org/pypi/sketchduino

The Arduino IDE is a very good tool when you are learning to develop for
AVR family of microcontrollers, but it becomes a barrier to more
structured projects. In view of these difficulties it was decided to
create a tool to automate the creation and maintenance of projects.

The sketchduino will create a complete project, a project will be
created with the following structure:

-  binary (result of compile processes)
-  lib (custom libraries of projetct future)
-  include (custom libraries of projetct future)
-  src (the code of you project)
-  tmp (temporary files of processes of compiler)

How to install this
-------------------

To install sketchduino is very simple, as it is a python tool you can
install it using the tool easy\_install or pip is the second most
recommended.

See how we can install using easy\_install:

    ``root@host ~/ # easy_install sketchduino``

With this command will be installed and its dependencies sketchduino
Site Packages Python.

Now see how to install using pip:

    ``root@host ~/ # easy_install sketchduino``

With this command will be installed and its dependencies sketchduino
Site Packages Python.

How to use this
---------------

The sketchduino is a command line tool, but its use is very simple and
can be easyly integrated with some good editor such as Vim and
SublimeText. Let's see how to use sketchduino.

::

    user@host ~/ $ sketchduino --help
    usage: sketchduino [-h] [--processor MCU] [--clock CLOCK] [--sdk SDK_HOME]
                       [--avr AVR_HOME] --cmd COMMAND [--project PROJECT_HOME]
                       [--programer PROGRAMER] [--variant VARIANT]

    The Arduino Sketch utiliter

    optional arguments:
      -h, --help            show this help message and exit
      --processor MCU       The name of Microcontroler Unit.
      --clock CLOCK         The clock of Microcontroler Unit in MHz.
      --sdk SDK_HOME        The path for SDK of arduino.
      --avr AVR_HOME        The path for AVR/GNU compiler.
      --cmd COMMAND         The command for Sketch utility.
      --project PROJECT_HOME
                            The home directory for project.
      --programer PROGRAMER
                            The programer hardware for deploy you firmwire.
      --variant VARIANT     The variante of your arduino.

Command Help
------------

The secret of this tool is are your commands and you can see the list of
commands with the following command:

::

    user@host ~/ $ sketchduino --cmd help
    Start of Arduino Sketch Utility.
    -------
     build
        Performs project build according to the settings, only compiles what
        has changed since the last compilation if cache.

     clean
        Performs cleaning the last compilation.

     deploy
        Command not implemented yet.

     variant-listNone
     create
        Handles the project.

     rebuild
        Performs cleaning the cache and performs compile a new build complete.

     show
        Displays current configuration information of the project.

     update
        Handles the project.

     library-list
        Command not implemented yet.

    -------
    End of Arduino Sketch Utility.