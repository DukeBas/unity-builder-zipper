import subprocess
from unityparser import UnityDocument
from pathlib import Path
import time

# USER SETTINGS
settings = {  # File paths are relative, except where noted
    # Absolute path to Unity executable
    'abs_path_unity': r'C:\Program Files\Unity\Hub\Editor\2022.3.20f1\Editor\Unity.exe',
    # Absolute path to 7-Zip executable
    '7z_path': r'C:\Program Files\7-Zip\7z.exe',
    # Path to ProjectSettings.asset file
    'project_settings': r'ProjectSettings/ProjectSettings.asset',
    # Name of the game, used for built executable name
    'game_name': r'ProjectAlexandrite',
    # Prefix for zipped build names
    'build_name': r'PA-',
    # Folder path for zipped builds
    'zipped_builds_folder_filepath': r'zipped-builds',
    # Folder path for latest Windows build
    'windows_builds_folder': r'auto-build-win',
    # Folder path for latest Mac build
    'mac_builds_folder': r'auto-build-mac',
    # Folder path for latest Linux build
    'linux_builds_folder': r'auto-build-linux',
    # Path to README file
    'readme_filepath': r'README.md',
}
build_targets = {  # Build targets
    'windows': True,
    'mac': False,
    'linux': True,
}
#####

strings = {
    # Unity command line option for Windows build, file path after this option
    'unity_windows_option': '-buildWindows64Player',
    # Unity command line option for Mac build, file path after this option
    'unity_mac_option': '-buildOSXPlayer',
    # Unity command line option for Linux build, file path after this option
    'unity_linux_option': '-buildLinux64Player',
    # File extension for Windows build
    'extension_windows': '.exe',
    # File extension for Mac build
    'extension_mac': '.app',
    # File extension for Linux build
    'extension_linux': '.x86_64',
}


@staticmethod
def get_build_name(target_platform: str, project_version: str) -> str:
    # Get build name
    build_name = settings['build_name'] + \
        project_version + '-' + target_platform
    return build_name


# Get project version
doc = UnityDocument.load_yaml(Path(settings['project_settings']))
ProjectSettings = doc.entry
ProjectVersion = ProjectSettings.bundleVersion

# Get build names
build_names = {}
for target_platform, build_enabled in build_targets.items():
    if build_enabled:
        build_names[target_platform] = get_build_name(
            target_platform, ProjectVersion)

# Check if project version already exists for zipped builds
zipped_builds_folder = Path(settings['zipped_builds_folder_filepath'])
zipped_builds = list(zipped_builds_folder.glob('*.zip'))
for zipped_build in zipped_builds:
    for target_platform, build_name in build_names.items():
        if build_name in zipped_build.name:
            print(
                f"Build {build_name} already exists. Please delete it or update the version before building again.")
            exit(1)

# Continue with build process
print(f"Building version {ProjectVersion} for the following platforms:")
for target_platform, build_name in build_names.items():
    print(f"  - {target_platform}")

# Build for each target platform
for target_platform, build_name in build_names.items():
    print(f"Building {build_name}...")

    # Get build folder path
    build_folder = Path.cwd() / \
        (settings[target_platform + '_builds_folder'] +
         "-" + time.strftime("%Y-%m-%d-%H-%M-%S"))

    # Make editor call
    abs_unity_path = Path(settings['abs_path_unity'])
    abs_build_file_path = build_folder / settings['game_name']
    abs_build_file_path = abs_build_file_path.with_suffix(
        strings['extension_' + target_platform])
    abs_project_folder_path = Path.cwd()
    platform = 'unity_' + target_platform + '_option'
    unity_call = f'"{abs_unity_path}" -batchmode -quit -projectpath "{abs_project_folder_path}" {strings[platform]} "{abs_build_file_path}"'

    # Do the call
    subprocess.run(unity_call)

    # Check if build folder exists
    if not build_folder.exists():
        print(f"Build failed for {target_platform}.")
        exit(1)

    # Add README file to build folder
    readme_path = Path(settings['readme_filepath'])
    readme_dest = build_folder / readme_path
    readme_dest.write_text(readme_path.read_text())

    # Make a zip of the build folder
    zip_name = build_name + '.zip'
    zip_path = zipped_builds_folder / zip_name
    subprocess.run([settings['7z_path'], 'a', str(
        zip_path), str(build_folder) + '/*'])

    # Finally, let the user know the build succeeded
    print(f"Build succeeded for {target_platform}.")
