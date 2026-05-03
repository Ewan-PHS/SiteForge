import json
from zipfile import ZipFile
import math
import matplotlib.pyplot as plt
from pathlib import Path

##########################################################################

def setXYZComponents(Index):
    if currentJson["data"]["orientation"][Index] == "x":
        varToSet = [currentJson["lines"][i]['X1'], currentJson["lines"][i]['X2']]
    elif currentJson["data"]["orientation"][Index] == "y":
        varToSet = [currentJson["lines"][i]['Y1'], currentJson["lines"][i]['Y2']]
    elif currentJson["data"]["orientation"][Index] == "0":
        varToSet = [0,0]
    
    return varToSet

##########################################################################

jsonFiles = {}

rootPath = Path("test_square.sfmodel")

if rootPath.suffix == ".sfmodel" or ".sfm" or ".zip":
    with ZipFile(rootPath) as openedZIP:
        for file in iter(openedZIP.filelist):
            if (not file.is_dir()) and (not file.filename.find(".json") == -1):
                with openedZIP.open(file.filename, "r") as openedFile:
                    jsonFiles.update({file.filename.removesuffix(".json"): json.load(openedFile)})
                    openedFile.close()
else:
    for file in Path.iterdir(rootPath):
        if file.is_file() and file.suffix == ".json":
            with open(f"{rootPath}\\{file.name}", "r") as openedFile:
                jsonFiles.update({file.stem: json.load(openedFile)})
                openedFile.close()

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

for key in jsonFiles:
    currentJson = jsonFiles[key]
    for i in range(len(currentJson["lines"])):
        match currentJson["lines"][i]['line_type']:
            case 'solid':
                lineType = '-'
            case 'hidden':
                lineType = '--'
            case 'center':
                lineType = '-.'

        xComponent = setXYZComponents(0)
        yComponent = setXYZComponents(1)
        zComponent = setXYZComponents(2)
    
        ax.plot(xComponent,yComponent,zComponent, color=currentJson["data"]["colour"], linestyle= lineType)

plt.show()