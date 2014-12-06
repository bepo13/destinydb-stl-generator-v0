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
    # Parse destinydb geom file and generate .stl output for a single item model
    itemModel = []
    itemModel.append(DestinyModel.DestinyModelClass(itemGeom))
    DestinyModelGenStl.generate(itemModel, itemName, itemFileName)
    
    playerModel = []
    playerModel.append(DestinyModel.DestinyModelClass(playerGeomHead))
    playerModel.append(DestinyModel.DestinyModelClass(playerGeomBody))
    playerModel.append(DestinyModel.DestinyModelClass(playerGeomGloves))
    playerModel.append(DestinyModel.DestinyModelClass(playerGeomBoots))
    playerModel.append(DestinyModel.DestinyModelClass(playerGeomClass))
    
    DestinyModelGenStl.generate(playerModel, playerName, playerFileName)
    
    print("Done")