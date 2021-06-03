import os
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJObject import WavefrontOBJObject

class WavefrontOBJReader(object):
	

	def __init__(self, objFilePath):
		self._materials = {}
		self._objects   = []

		objFilePath = str(objFilePath)

		objFileName 	= os.path.basename(objFilePath)
		objFileDir 		= os.path.dirname(objFilePath)
		scenename, _ 	= os.path.splitext(objFileName)
		materialsFile 	= os.path.join(objFileDir, scenename+'.mtl')
		if not os.path.isfile(materialsFile): materialsFile = objFilePath
		
		self.__loadMaterials( materialsFile)
		self.__loadObjects(	 objFilePath)

	@property
	def objects(self): return [x for x in self._objects if not x.getProperty('type')=='Camera']

	@property
	def cameras(self): return [x for x in self._objects if x.getProperty('type')=='Camera']

			
	def __loadMaterials(self, filename):
		infile = open(filename, 'r')

		currentMaterial = None
		for line in infile:

			if line.startswith('newmtl '):
				currentMaterial = {}
				currentMaterial['name'] = line.strip('\n')[7:]

			if line.startswith('Ka '):
				values = list(map(float, line.replace(',','.').strip('\n')[3:].split(' ')))
				currentMaterial['Ka'] = values

			if line.startswith('d '):
				value = float(line.replace(',','.').strip('\n')[2:])
				currentMaterial['Ka'].append( value )

			if line=='\n' and 'name' in currentMaterial:
				self._materials[currentMaterial['name']] = currentMaterial
		
		infile.close()


	def __loadObjects(self, filename):
		infile = open(filename, 'r')

		currentObject = None
		for line in infile:
	
			if line.startswith('o '):
				name = line.strip('\n')[2:]
				currentObject = WavefrontOBJObject( name )
				
			if line.startswith('usemtl '):
				material = line.strip('\n')[7:]
				currentObject.color = self._materials[material]['Ka'] if material in self._materials else (1,1,1,1)

			if line.startswith('v '):
				values = list(map(float, line.replace(',','.').strip('\n')[2:].split(' ')[:3] ))
				currentObject.addVertice( values )

			if line.startswith('# '):
				prop, values = self.__parseProperty(line)
				currentObject.addProperty(prop, values)

			if line=='\n' and currentObject!=None:
				self._objects.append( currentObject )

		infile.close()



	def __parseProperty(self, line):
		prop, value = line[2:].strip('\n').split(': ')


		if ', ' in value: 
			#value = value.split(',')
			#value = map(float, value)
			value = eval(value)

		return prop, value