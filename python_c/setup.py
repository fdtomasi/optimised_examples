from distutils.core import setup, Extension

module1 = Extension('spam',
                    sources = ['spammodule.c'])

setup (name = 'pythonc_c',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
