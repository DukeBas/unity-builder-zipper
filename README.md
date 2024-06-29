# Unity Builder Zipper
Python script to automate making and zipping multi-platform desktop builds for Unity games for easy distribution.

## Description
The script calls the Unity editor as a CLI and then uses 7zip to make a compressed build file per platform. The game version as defined in the editor under player settings (Edit->Project Settings->Player->Version) is added to the build name.

## Usage
1. Make sure you have 7zip and a recent version of Python installed.
2. Install the dependencies using `pip install -r requirements.txt`
3. Place `build-script.py` in your Unity project folder (the folder with `Assets` ,`Packages`, etc.)
4. Modify settings inside `build-script.py` by opening it up in your usual Unity editor of choice or VSC. All settings are near the top in the `settings` object.
   1. Change `abs_path_unity` to point to your Unity editor install. This can be found by launching Unity Hub, clicking on 'Installs' on the left and copying the file path of the desired editor version.
   2. Change `7z_path` to point to 7zip.
   3. Change `game_name` and `build_name` to match the name of your game.
   4. Potentially change other settings if desired, all of them have explanations for what they do.

Now the script can be used by running the Python script using a command prompt `python build-script.py`.
