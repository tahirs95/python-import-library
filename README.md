# Setup

To prepare for running ensure these tools and packages are installed:
* Python 3 - at least Python 3.6.4 or later
* SQL Alchemy 1.3

For Postgres support and unit tests these packages are also required:
* geoalchemy2
* psycopg2
* nose2 (0.9.1)

To install packages use `pip install <package>` or `py -3 -m pip install <package>` depending on your installation

# Command Line Instructions

To run from the command line go to the top level directory of the library in your bash shell or terminal program

Run by specifying the program as a module with `-m` and leaving off the .py file extension

The exact executable name for invoking python will depend how you have it installed, but most commonly it's just `python`
  
For example run the Sqlite example using:  
```python -m Experiments.DataStore_sqliteExperiment```

# IntelliJ Instructions

To run from inside IntelliJ open the project  
Mark the `Store` package as source by right clicking on the directory and selecting `Mark Directory as -> Source Root`

Open any python module you want to run in the main editor window, right click anywhere in the editor and choose the `Run` or `Debug` option

# Jupyter demo

Link to HelloWorld demo script: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/debrief/python-import-library/master?filepath=jupyter%2FHelloWorld.ipynb)


Placeholder for live Jupyter view of whole repo
[![Master branch](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/debrief/python-import-library/master)
