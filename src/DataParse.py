import io
import struct
import numpy as np

class DataParseClass:
    def __init__(self, byteData):
        self.data = io.BytesIO(byteData)
        return
        
    def readUTF(self):
        length = int.from_bytes(self.data.read(2), byteorder='little')
        return self.data.read(length).decode('utf-8')
    
    def readInt8(self):
        return int.from_bytes(self.data.read(1), byteorder='little')
    
    def readInt16(self):
        return int.from_bytes(self.data.read(2), byteorder='little')
    
    def readInt32(self):
        return int.from_bytes(self.data.read(4), byteorder='little')
    
    def readFloat(self):
        return struct.unpack('f', self.data.read(4))[0]
    
    def readVector2D(self):
        return np.array([self.readFloat(), self.readFloat()], dtype='float')
    
    def readVector3D(self):
        return np.array([self.readFloat(), self.readFloat(), self.readFloat()], dtype='float')
    
    def readVector4D(self):
        return np.array([self.readFloat(), self.readFloat(), self.readFloat(), self.readFloat()], dtype='float')