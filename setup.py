#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from setuptools import setup

setup(

	name				='py3dengine',
	version 			='0.0',
	description 		="""""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	
	packages=[
		'py3dengine',
		'py3dengine.bin',
		'py3dengine.cameras',
		'py3dengine.objects',
		'py3dengine.scenes',
		'py3dengine.utils',
		'py3dengine.utils.WavefrontOBJFormat',
		'py3dengine.thirdparty',
	],

	entry_points={
		'console_scripts':['py3d-engine-server=py3dengine.bin.RunSceneServer:main']
	}
)