import os

import shutil
import sys
import time

basepath = r'G:\Bethesda Modding\SkyrimSE\mods'
profilepath = r'G:\Bethesda Modding\SkyrimSE\profiles\2021 Playthrough'
outputpath = r'G:\Bethesda Modding\SkyrimSE\test'
mod_dirs = []
with open(os.path.join(profilepath,'modlist.txt'),'r',encoding='utf-8-sig') as f:
    lines = f.readlines()
    num = 0

    for line in lines[::-1]: # reverse file as mod organizer stores it backwards
        if line.startswith('+'):  # means mod is active
            mod = line.strip()[1:]
            print(f'{num}: {mod}')
            mod_dirs.append(os.path.join(basepath,mod))
            num += 1

print(f'A total of {len(mod_dirs)} directories will now be checked for BSA-archivable content')
print('Path traversal will follow Mod Organizer Setup [In-order of Mod Organizer folder overwrite]')

# folders to search for in each directory to archive
folders_care = ['meshes', 'textures', 'music', 'seq', 'lodsettings', 'menus', 'sound', 'scripts', 'interface']
fold_num = 1
# Walking a directory tree and printing the names of the directories and files
# for dirpath, dirnames, files in os.walk(basepath):
#     if dirpath.endswith('mods'): # directory is basedir
#         print(f'[{fold_num:04}] Found directory: {dirpath}')
#     elif any(folder in dirpath for folder in ['separator','NET']):
#         continue
#     elif any(folder in dirpath for folder in folders_care): # directory is folder to archive bsa
#         print(f'\t[{fold_num:04}] Found BSA directory: {dirpath}')
#     for file_name in files:
#         print(file_name)
#     fold_num += 1
#     if fold_num > 5:
#         break

folders = os.listdir(basepath)
merge_folders = {
    'meshes': [],
    'textures': [],
    'music': [],
    'seq': [],
    'lodsettings': [],
    'menus': [],
    'sound': [],
    'scripts': [],
    'interface': []
}
for folder in mod_dirs:
    if any(skip in folder for skip in ['separator', 'NET']):  # ignore separators, others as needed
        continue  # skip
    else:
        print(f'[{fold_num:03}] Found mod directory: \t{folder}')
        fold_num +=1
        mod_content = os.scandir(folder)
        # Get directories that are BSA-archive able
        folder_grab = [mod for mod in mod_content if mod.is_dir() and mod.name.lower() in folders_care]
        if folder_grab:
            for mod_folder in folder_grab:
                bsa_path = os.path.join(folder, mod_folder.name)
                merge_folders[mod_folder.name.lower()].append(bsa_path)
                print(f'\t  Found BSA directory: \t{bsa_path}')
        else:
            print(f'\t  No Archivable Content Found')
print('Done')

# from: https://stackoverflow.com/questions/26496821/python-shutil-copytree-is-there-away-to-track-the-status-of-the-copying

def copy2_verbose(src, dst):
    print('\t Copying {0}'.format(src))
    shutil.copy2(src,dst)

# for folder in merge_folders:
#     dirpath = os.path.join(outputpath, folder)
#     os.makedirs(dirpath, exist_ok=True)
#     print(f'[{folder}] Combining all files into folder: {folder}')
#     mod_num = 1
#     total = len(merge_folders[folder])
#     start = time.perf_counter()
#     for mod in merge_folders[folder]:
#         print(f'\t[{folder}:{mod_num:03}] Copying folder {{{mod}}} into {folder} [{mod_num/total*100:.2f}% - {mod_num}/{total}]')
#         mod_num += 1
#         #shutil.copytree(mod, dirpath, copy_function=copy2_verbose, dirs_exist_ok=True) for verbosity
#         shutil.copytree(mod, dirpath, dirs_exist_ok=True)
#     end = time.perf_counter()
#     print(f'[{folder}] Completed Copying of all data of type [{folder}] in {end-start:.2f}s')

print('Done with all operations - Use Cathedral Asset Optimizer to pack into a BSA :)')

print('"Hiding" Folders by renaming - Reversible inside mod organizer UI if required or use flag hide=False in code')
hide = True # reverse this flag to reshow directories - useful for testing
for folder in merge_folders:
    for mod in merge_folders[folder]:
        if hide:
            print(f'\t[{folder}] Renaming folder {{{mod}}} to {{{mod+".mohidden"}}}')
            os.rename(mod,mod+".mohidden")
        else:
            break

if not hide:
    hidden = []
    for folder in mod_dirs:
        mod_content = os.scandir(folder)
        # Get directories that are BSA-archive able
        folder_grab = [mod for mod in mod_content if mod.is_dir() and mod.name.lower().endswith('.mohidden')]
        if folder_grab:
            for mod_folder in folder_grab:
                bsa_path = os.path.join(folder, mod_folder.name)
                print(f'\t  Found hidden directory: \t{bsa_path}')
                hidden.append(bsa_path)
    for hidden_dir in hidden:
        new_name = hidden_dir.replace(".mohidden","")
        print(f'\tRenaming folder {{{hidden_dir}}} to {{{new_name}}}')
        os.rename(hidden_dir, new_name)


""" # TODO put into functions? too lazy
# random extras: removal of thumbs.db or desktop.ini files in directories (doesn't remove folders - but could)
for (root, dirs, files) in os.walk(basepath, topdown=True):
    for file in files:
        if file.lower() in ['desktop.ini','thumbs.db']:
            print(file)
            print(root)
            print('--------------------------------')
            path = os.path.join(root, file)
            os.remove(path)

# random extras: removal of all .mohidden files in directories (doesn't remove folders - but could)
# extra warning: be sure you want to do this
for (root, dirs, files) in os.walk(basepath, topdown=True):
    for file in files:
        if '.mohidden' in file.lower():
            print(file)
            print(root)
            print('--------------------------------')
            path = os.path.join(root, file)
            os.remove(path)
            
# random extras: remove all empty directories
# from: https://stackoverflow.com/questions/23488924/how-to-delete-recursively-empty-folders-in-python3
def remove_empty_dir(path):
    try:
        os.rmdir(path)
        print(f'Removed Directory: {path}')
    except OSError:
        pass

def remove_empty_dirs(path):
    for root, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            remove_empty_dir(os.path.realpath(os.path.join(root, dirname)))
            
remove_empty_dirs(basepath)
"""