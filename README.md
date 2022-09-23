# Windows Power Plan Vertical Scaler

## Power Plan Automatic Switch
Power Plan Auto Switch is a windows power manager based in python coding to automatically switch your power plans according to CPU needs.
Its focus, is to balance the necessity of resources with the usage of applications.

### 1. Pre requisites:
  - Python (version 3).
  - pystray (python library).
  - PIL (python library).

### 2. Installation:
  - Install python.
  - Install libraries.
  - Add to task scheduler to run at log on the python file.

### 3. Notes:
  - The script depends to power plans name in your system.
  - the script only swtiches to a high performance power plan if CPU usage is above 40% and sets it back to the normal power plan when bellow 40%.
