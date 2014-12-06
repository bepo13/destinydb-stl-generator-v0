import numpy as np

class EmptyObject(object):
    pass

class VertexBufferClass:    
    POSITION = 1;
    MAX_POSITION = 3;
    TEX_COORD = 4;
    MAX_TEX_COORD = 11;
    NORMAL = 12;
    MAX_NORMAL = 18;
    TANGENT = 19;
    MAX_TANGENT = 25;
    COLOR = 26;
    MAX_COLOR = 32;
    BLEND_WEIGHT = 33;
    MAX_BLEND_WEIGHT = 39;
    BLEND_INDEX = 40;
    MAX_BLEND_INDEX = 47;
    
    def __init__(self, data):
        # Extract vertexBuffers
        self.vertexBuffers = []
        self.count = data.readInt32()
        
#         print("Number of vertexBuffers:", self.count)
        
        i = self.count
        while i > 0:
            # Create new vertexBuffer object
            vertexBuffer = EmptyObject()
            
            vertexBuffer.count = data.readInt32()
            vertexBuffer.data = []
            vertexBuffer.stride = data.readInt32()
            vertexBuffer.elements = EmptyObject()
            vertexBuffer.elements.count = data.readInt32()
            vertexBuffer.elements.data = []
            vertexBuffer.positions = []
            vertexBuffer.texCoords = []
            vertexBuffer.normals = []
            vertexBuffer.tangents = []
            vertexBuffer.colors = []
            vertexBuffer.blendWeights = []
            vertexBuffer.blendIndices = []
        
            slot = 0
            offset = 0
            
            # Add elements
            j = vertexBuffer.elements.count
            while j > 0:
                element = EmptyObject()
                
                # Read in the element type
                element.type = data.readInt8()
                element.slot = slot
                element.offset = offset
                
                startOffset = offset
                
                if (element.type >= self.POSITION) and (element.type <= self.MAX_POSITION):
                    offset += 4
                    element.type = self.POSITION
                elif (element.type >= self.TEX_COORD) and (element.type <= self.MAX_TEX_COORD):
                    offset += 2
                    element.type = self.TEX_COORD
                elif (element.type >= self.NORMAL) and (element.type <= self.MAX_NORMAL):
                    offset += 4
                    element.type = self.NORMAL
                elif (element.type >= self.COLOR) and (element.type <= self.MAX_COLOR):
                    offset += 4
                    element.type = self.COLOR
                elif (element.type >= self.TANGENT) and (element.type <= self.MAX_TANGENT):
                    offset += 4
                    element.type = self.TANGENT
                elif (element.type >= self.BLEND_WEIGHT) and (element.type <= self.MAX_BLEND_WEIGHT):
                    offset += 2
                    element.type = self.BLEND_WEIGHT
                elif (element.type >= self.BLEND_INDEX) and (element.type <= self.MAX_BLEND_INDEX):
                    offset += 2
                    element.type = self.BLEND_INDEX
                    
                if startOffset != offset:
                    slot += 1
                
                # Add new elements object
                vertexBuffer.elements.data.append(element)
                j -= 1
                
            vertexBuffer.stride = offset
            vertexBuffer.slots = slot
            
            # Read in vertexBuffer
            for j in range(vertexBuffer.count):
                for k in range(vertexBuffer.elements.count):
                    element = vertexBuffer.elements.data[k]
                    
                    if element.type == self.POSITION:
                        x = data.readFloat()
                        y = data.readFloat()
                        z = data.readFloat()
                        w = data.readFloat()
                        vertexBuffer.positions.append(np.array([x, y, z, w], dtype='float'))
                    elif element.type == self.TANGENT:
                        x = data.readFloat()
                        y = data.readFloat()
                        z = data.readFloat()
                        w = data.readFloat()
                        vertexBuffer.tangents.append(np.array([x, y, z, w], dtype='float'))
                    elif element.type == self.NORMAL:
                        x = data.readFloat()
                        y = data.readFloat()
                        z = data.readFloat()
                        w = data.readFloat()
                        vertexBuffer.normals.append(np.array([x, y, z, w], dtype='float'))
                    elif element.type == self.BLEND_WEIGHT:
                        vertexBuffer.blendWeights.append([data.readInt8(),data.readInt8(),data.readInt8(),data.readInt8()])
                    elif element.type == self.BLEND_INDEX:
                        vertexBuffer.blendIndices.append([data.readInt8(),data.readInt8(),data.readInt8(),data.readInt8()])
                    elif element.type == self.TEX_COORD:
                        u = data.readFloat()
                        v = data.readFloat()
                        vertexBuffer.texCoords.append(np.array([u, v], dtype='float'))
                    elif element.type == self.COLOR:
                        vertexBuffer.colors.append([data.readInt8(),data.readInt8(),data.readInt8(),data.readInt8()])
            
            # Add vertexBuffer to array
            self.vertexBuffers.append(vertexBuffer)
            i -= 1
        
        return
        
    def getPositions(self):
        for vB in self.vertexBuffers:
            if len(vB.positions) > 0:
                return vB.positions
    
    def getTexCoords(self):
        for vB in self.vertexBuffers:
            if len(vB.texCoords) > 0:
                return vB.texCoords
    
    def getNormals(self):
        for vB in self.vertexBuffers:
            if len(vB.normals) > 0:
                return vB.normals
    
    def getTangents(self):
        for vB in self.vertexBuffers:
            if len(vB.tangents) > 0:
                return vB.tangents
    
    def getColors(self):
        for vB in self.vertexBuffers:
            if len(vB.colors) > 0:
                return vB.colors
    
    def getBlendWeights(self):
        for vB in self.vertexBuffers:
            if len(vB.blendWeights) > 0:
                return vB.blendWeights
    
    def getBlendIndices(self):
        for vB in self.vertexBuffers:
            if len(vB.blendIndices) > 0:
                return vB.blendIndices

