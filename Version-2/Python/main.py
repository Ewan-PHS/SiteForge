import json
from zipfile import ZipFile
import math
import matplotlib.pyplot as plt
from pathlib import Path

from flask import views

##########################################################################

def setXYZComponents(Input, Index):
    if Input["data"]["orientation"][Index] == "x":
        varToSet = [Input["lines"][i]['X1'], Input["lines"][i]['X2']]
    elif Input["data"]["orientation"][Index] == "y":
        varToSet = [Input["lines"][i]['Y1'], Input["lines"][i]['Y2']]
    elif Input["data"]["orientation"][Index] == "0":
        varToSet = [0,0]
    
    return varToSet

def convertXYAndOrientationToXYZ(InputPt, Orientation):
    # Input point formatted as [X, Y]
    ptX, ptY = InputPt

    outputPt = []

    for i in range(len(Orientation)):
        if Orientation[i] == "x":
            outputPt.append(ptX)
        elif Orientation[i] == "y":
            outputPt.append(ptY)
        else:
            outputPt.append(Orientation[i])

    return outputPt

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

viewsData = {} # formatted as {viewname: {linetype: {lines: [], verticies: [] } } }

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

        xComponent = setXYZComponents(currentJson, 0)
        yComponent = setXYZComponents(currentJson, 1)
        zComponent = setXYZComponents(currentJson, 2)

        xPoints = list(set(xPoints) | set(xComponent))
        yPoints = list(set(yPoints) | set(yComponent))
        zPoints = list(set(zPoints) | set(zComponent))

        # viewsData.update({key: {currentJson["lines"][i]["linetype"]: {"verticies": [[]]}}}) this is bad, it needs to be outside these loops in another loop like this one but after it so it can access all the points once they have been generated

        # ax.plot(xComponent,yComponent,zComponent, color=currentJson["data"]["colour"], linestyle= lineType)
        ax.scatter(xComponent,yComponent,zComponent, color=currentJson["data"]["colour"])

for key in jsonFiles:
    currentJson = jsonFiles[key]
    viewsData.update({key: {}})
    for linetype in ["solid", "hidden", "center"]:

        viewsData[key].update({linetype:{"lines":[], "verticies": []}})

        for i in range(len(currentJson["lines"])):
            if currentJson["lines"][i]["line_type"] == linetype:
                viewsData[key][linetype]["verticies"].append(convertXYAndOrientationToXYZ([currentJson["lines"][i]["X1"], currentJson["lines"][i]["Y1"]], currentJson["data"]["orientation"]))
                viewsData[key][linetype]["verticies"].append(convertXYAndOrientationToXYZ([currentJson["lines"][i]["X2"], currentJson["lines"][i]["Y2"]], currentJson["data"]["orientation"]))
                
            # print(viewsData)
            # viewsData[key][linetype]["verticies"].append([setXYZComponents(currentJson, 0), setXYZComponents(currentJson, 1), setXYZComponents(currentJson, 2)])

print(viewsData)

candidateVerticies = []
candidateEdges = []

for x in xPoints:
    for y in yPoints:
        for z in zPoints:
            # ax.scatter([x],[y],[z],color='black')
            candidateVerticies.append([x,y,z])

# print(jsonFiles)

# print(len(candidateVerticies))
plt.show()