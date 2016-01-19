

class WavefrontFileLoader:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
 
        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.replace(',', '.').split()
            if not values: continue

            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz: v = v[0], v[2], v[1]
                self.vertices.append(v)

            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz: v = v[0], v[2], v[1]
                self.normals.append(v)

            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))

            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]

            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])

            elif values[0] == 'f':
                face = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))

                self.faces.append(face)



if __name__ == "__main__":

    obj = WavefrontFileLoader('/home/ricardo/Desktop/teste.obj')

    print obj.faces
    print obj.vertices