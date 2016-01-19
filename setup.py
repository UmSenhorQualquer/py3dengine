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

	name				='py3DEngine',
	version 			='0.0',
	description 		="""""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	
	packages=[
		'py3DEngine',
		'py3DEngine.bin',
		'py3DEngine.cameras',
		'py3DEngine.objects',
		'py3DEngine.scenes',
		'py3DEngine.utils',
		'py3DEngine.utils.WavefrontOBJFormat',
		'py3DEngine.thirdparty',
		],

	install_requires=[
		"pyopengl >= 3.1.0",
		"numpy >= 1.6.1"
	],

	entry_points={
		'console_scripts':['py3DEngine-server=py3DEngine.bin.RunSceneServer:main']
	}
)