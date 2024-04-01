from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.toolchain import shprint, current_directory, info
import sh
from os.path import join

class PlyerRecipe(PythonRecipe):
    version = '2.1.0'
    url = 'https://github.com/kivy/plyer/archive/{version}.zip'
    name = 'plyer'
    depends = ['pyjnius']
    site_packages_name = 'plyer'

    patches = ['master.patch', 'flash.patch']


recipe = PlyerRecipe()
