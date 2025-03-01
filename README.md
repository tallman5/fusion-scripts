# Fusion Scripts
This repository provides a collection of utilities and add-in scripts designed to enhance Autodesk Fusion's functionality. These scripts, all written in Python, help automate tasks, improve workflow efficiency, and facilitate advanced customization within the Fusion environment.

## BOM Scripts
The following scripts are designed to create a more accurate bill of materials (BOM).

### [add-ignore-attribute](src/add-ignore-attribute/add-ignore-attribute.py)
This script is a helper for the Export BOM script. It ensures that assemblies with the ignore attribute set to `true` will not be exported as part of the BOM. It adds an attribute to the selected component with the following parameters:

- **groupName:** `exportBom`
- **name:** `ignore`
- **value:** `True`

### [add-single-attribute](src/add-single-attribute/add-single-attribute.py)
This script is a helper for the Export BOM script. It is useful for assemblies that contain multiple sub-components but should be treated as a single unit in the BOM. For example, a Raspberry Pi assembly with a board and connectors may be considered as one entity in the BOM.

It adds an attribute to the selected component with the following parameters:

- **groupName:** `exportBom`
- **name:** `isSingleAssembly`
- **value:** `True`

### [export-bom](src/export-bom/export-bom.py)
This script generates a BOM from the root component. The output is a markdown file containing the BOM, with images stored in an `images` folder.

### [update-partnumbers](src/update-partnumbers/update-partnumbers.py)
This script is a helper for the Export BOM script. When parts are pasted using "Paste New" in Fusion, they receive a name with an appended index (e.g., `Component (1)`). This causes the BOM to treat them as separate items. This script finds such indexed parts and assigns a common non-indexed name to the part number attribute, ensuring that identical parts are grouped together in the BOM with a proper quantity count.

### [attribute-editor](src/attribute-editor/attribute-editor.py)
This script provides a manual way to edit attributes in a Fusion assembly. Attributes are hidden group/name/value sets used in Fusion assemblies. The script allows users to undo changes made by other scripts or add custom attributes for other purposes.

## Installation

> [!NOTE]
> I am only familiar with Windows. If anyone else knows the correct way to do this on macOS or Linux, please update and submit a PR.

To install the scripts

1. Copy the contents of the `src/` directory to the following locations:
   1. **Windows:** `C:\Users\<username>\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts\`
   1. **macOS:** `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`
      1. **Note:** If Fusion 360 was installed via the Mac App Store, the path may be:
    `~/Library/Containers/com.autodesk.mas.fusion360/Data/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`
   1. **Linux:** Autodesk Fusion 360 does not officially support Linux. However, if running through Wine, the installation path depends on the Wine configuration.
1. In each of the folders, rename `.env.sample` to `.env`.
1. Update the paths in the `.env` files.

### Additional Steps

1. **Accessing the Scripts and Add-Ins Manager:**
   1. Launch Fusion 360.
   1. Navigate to the "Tools" tab.
   1. Click on "Scripts and Add-Ins."
1. **Running a Script:**
   1. In the "Scripts" tab, locate the script you want to run.
   1. Select it and click "Run."
