# XBee Sniffer Interface
## Description
A GUI application used to read any packets in a given network using XBee radio modules. Originally desinged for the [C-ARQ research](https://github.com/a-pohlman/C-ARQ-Research) project at [Ohio Northern University](https://onu.edu), a lightweight and unique application that takes the hassle out of using a longwinded terminal script. With a easy to navigate user interface, it makes the process of starting and running new tests straightforward. 

## Features
- Easy to use user interface
- Better file management
- Easy configurations for testing
- Allows both .txt and .csv files
- Auto ends with specified string
- Statistics frame to show testing info
- Tracks progress during testing
- Supports different themes

## Version 0.2.5 
**Outdated** release of the application from **02/14/2026.** Please see the newest release XSI_0.3.0 by using the github branches for the most up-to-date version. 

> [!WARNING]
> The app was developed and tested using Python 3.13 enviornment. If using the Python Version, and not an exectuable, it is recommended to have a Python interperter 3.10 and higher.

> [!IMPORTANT]
> The only XBee radio devices that were used to test on when devleoping the app were the XBee S2C radios. It may be possible that the app does not work with all XBee radio modules.

## Setting Up
There are two different ways to still install this version if wanted. The first way is to use the Python version, the other is by using a legacy exectuable packaged into a setup wizard for Windows 11. Please review the below sections to see how to install them.

### Exectuable Versions
1. Start by going to the releases tab on the right, and clicking on the version of XSI you want (available: XSI_0.2.5 | XSI_0.3.0)
2. Once downloaded, you should have a file called 'xsi_[VERSION]_setup.exe'
3. Double click or run the executable to start the setup wizard
4. Follow the on screen prompts
5. Wait for it to download

That's it! Assuming you checked the box for a desktop shortcut, you can now run the XSI application. 

### Python Version
1. Start by downloading the Github in whatever way you like (Whether it be the zip folder or cloning the repository)
2. Navigate to the folder you just downloaded
3. Extract the folder
4. Next, you'll need to install the correct modules for your Python interperter
   > NOTE: It's assumed that you already have a Python interperter downloaded if installing this verison. If you don't have one, download one before continuing forward.

   For the modules, go to your systems terminal, and type in the following commands one at a time:
   ```powershell
   pip install customtkinter pyserial pillow
   ```

> [!TIP]   
> To check if the modules were installed correctly, in the same terminal type `python` and run the following code:
> ```python
> import customtkinter
> import serial
> import pillow # For Windows 11 systems only
> ```

5. After verifying that the appropriate modules have been installed, navigate inside the folder you extracted from earlier
7. Navigate inside the bin folder
8. You'll find a file called 'xsi.pyw'
9. There are two options two running this file. If your in Windows, right click on it and slect Python. Otherwise, you can run the file using your systems terminal.

Assuming everything went correctly, you should have a working version of XSI using python!

### WARNINGS
> [!CAUTION]
> It's important that you do not move any files or folders outside of the bin folder as this can and will cause the application to freeze and crash!

> [!WARNING]
> In its current state for the Windows 11 executable, it is recommended not to store XSI in 'Program Files' folder as it has been known to crash and cannot save data in the default cache folder. Instead it is recommended to keep the program anywhere in the users files.

> [!IMPORTANT]
> Inside the bin folder, you will also find a folder named 'cache.' When running tests with the 'default' path, this is where it will automatically store those files.

## Help
If you want to know how the app works, a PDF has been provided that will give all the knowledge needed on how to use the app. Navigate into the bin folder, and you should see a PDF labeled, 'help.pdf.' For your convience, the app also has a help button that you can click to open the PDF directly. For any issues with the app or if something is bugged, please feel free to use the issues tab to report them. 
