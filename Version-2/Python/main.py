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
            outputPt.append(int(Orientation[i]))

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

        # ax.plot(xComponent,yComponent,zComponent, color=currentJson["data"]["colour"], linestyle= lineType)
        # ax.scatter(xComponent,yComponent,zComponent, color=currentJson["data"]["colour"])

for key in jsonFiles:
    currentJson = jsonFiles[key]
    viewsData.update({key: {}})
    for linetype in ["solid", "hidden", "center"]:

        viewsData[key].update({linetype:{"lines":set(), "verticies": set()}})

        for i in range(len(currentJson["lines"])):
            if currentJson["lines"][i]["line_type"] == linetype:
                viewsData[key][linetype]["verticies"].add(tuple(convertXYAndOrientationToXYZ([currentJson["lines"][i]["X1"], currentJson["lines"][i]["Y1"]], currentJson["data"]["orientation"])))
                viewsData[key][linetype]["verticies"].add(tuple(convertXYAndOrientationToXYZ([currentJson["lines"][i]["X2"], currentJson["lines"][i]["Y2"]], currentJson["data"]["orientation"])))
                
print(viewsData)

# print(viewsData['front']['solid']['verticies'][1][0])



for viewKey in viewsData:
    for linetypeKey in ["solid", "hidden", "center"]:
        for point3D in viewsData[viewKey][linetypeKey]["verticies"]:
            match linetypeKey:
                case "solid":
                    colour = "red"
                case "hidden":
                    colour = "blue"
                case "center":
                    colour = "green"

            ax.scatter(point3D[0],point3D[1],point3D[2],color=colour)

            # print(point3D[0],point3D[1],point3D[2])


candidateVerticies = []
candidateEdges = []

for x in xPoints:
    for y in yPoints:
        for z in zPoints:
            # ax.scatter([x],[y],[z],color='black')
            candidateVerticies.append([x,y,z])

# print(jsonFiles)

# print(len(candidateVerticies))

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()