# Fusion Scripts

This repository provides a collection of utilities and add-in scripts designed to enhance Autodesk Fusion's functionality. These scripts, all written in Python, help automate tasks, improve workflow efficiency, and facilitate advanced customization within the Fusion environment.

> [!NOTE]
> This project includes affiliate links. If you click on these links, I may earn a commission or credit. This does not cost you anything extra, but it helps support the project and future development efforts. Thank you for your support!

## BOM Scripts

The following scripts are designed to create a more accurate bill of materials (BOM).

### [export-bom](src/export-bom/export-bom.py)

This script generates a BOM from the root component.
The output is a markdown file containing the BOM, with images stored in an `images` folder.

### [add-bb-attribute](src/add-bb-attribute/add-bb-attribute.py)

This script is a helper for the Export BOM script.
When this attribute is set to true, the component is exported with its dimensions automatically, based on the physical bounding box.
Handy for say wood parts!
It adds an attribute to the selected component with the following parameters:

- **groupName:** `exportBom`
- **name:** `boundingBox`
- **value:** `True`

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

### [update-partnumbers](src/update-partnumbers/update-partnumbers.py)

> [!WARNING]
This one may or may not work any more. After a Fusion update, it appears copy/paste does not result in components with the index in parenthesis.

This script is a helper for the Export BOM script. When parts are pasted using "Paste New" in Fusion, they receive a name with an appended index (e.g., `Component (1)`). This causes the BOM to treat them as separate items. This script finds such indexed parts and assigns a common non-indexed name to the part number attribute, ensuring that identical parts are grouped together in the BOM with a proper quantity count.

### [attribute-editor](src/attribute-editor/attribute-editor.py)

This script provides a manual way to edit attributes in a Fusion assembly. Attributes are hidden group/name/value sets used in Fusion assemblies. The script allows users to undo changes made by other scripts or add custom attributes for other purposes.

## Installation

To install the scripts, copy the contents of the `src/` directory to the following locations:

> [!NOTE]
> I am only familiar with Windows. If anyone else knows the correct way to do this on macOS or Linux, please update and submit a PR.

- **Windows:** `C:\Users\<username>\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts\`
- **macOS:** `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`
  - **Note:** If Fusion 360 was installed via the Mac App Store, the path may be:
    `~/Library/Containers/com.autodesk.mas.fusion360/Data/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`
- **Linux:** Autodesk Fusion 360 does not officially support Linux. However, if running through Wine, the installation path depends on the Wine configuration.

### Additional Steps

1. **Accessing the Scripts and Add-Ins Manager:**

   - Launch Fusion 360.
   - Navigate to the "Tools" tab.
   - Click on "Scripts and Add-Ins."

2. **Running a Script:**

   - In the "Scripts" tab, locate the script you want to run.
   - Select it and click "Run."

For more information, refer to Autodesk's official documentation: [help.autodesk.com](https://help.autodesk.com/view/fusion360/ENU/)

## Sample BOMs

Below are three sample Bill of Materials (BOMs) generated using the `export-bom` script. These examples demonstrate different use cases and formats that can be generated.

1. **[4 Cabinet Counter](sample-boms/4-cabinet-counter/4-cabinet-counter-bom.md):** A simple set of utility drawers and counter for a hobby shop. The full project for these can be found at [/tallman5/diy-utility-drawers](https://github.com/tallman5/diy-utility-drawers).
1. **[Voron v2.4 R2](sample-boms/voron-2.4-r2/voron-2.4r2-bom.md):** A CoreXY 3D printer
1. **[Others](sample-boms/):** Some other BOMs from existing projects.

Each sample BOM includes images and part details to illustrate the output format and help users understand how the script structures data.

# License
Fusion Scripts © 2023-2025 by Joseph McGurkin is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1)


<img style="height:22px!important;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="">&nbsp;<img style="height:22px!important;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="">&nbsp;<img style="height:22px!important;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt="">&nbsp;<img style="height:22px!important;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt="">
