## -----------------------------------------------------
## Python Logic for a (Very Simple) File Explorer
## -----------------------------------------------------
init python:

    # imports
    import os
    import re
    import shutil
    import string
    import time

    # configuration, edit as necessary
    # NOTE: please see the README for more information on these settings
    FILE_EXPLORER_CONFIG = {

        # these are the colours of the file explorer
        "colors": {
            "background": "#1E1E2E",
            "frame_background": "#252535",
            "grid_background": "#222235",
            "folder_background": "#333355",
            "file_background": "#2A2A4E",
            "text_color": "#FFFFFF",
            "button_hover": "#555555",
            "exit_text": "#FF5555",
            "exit_button": "#550000",
            "exit_hover": "#770000"
        },

        # these are the icons used in the file explorer
        "icons": {
            "drive": "💾",
            "folder": "📁",
            "file": "📄",
            "up": "⬆️",
            "go": "->",
            "exit": "x"
        },

        # these are the text settings for the file explorer
        "language": {
            "selected_file": "Selected file:", # the label for the selected file
            "choose_file": "Choose File", # the text for the "Choose File" button
            "favourites": "Favourites", # the label for the favourites section
            "up": "Go Up", # the label for the "Up" button
        },

        # the favourite folders for the file explorer
        "favourites": {
            # use this format: "Name": "Path"
            "Game Directory": renpy.config.gamedir, # the game directory
            "Desktop": os.path.expanduser("~\Desktop"), # the desktop folder
            "Documents": os.path.expanduser("~\Documents"), # the documents folder
            "Pictures": os.path.expanduser("~\Pictures"), # the pictures folder
            "Music": os.path.expanduser("~\Music"), # the music folder
            "Downloads": os.path.expanduser("~\Downloads"), # the downloads folder
        },

        # these are the settings for the file explorer
        "explorer": {
            "accept_types": { "all" }, # if not "all", only show files with these extensions (ex. { "png", "jpg", "jpeg" })
            "starting_directory": os.path.expanduser("~\Desktop"), # the starting directory for the file explorer
        },

    }

    # adjust font size in the file explorer based on the length of the text
    def get_dynamic_font_size(text, base_size=18):
        length = len(text)
        if length <= 10:
            return base_size
        elif length <= 15:
            return base_size - 2
        elif length <= 20:
            return base_size - 4
        else:
            return base_size - 6  # for very, very long text

    # truncate the directory if it is too long
    def truncate_directory(directory, max_length=50):
        if len(directory) > max_length:
            return "..." + directory[-max_length:]
        return directory

    # define the file explorer class
    class FileExplorer:

        # initialize the file explorer
        def __init__(self, start_dir=None):
            self.current_dir = start_dir or os.path.expanduser("~\Desktop") # the current directory (ex. starting directory)
            self.truncated_dir = truncate_directory(self.current_dir) # the truncated directory for display
            self.files = [] # list of all files in the current directory
            self.folders = [] # list of all folders in the current directory
            self.drives = [] # list of all drives on the system, if the root is selected
            self.root = False # if true, show drives instead of folders 
            self.selected_file = None # the file that is currently selected
            self.update_file_list() # load the starting directory

        # check if the current directory is the top level (ex. C:\ on Windows, / on Linux)
        def is_top_level(self):
            if os.name == "nt":
                return re.match(r"^[A-Z]:\\$", self.current_dir, re.IGNORECASE) is not None
            return self.current_dir == "/"

        # get the drives on the system for when the root is selected
        def get_drives(self):
            # checking for drives on windows (using the string.ascii_uppercase to get A-Z and test their availability)
            if os.name == 'nt':
                drives = []
                for letter in string.ascii_uppercase:
                    drive = f"{letter}:\\"
                    if os.path.exists(drive):
                        drives.append(drive)
                return drives
            # checking for drives on linux and macOS (stored in /mnt, /media, and /Volumes)
            elif os.name == 'posix': 
                drives = []
                if os.path.isdir("/mnt"): # Linux (typically)
                    drives.extend([os.path.join("/mnt", d) for d in os.listdir("/mnt") if os.path.isdir(os.path.join("/mnt", d))])
                if os.path.isdir("/media"): # Linux (sometimes)
                    drives.extend([os.path.join("/media", d) for d in os.listdir("/media") if os.path.isdir(os.path.join("/media", d))])
                if os.path.isdir("/Volumes"): # macOS
                    drives.extend([os.path.join("/Volumes", d) for d in os.listdir("/Volumes") if os.path.isdir(os.path.join("/Volumes", d))])
                return drives
            return []

        # filtering out files that we do not want to show (ex. system files, hidden files, cache)
        def should_ignore_item(self, item):

            # we do not want these
            disallowed_prefixes = { "$", "." }
            disallowed_extensions = { "ini", "db", "db-journal", "lnk", "tmp", "temp", "bak", "swp" }
            disallowed_names = { "thumbs.db", "system volume information", "tmp", "recovery" }

            # if file starts with <x>, hide
            for prefix in disallowed_prefixes:
                if item.startswith(prefix):
                    return True
            
            # if file ends with <x>, hide
            for ext in disallowed_extensions:
                if item.lower().endswith(f".{ext}"):
                    return True

            # if file is in the disallowed names list, hide
            if item.lower() in disallowed_names:
                return True

            #  if file has a tag, hide (renpy will bork if it reads this)
            tag_pattern = re.compile(r"{.*?}")
            if tag_pattern.search(item):
                return True

            # custom filtering, if desired (either "all" and we do nothing or filter by a list of extensions)
            if FILE_EXPLORER_CONFIG["explorer"]["accept_types"] != { "all" }:
                allowed_extensions = FILE_EXPLORER_CONFIG["explorer"]["accept_types"]
                if not any(item.lower().endswith(f".{ext}") for ext in allowed_extensions):
                    return True

            return False

        # update the file (and folder, or drive) list for the current directory
        def update_file_list(self):
            self.drives = []
            self.folders = []
            self.files = []
            if self.root:
                # only get roots here
                self.drives = self.get_drives()
            else:
                try:
                    # get the list of items in the current directory
                    items = os.listdir(self.current_dir)

                    # go through each item
                    for item in items:

                        # get the full path of the item, filter
                        item_path = os.path.join(self.current_dir, item)
                        # Don't ignore directories; file might be in subdirectory
                        if self.should_ignore_item(item) and os.path.isfile(item_path):
                            continue

                        # check if the item is a folder or a file
                        if os.path.isdir(item_path):
                            try:
                                if os.access(item_path, os.R_OK):
                                    self.folders.append(item)
                            except PermissionError:
                                print(f"Permission error with folder: {item_path}")
                        elif os.path.isfile(item_path):
                            try:
                                if os.access(item_path, os.R_OK):
                                    self.files.append(item)
                            except PermissionError:
                                print(f"Permission error with file: {item_path}")
                except Exception as e:
                    print(f"Error loading directory: {e}")
                    self.files, self.folders = [], []

        # navigate to a folder
        def navigate_to(self, folder):
            if self.root:
                return
            new_path = os.path.join(self.current_dir, folder)
            if os.path.isdir(new_path) and os.access(new_path, os.R_OK):
                self.current_dir = new_path
                self.truncated_dir = truncate_directory(self.current_dir)
                self.update_file_list()

        # set the file explorer's directory to a different drive
        def jump_drive(self, drive):
            if not drive.endswith("\\"):  
                drive += "\\"
            if os.path.exists(drive):
                self.root = False
                self.current_dir = drive
                self.truncated_dir = truncate_directory(self.current_dir)
                self.update_file_list()

        # go up a directory (ex. cd ..)
        def go_up(self):
            parent = os.path.dirname(self.current_dir)
            if self.is_top_level():
                self.root = True
                self.update_file_list()
            else:
                if parent and os.path.exists(parent):
                    self.current_dir = parent
                    self.truncated_dir = truncate_directory(self.current_dir)
                    self.update_file_list()

        # select a file (not actually choose it yet)
        def select_file(self, filename):
            full_path = os.path.join(self.current_dir, filename)
            if os.path.isfile(full_path):
                self.selected_file = full_path

        # reset the file explorer's selection (ex. when closing the file explorer)
        def reset_selection(self):
            self.selected_file = None
            self.current_dir = os.path.expanduser("~\Desktop")

        # navigate to the currently typed directory
        def navigate_to_directory(self, directory):
            if os.path.isdir(directory) and os.access(directory, os.R_OK):
                self.current_dir = directory
                self.truncated_dir = truncate_directory(directory)
                self.update_file_list()

        # the actual action that happens when a file is chosen
        def choose_file(self, filename):
            global full_path
            base_filename = os.path.basename(filename) # just the file name
            full_path = os.path.join(self.current_dir, filename) # the full file path
            # return full_path


    # create an instance of the file explorer
    file_explorer = FileExplorer()

