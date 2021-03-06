import os
from unittest import TextTestRunner, TestLoader

# import pydevd
# pydevd.settrace('localhost', port=8080, stdoutToServer=True, stderrToServer=True, suspend=False)


def run():
    """Will be executed from the Vectorworks testing document by running its Testing script.

    Make sure that the DLibrary folder is added to the Python script paths in Vectorworks.
    Running the script will throw up an error, which will just show the results of the test run.
    """
    TextTestRunner(verbosity=2).run(TestLoader().discover(os.path.dirname(__file__), 'test_*.py'))
