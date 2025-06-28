from setuptools import setup
import sys, os

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "chakkree_rebar_tools", "version.py")

with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.chakkree_rebar_tools',
      version=str(__version__),
      packages=['freecad',
                'freecad.chakkree_rebar_tools'],
      maintainer="chakkree tiyawongsuwan",
      maintainer_email="chakkree@hotmail.com",
      #url="",
      description="Workbench for rebar in concrete structure.",
      #install_requires=['numpy','scipy'],
      include_package_data=True)
