#Author-tallman5
#Description-Adds a boundingBox = true attribute to the active component for use with the Export BOM script. This tells the script to export the w x h x d dimensions.

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        product = app.activeProduct

        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('Please change to MODEL workspace and try again.')
            return

        activeComponent = design.activeComponent
        attributes = activeComponent.attributes

        attributeAdded = False

        for attribute in attributes:
            if attribute.groupName == 'exportBom':
                if attribute.name == 'boundingBox':
                    attribute.value = 'True'
                    attributeAdded = True
        
        if attributeAdded == False:
            attributes.add('exportBom', 'boundingBox', 'True')

        ui.messageBox('Done!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
