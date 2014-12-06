import zlib
import DataParse

import DestinyTexture
import DestinyGeometry

outputBin = "bin/decompressed_data.bin"

class DestinyModelClass(object):    
    def __init__(self, file):
        self.file = file
        with open(file, "rb") as f:
            # Verify the magic number
            self.magicNumber = int.from_bytes(f.read(4), byteorder='little')
            if self.magicNumber != 572728357:
                print("Invalid magic number: ", self.magicNumber, " exiting...")
                return
            
            print("Correct magic number:", self.magicNumber)
            
            # Read data into a byte array
            data = bytearray(f.read())
            print("Read ", len(data), " bytes into the byte array...")
            
            # Decompress the binary data
            data = zlib.decompress(data)
            print("Decompressed binary data...")
            fo = open(outputBin, 'wb')
            fo.write(data)
            fo.close()
            
            data = DataParse.DataParseClass(data)
    
            # Process textures
            print("Processing textures...")
            self.textures = DestinyTexture.DestinyTextureClass(data)
            
            # Process geometries
            print("Processing geometries...")
            self.geometry = DestinyGeometry.DestinyGeometryClass(data)
                
        return