class DestinyPartClass:
    def __init__(self, data):
        # Read in part data
        self.indexStart = data.readInt16()
        self.indexCount = data.readInt16()
        self.indexMin = data.readInt16()
        self.indexMax = data.readInt16()
        self.flags = data.readInt32()
        self.primitive = data.readInt32()
        
        dyeIndex = data.readInt32()
        
        if dyeIndex == 1:
            self.dyeIndex = 0
            self.usePrimaryColor = False
        elif dyeIndex == 2:
            self.dyeIndex = 1
            self.usePrimaryColor = True
        elif dyeIndex == 3:
            self.dyeIndex = 1
            self.usePrimaryColor = False
        elif dyeIndex == 4:
            self.dyeIndex = 2
            self.usePrimaryColor = True
        elif dyeIndex == 5:
            self.dyeIndex = 2
            self.usePrimaryColor = False
        elif dyeIndex == 6:
            self.dyeIndex = 3
            self.usePrimaryColor = True
        elif dyeIndex == 7:
            self.dyeIndex = 3
            self.usePrimaryColor = True
        
        self.externalId = data.readInt32()
        self.levelOfDetail = data.readInt32()
        self.levelOfDetailName = data.readUTF()
        
        self.textures = EmptyObject()
        self.textures.data = []
        self.textures.count = data.readInt32()
        i = self.textures.count
        while i > 0:
            self.textures.data.append(data.readUTF())
            i -= 1
        
        if self.textures.count >= 5:
            self.diffuseTexture = self.textures.data[0]
            self.normalTexture = self.textures.data[2]
            self.stackTexture = self.textures.data[4]
        elif (self.textures.count > 0) and ("detail" not in self.textures.data[0]):
            self.diffuseTexture = self.textures.data[0]
        else:
            self.diffuseTexture = ""
        
        try:
            if ((self.flags & 32) != 0) or (self.diffuseTexture != "") or (self.normalTexture != "") or (self.stackTexture != ""):
                self.hasProgram = True
        except:
            self.hasProgram = False
            
        return
     
class DestinyMeshClass:
    def __init__(self, data):
        # Extract meshes
        self.meshes = []
        self.count = data.readInt32()
        
#         print("Number of meshes:", self.count)
        
        i = self.count
        while i > 0:
            # Create new mesh object
            mesh = EmptyObject()
            mesh.vertexBuffers = VertexBufferClass(data)
            
            # Parse the vertex buffers for all data sets
            mesh.positions = mesh.vertexBuffers.getPositions()
            mesh.texCoords = mesh.vertexBuffers.getTexCoords()
            mesh.normals = mesh.vertexBuffers.getNormals()
            mesh.tangents = mesh.vertexBuffers.getTangents()
            mesh.colors = mesh.vertexBuffers.getColors()
            mesh.blendWeights = mesh.vertexBuffers.getBlendWeights()
            mesh.blendIndices = mesh.vertexBuffers.getBlendIndices()
            
            # Add indices
            mesh.indices = EmptyObject()
            mesh.indices.count = data.readInt32()
            mesh.indices.data = []
            j = mesh.indices.count
            while j > 0:
                mesh.indices.data.append(data.readInt16())
                j -= 1
            
            # Read additional mesh data
            mesh.boundsMin = data.readVector3D()
            mesh.boundsMax = data.readVector3D()
            mesh.offset = data.readVector3D()
            mesh.scale = data.readVector3D()
            
            # Load mesh parts
            mesh.parts = EmptyObject()
            mesh.parts.count = data.readInt32()
            mesh.parts.data = []
            j = mesh.parts.count
            while j > 0:
                part = DestinyPartClass(data)
                
                # Process mesh part
                
                # Add mesh part
                mesh.parts.data.append(part)
                j -= 1
            
            self.meshes.append(mesh)
            i -= 1
        
        return


class DestinyPlatesClass:
    def __init__(self, data):
        # Extract plates
        self.plates = []
        self.count = data.readInt32()
        
#         print("Number of texture plates", self.count)
        
        i = self.count
        while i > 0:
            # Create new plate object
            plate = EmptyObject()
            
            plate.name = data.readUTF()
            plate.id = data.readUTF()
            plate.index = data.readInt32()
            plate.width = data.readInt16()
            plate.height = data.readInt16()
            plate.parts = []
            
            partCount = data.readInt32()
#             print("Number of plates parts:", partCount)

            while partCount > 0:
                # Create new part object
                part = EmptyObject()

                part.name = data.readUTF()
                part.index = data.readInt32()
                part.width = data.readInt16()
                part.height = data.readInt16()
                part.x = data.readInt16()
                part.y = data.readInt16()
                
                # Add part object
                plate.parts.append(part)
                partCount -= 1
            
            # Add plate object
            self.plates.append(plate)
            i -= 1
        
        return
        
class DestinyGeometryClass:
    def __init__(self, data):
        # Extract geometry
        self.geometry = []
        self.count = data.readInt32()
        
#         print("Number of geometries:", self.count)
        
        i = self.count
        while i > 0:
            # Create new geometry object
            geometry = EmptyObject()
              
            # Read length of string and add texture to list
            geometry.name = data.readUTF()
            geometry.meshes = DestinyMeshClass(data)
            geometry.plates = DestinyPlatesClass(data)
            
            # Add geometry object
            self.geometry.append(geometry)
            i -= 1
        
        return
    
def parse(data):
    return DestinyGeometryClass(data)