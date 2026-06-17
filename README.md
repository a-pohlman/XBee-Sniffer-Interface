<p align="center">
  <img src="images/xsi_git_logo.png" alt="Alternate Text" width="500">
</p>

# XBee Sniffer Interface
## Description
A GUI application used to read any packets in a given network using XBee radio modules. Originally desinged for the [C-ARQ research](https://github.com/a-pohlman/C-ARQ-Research) project at [Ohio Northern University](https://onu.edu), a lightweight and unique application that takes the hassle out of using a longwinded terminal script. With a easy to navigate user interface, it makes the process of starting and running new tests straightforward. 

## Features
- Intuitive interface
- Better file management
- Easy configurations for testing
- Allows both .txt and .csv files
- Auto ends with specified string
- Auto ends with packet count (*New)
- Tracks progress during testing
- Supports different themes
- Has the ability to make custom tests (*New)
- Time Estimator (*New)

## Version 0.3.0
The current release of the application as of **06/16/2026.** This version of the application has had a major UI overhaul, completing changing how the app looks and feels. As well as this, other known features have had quality or bug fixes to them. 
> [!WARNING]
> The app was developed and tested using a Python 3.14 enviornment. If using the Python Version, and not an exectuable, it is recommended to have a Python interperter 3.10 and higher.

> [!IMPORTANT]
> The only XBee radio devices that were used to test on when developing the app were the XBee S2C radios. It may be possible that the app does not work with all XBee radio modules! If this happens please report this to the issues tab with your error.

## Setting Up
There are different ways to setup and run the application. Differenet versions of the application exsist, such as the exectuable version, or the Python version. Follow the steps below in order to install the version that you want!

### Windows 11 Exectuable Versions
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
> import pillow
> ```

5. After verifying that the appropriate modules have been installed, navigate inside the folder you extracted from earlier
7. Navigate inside the bin folder
8. You'll find a file called 'xsi.pyw'
9. There are two options two running this file. If your in Windows, right click on it and slect Python. Otherwise, you can run the file using your systems terminal.

Assuming everything went correctly, you should have a working version of XSI using python!

### NOTES & WARNINGS
> [!IMPORTANT]
> Inside the bin folder, you will also find a folder named 'cache.' When running tests with the 'default' path, this is where it will automatically store those files.

> [!CAUTION]
> It's important that you do not move any files or folders outside of the bin folder as this can and will cause the application to freeze and crash!

> [!WARNING]
> In its current state for the Windows 11 executable, it is recommended not to store XSI in 'Program Files' folder as it has been known to crash and cannot save data in the default cache folder. Instead it is recommended to keep the program anywhere in the users files.

## Help
If you want to know how the app works, a PDF has been provided that will give all the knowledge needed on how to use the app. Navigate into the bin folder, and you should see a PDF labeled, 'help.pdf.' For your convience, the app also has a help button that you can click to open the PDF directly. For any issues with the app or if something is bugged, please feel free to use the issues tab to report them. 
