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

rootPath = Path("C:\\Not_Onedrive\\GitHub\\SIP-Project-2026\\Version-2\\Python\\test_json")

if (rootPath.suffix == ".sfmodel") or (rootPath.suffix == ".sfm") or (rootPath.suffix == ".zip"):
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

xPoints = []
yPoints = []
zPoints = []

viewsData = {} # formatted as {viewname: {linetype: {lines: {}, verticies: {} } } }

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

        xPoints = list(set(xPoints) | set(xComponent))
        yPoints = list(set(yPoints) | set(yComponent))
        zPoints = list(set(zPoints) | set(zComponent))

        # viewsData.update({key: {currentJson["lines"][i]["linetype"]: {"verticies": [[]]}}}) this is bad, it needs to be outside these loops in another loop like this one but after it so it can access all the points once they have been generated

        # ax.plot(xComponent,yComponent,zComponent, color=currentJson["data"]["colour"], linestyle= lineType)
        # ax.scatter(xComponent,yComponent,zComponent, color=currentJson["data"]["colour"])

candidateVerticies = []
candidateEdges = []

for x in xPoints:
    for y in yPoints:
        for z in zPoints:
            ax.scatter([x],[y],[z],color='black')
            candidateVerticies.append([x,y,z])

print(jsonFiles)

print(len(candidateVerticies))
plt.show()