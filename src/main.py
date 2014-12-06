import DestinyModel
import DestinyModelGenStl

itemName = "mythoclast"
itemFileName = "stl/mythoclast.stl"
itemGeom = "geom/346443849.geom"

playerName = "r4ndy_moss"
playerFileName = "stl/r4ndy_moss.stl"
playerGeomHead = "geom/144553854.geom"
playerGeomBody = "geom/3833808556.geom"
playerGeomGloves = "geom/1835128980.geom"
playerGeomBoots = "geom/1698410142.geom"
playerGeomClass = "geom/3790886867.geom"

if __name__ == '__main__':
    # Parse single destinydb geom file and generate item model .stl output
    itemModel = []
    itemModel.append(DestinyModel.parse(itemGeom))
    DestinyModelGenStl.generate(itemModel, itemName, itemFileName)
    
    # Parse multiple destinydb geom files and generate player model .stl output
    playerModel = []
    playerModel.append(DestinyModel.parse(playerGeomHead))
    playerModel.append(DestinyModel.parse(playerGeomBody))
    playerModel.append(DestinyModel.parse(playerGeomGloves))
    playerModel.append(DestinyModel.parse(playerGeomBoots))
    playerModel.append(DestinyModel.parse(playerGeomClass))
    DestinyModelGenStl.generate(playerModel, playerName, playerFileName)
    
    print("Done")