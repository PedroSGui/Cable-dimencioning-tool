from distutils.core import setup
import py2exe
setup(windows=[{'script': 'ui.py'}],
          options={"py2exe": {"includes": ["tkinter"],
                    "packages" : ["sqlite3"],
                             'bundle_files': 3,
                              'compressed': False}},
          zipfile = None     )