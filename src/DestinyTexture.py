class DestinyTextureClass:
    def __init__(self, data):
        # Extract textures
        self.textures = []
        self.count = data.readInt32()
        
#         print("Number of textures:", self.count)
        
        i = self.count
        while i > 0:
            # Read length of string and add texture to list
            self.textures.append(data.readUTF())
            i -= 1
        return
    
def parse(data):
    return DestinyTextureClass(data)