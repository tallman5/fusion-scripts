# Author: tallman#9584 on Discord
# Description:
#   This script creates a BOM from the root component. 
#   Output is a markdown file with images in an images folder.
# Notes:
#   Yes, there are solutions which simply iterate through the root component's all occurrences.
#   This scripts adds some more robust features:
#   1. Child and grand child linked assemblies - 
#      Simply going through all occurrences will not include the grandchildren
#   2. Single Assemblies - 
#      Using a Raspberry Pi assembly as an example, it may be comprised of many smaller components.
#      However, in the BOM it should be just a single line.
#      Use the add-single-assembly-attribute.py script to tag any assembly or component as single.
#   3. Ignoring Assemblies - 
#      If there's something in the assembly which shouldn't be in the BOM
#      Use the attribute-editor.py script to tag any assembly or component as single.

import adsk.core, adsk.fusion, traceback, urllib, re

def createSafeFilename(inputString):
    # Define the characters to be replaced with a dash
    invalidChars = r'[\\/:*?"<>|\s]'
    # Replace invalid characters with dash
    safeString = (re.sub(invalidChars, '-', inputString)).lower()
    # Ensure the file name is not empty
    return safeString if safeString else "default_filename"
    
def toggleChildren(occ, newValue, recursive):
    occ.isLightBulbOn = newValue
    occ.component.isLightBulbOn = newValue
    for body in occ.bRepBodies:
        body.isLightBulbOn = newValue
    if recursive == True:
        for child in occ.childOccurrences:
            toggleChildren(child, newValue, recursive)

def processOccs(occs, dialog, bom, viewPort, imagesFolder):
    if dialog.wasCancelled:
        return
    for occ in occs:
        processOcc(occ, dialog, bom, viewPort, imagesFolder)

def processOcc(occ, dialog, bom, viewPort, imagesFolder):
    if dialog.wasCancelled:
        return
    
    inBom = False
    ignorePart = False
    isSingleAssembly = False
    partNumber = occ.component.partNumber

    for attr in occ.component.attributes:
        if attr.groupName == 'exportBom':
            if attr.name == 'isSingleAssembly' and attr.value == 'True':
                isSingleAssembly = True
            if attr.name == 'ignore' and attr.value == 'True':
                ignorePart = True

    if not ignorePart:
        if isSingleAssembly or occ.component.bRepBodies.count > 0:
            for bomItem in bom:
                if bomItem['partNumber'] == partNumber:
                    bomItem['instances'] += 1
                    inBom = True
                    break

            if not inBom:
                toggleChildren(occ, True, isSingleAssembly)

                viewPort.fit()
                imageFileName = f"{createSafeFilename(partNumber)}.png"
                # imagePath = urllib.parse.quote("images/" + imageFileName)
                filePath = f"{imagesFolder}{imageFileName}"   # "{}{}.png".format(imagesFolder, partNumber)
                viewPort.saveAsImageFile(filePath, 100, 100)
                bom.append({
                    'imagePath': filePath,
                    'partName': occ.name,
                    'partNumber': partNumber,
                    'instances': 1,
                    'material': '',
                    'description': occ.component.description,
                })

            toggleChildren(occ, False, True)

    if isSingleAssembly == False:
        occ.isLightBulbOn = True
        processOccs(occ.childOccurrences, dialog, bom, viewPort, imagesFolder)

    dialog.progressValue = dialog.progressValue + 1

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        viewPort = app.activeViewport
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('No active Fusion design', 'No Design')
            return
        rc = design.rootComponent
        allOccs = rc.allOccurrences
        rcOccs = rc.occurrences
        userCancelled = False
        bomList = []

        bomFolder = "C:\\Temp\\bom\\"
        folderDialog = ui.createFolderDialog()
        folderDialog.title = "Selcect a folder for the BOM"
        dialogResult = folderDialog.showDialog()
        if dialogResult == adsk.core.DialogResults.DialogOK:
            bomFolder = folderDialog.folder + "\\"
        else:
            return
        imagesFolder = bomFolder + "images\\"

        # If grid is on, temporarily turn off
        turnedOffGrid = False
        cmdDef = ui.commandDefinitions.itemById('ViewLayoutGridCommand')
        listCntrlDef = adsk.core.ListControlDefinition.cast(cmdDef.controlDefinition)
        layoutGridItem = listCntrlDef.listItems.item(0)
        if layoutGridItem.isSelected:
            layoutGridItem.isSelected = False
            turnedOffGrid = True

        occDialog = ui.createProgressDialog()
        occDialog.cancelButtonText = 'Cancel'
        occDialog.isBackgroundTranslucent = False
        occDialog.isCancelButtonShown = True

        occDialog.show('Step 1 of 3: Hiding everything...', '%p percent complete, component %v of %m', 0, allOccs.count, 1)
        for occ in allOccs:
            if occ.isLightBulbOn == True:
                occ.isLightBulbOn = False
            for body in occ.bRepBodies:
                if body.isLightBulbOn == True:
                    body.isLightBulbOn = False
            occDialog.progressValue = occDialog.progressValue + 1
            if occDialog.wasCancelled:
                userCancelled = True
                break
        occDialog.hide()

        if userCancelled == False:
            occDialog.show('Step 2 of 3: Exporting images...', '%p percent complete, component %v of %m', 0, allOccs.count, 1)
            processOccs(rcOccs, occDialog, bomList, viewPort, imagesFolder)

        # Get root image for BOM
        sels = ui.activeSelections
        sels.clear()
        sels.add(rc)
        app.executeTextCommand('Commands.Start ShowAllComponentsCmd')
        app.executeTextCommand('Commands.Start ShowAllBodiesCmd')
        sels.clear()
        viewPort.fit()
        startImagePath = imagesFolder + createSafeFilename(rc.partNumber) + ".png"
        viewPort.saveAsImageFile(startImagePath, 200, 200)
        
        if len(bomList) > 0:
            occDialog.show('Step 3 of 3: Generating BOM...', '%p percent complete, component %v of %m', 0, len(bomList), 1)

            mdText = "# " + rc.partNumber + " BOM\n"
            mdText += "![](images/" + createSafeFilename(rc.partNumber) + ".png)\n"
            mdText += "|Image|Name|Number|Description|Quantity|\n|-|-|-|-|-|"
        
            bomList.sort(key=lambda x: (x['partName'].casefold(), x))
            for bomItem in bomList:
                mdText = mdText + "\n|![](" + bomItem['imagePath'] + ")|" + bomItem['partName'] +  "|" + bomItem['partNumber'] +  "|" + bomItem['description'] + "|" + str(bomItem['instances']) + "|"
                occDialog.progressValue = occDialog.progressValue + 1
                if occDialog.wasCancelled:
                    userCancelled = True
                    break

            if userCancelled == False:
                mdPath = f"{bomFolder}\\{createSafeFilename(rc.partNumber + " BOM")}.md"
                with open(mdPath, "w") as outputFile:
                    outputFile.writelines(mdText)

        if turnedOffGrid == True:
            layoutGridItem.isSelected = True
        occDialog.hide()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        