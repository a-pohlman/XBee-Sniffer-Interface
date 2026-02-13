# XBee Sniffer Interface
## Description
A GUI application used to read any packets in a given network using XBee radio modules. Originally desinged for the C-ARQ research project at Ohio Northern University, a lightweight and unique application that takes the hassle out of using a boring terminal line. With a easy to navigate user interface, it makes the process of starting and running new tests straightforward. 

## Version 0.2.5-beta
The current release of the application as of **02/13/2026.** This will be the first instalment of the application. Development may or may not continue in the future. It all depends on if the project needs more updates and features. Since this is the first version to be released, there are no bug updates or reports to be made as of this time. Read the below footer notes for the section to view any additional information needed.

> [!WARNING]
> The app was developed in tested using Python 3.13 enviornment. If using the Python Version, and not an exectuable, it is recommended to have a Python interperter 3.10 and higher.

> [!IMPORTANT]
> The only XBee radio devices that were used to test on when devleoping the app were the XBee S2C radios. It may be possible that the app does not work with all XBee radio modules.

## Setting Up
There are currently different ways to set up the application for various different systems. Currently there are only two exectuables available for Windows 11 and Debian / Ubuntu systems. These are the easiest, and most reliable in terms of setting up and getting started with using the application. If your system can not use one of these, then, you can try and use the Python Version as well. By default, the repository is set up to default to the Windows branch since it's the most common system. Unix systems will have to switch the branch on the repository to the version wanted. 
### Exectuable Versions
1. Start by downloading the Github in whatever way you like (Whether it be the zip folder or cloning the repository)
2. Navigate to the folder you just downloaded
3. Extract the folder
4. Navigate into the extracted folder
5. Extract the bin folder
6. Once completed, then navigate into the bin folder
7. At this point, whether on Windows 11 or Debian, you should find a file called 'xsi.exe' or 'xsi'
8. Double click on this file to run the program

That's it! You can create a shortcut of this file and store it on your system's desktop if you wish, but this is how you can run the application. 

> [!CAUTION]
> It's important that you do not move any files or folders outside of the bin folder as this can and will cause the application to freeze and crash!

> [!IMPORTANT]
> Inside the bin folder, you will also find a folder named 'cache.' When running tests with the 'default' path, this is where it will automatically store those files.

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
> To check if the modules were installed correctly, run the following commands:
> 

   

   
   