init python:
    # Example file handler for chosen file; check and hand-off
    def FileActionHandler(chosen_file):
        if(chosen_file != None):
            CopyMCAvatar(chosen_file, dest_file)
        else:
            renpy.call_screen("ModalWarning", "Filename cannot be None")

    # Copy avatar to destination
    # dest_file is global defined in script.rpy
    def CopyMCAvatar(src_file, dest_file):
        shutil.copyfile(src_file, dest_file)

# Display screen to show size, warning to quit and restart game
screen ModalWarning(warningMsg):
    modal True
    zorder 101

    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        vbox:
            xalign 0.5
            text warningMsg
            text ""
            textbutton "Close":
                xalign 0.5
                action Hide()


## -----------------------------------------------------
## Ren'Py Screen for a (Very Simple) File Explorer
## -----------------------------------------------------
screen file_explorer_screen():
    # screen properties
    modal True
    zorder 100

    # temporary variables to track explorer state
    default directory_input = file_explorer.current_dir
    default directory_is_editable = False 

    on "show" action Show("ModalWarning", warningMsg="Image size needs to be 200 x 324\nYou need to quit the game and restart for avatar to work correctly")

    # the explorer screen itself
    frame:
        xsize 1250
        ysize 650
        background FILE_EXPLORER_CONFIG["colors"]["background"]
        padding (15, 15)
        align (0.5, 0.5)

        # it's actually a stack of horizontal layers (top row, centre, bottom row)
        vbox:
            spacing 10
            xsize 1200
            xfill True

            frame:
                xfill True
                ysize 50
                background FILE_EXPLORER_CONFIG["colors"]["background"]
                padding (10, 10)

                # top row with the directory input and navigation buttons
                hbox:
                    spacing 5
                    xfill True

                    frame:
                        background FILE_EXPLORER_CONFIG["colors"]["frame_background"]
                        padding (5, 5)
                        xsize 1125
                        ysize 40
                        xpos -0.010

                        button:
                            xsize 1000
                            ysize 40
                            xpos 0
                            ypos -12
                            # toggle directory_is_editable when clicked (button takes up MOST of the frame)
                            action [SetScreenVariable("directory_is_editable", not directory_is_editable), SetScreenVariable("directory_input", file_explorer.current_dir)]
                            if directory_is_editable == False:
                                # use the truncated directory if not editing
                                text "[file_explorer.truncated_dir]":
                                    size 28
                                    color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                                    xalign 0
                            else:
                                # use the full directory if editing
                                input value ScreenVariableInputValue("directory_input"):
                                    size 28
                                    color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                                    xalign 0

                    null width 1.0  

                    # navigation buttons to the right of the directory     
                    frame:
                        padding (5, 5)
                        xsize 70
                        xpos -0.5
                        ysize 40
                        background FILE_EXPLORER_CONFIG["colors"]["background"]
                        
                        textbutton FILE_EXPLORER_CONFIG["icons"]["go"]:
                            action [Function(file_explorer.navigate_to_directory, directory_input), SetScreenVariable("directory_is_editable", False)]
                            text_size 26
                            text_color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                            xsize 50
                            ysize 40
                            background FILE_EXPLORER_CONFIG["colors"]["frame_background"]
                            hover_background FILE_EXPLORER_CONFIG["colors"]["button_hover"]
                            yalign 0.5
                            xpos 0.05

                        textbutton FILE_EXPLORER_CONFIG["icons"]["exit"]:
                            action [Hide("file_explorer_screen"), Function(file_explorer.reset_selection)]
                            text_size 26
                            text_color FILE_EXPLORER_CONFIG["colors"]["exit_text"]
                            xsize 40
                            ysize 40
                            background FILE_EXPLORER_CONFIG["colors"]["exit_button"]
                            hover_background FILE_EXPLORER_CONFIG["colors"]["exit_hover"]
                            yalign 0.5
                            xpos 1.0

            # centre row with the file grid and favourites
            hbox:
                spacing 20
                xsize 1200
                ysize 500

                frame:
                    xsize 200
                    ysize 500
                    background FILE_EXPLORER_CONFIG["colors"]["frame_background"]
                    padding (10, 10)

                    # favourites section
                    vbox:
                        spacing 10
                        text FILE_EXPLORER_CONFIG["language"]["favourites"] size 22 color "#FFFFFF" bold True

                        for name, path in FILE_EXPLORER_CONFIG["favourites"].items():
                            button:
                                xsize 180
                                ysize 50
                                background FILE_EXPLORER_CONFIG["colors"]["folder_background"]
                                padding (5, 5)
                                action Function(file_explorer.navigate_to_directory, path)

                                text name:
                                    size 18
                                    color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                                    xalign 0.5
                                    yalign 0.5
                                    textalign 0.5
                                    layout "nobreak"

                # file grid
                frame:
                    xsize 1000
                    ysize 500
                    background FILE_EXPLORER_CONFIG["colors"]["grid_background"]
                    padding (10, 10)

                    viewport:
                        xsize 1000
                        ysize 480
                        scrollbars "vertical"
                        mousewheel True

                        vpgrid:
                            cols 6
                            spacing 10

                            # add the "Up" button as the first item
                            if not file_explorer.root:
                                button:
                                    xsize 150
                                    ysize 150
                                    background FILE_EXPLORER_CONFIG["colors"]["folder_background"]
                                    action Function(file_explorer.go_up)
                                    text FILE_EXPLORER_CONFIG["icons"]["up"] + " " + FILE_EXPLORER_CONFIG["language"]["up"]:
                                        size 24
                                        color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                                        xalign 0.5 
                                        yalign 0.5

                            # drive buttons
                            for drive in file_explorer.drives:
                                $ drive_font_size = get_dynamic_font_size(drive)
                                button:
                                    xsize 150
                                    ysize 150
                                    background FILE_EXPLORER_CONFIG["colors"]["folder_background"]
                                    action Function(file_explorer.jump_drive, drive)
                                    text [FILE_EXPLORER_CONFIG["icons"]["drive"] + " " + drive]:
                                        size drive_font_size 
                                        color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                                        xalign 0.5 
                                        yalign 0.5 
                                        xmaximum 100

                            # folder buttons
                            for folder in file_explorer.folders:
                                $ folder_font_size = get_dynamic_font_size(folder)
                                button:
                                    xsize 150
                                    ysize 150
                                    background FILE_EXPLORER_CONFIG["colors"]["folder_background"]
                                    action Function(file_explorer.navigate_to, folder)
                                    text FILE_EXPLORER_CONFIG["icons"]["folder"] + " " + folder:
                                        size folder_font_size
                                        color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                                        xalign 0.5 
                                        yalign 0.5 
                                        xmaximum 100

                            # file buttons
                            for file in file_explorer.files:
                                $ file_font_size = get_dynamic_font_size(file)
                                button:
                                    xsize 150
                                    ysize 150
                                    background FILE_EXPLORER_CONFIG["colors"]["file_background"]
                                    action Function(file_explorer.select_file, file)
                                    # Work-around for text interpolation
                                    $ nfile = "[file!s]"
                                    text FILE_EXPLORER_CONFIG["icons"]["file"] + " " + nfile:
                                        size file_font_size 
                                        color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                                        xalign 0.5 
                                        yalign 0.5
                                        xmaximum 100

            # bottom row with the selected file and "Choose File" button
            frame:
                xsize 1200
                ysize 60
                background FILE_EXPLORER_CONFIG["colors"]["background"]
                padding (10, 10)

                hbox:
                    spacing 20
                    xsize 1200
                    ysize 60

                    # left: "Selected file:" label
                    text FILE_EXPLORER_CONFIG["language"]["selected_file"] + " " + (file_explorer.selected_file if file_explorer.selected_file else "None"):
                        size 18
                        color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                        xalign -0.025

                    # right: "Choose File" button
                    textbutton FILE_EXPLORER_CONFIG["language"]["choose_file"]:
                        action If(file_explorer.selected_file != None, (Function(file_explorer.choose_file, file_explorer.selected_file),Function(FileActionHandler, file_explorer.selected_file),Hide("file_explorer_screen")))
                        #action If(file_explorer.selected_file != None, Function(file_explorer.choose_file, file_explorer.selected_file))
                        #action Function(file_explorer.choose_file, file_explorer.selected_file)
                        text_size 20  # Corrected from 'size' to 'text_size'
                        background FILE_EXPLORER_CONFIG["colors"]["frame_background"]
                        hover_background FILE_EXPLORER_CONFIG["colors"]["button_hover"]
                        text_color FILE_EXPLORER_CONFIG["colors"]["text_color"]
                        xsize 200
                        ysize 40
                        xalign 1.0
                        yalign -0.1
                        text_xalign 0.5
