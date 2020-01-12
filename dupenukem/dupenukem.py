'''
Checks for duplicate images within the current directory or path argument and moves the duplicated pares to sub-directories for manual comparison'''

import sys, os, itertools, filecmp, shutil

# Change working directory to the first argument specified if one exists.
try:
    if os.path.isdir(sys.argv[1]):
        os.chdir(sys.argv[1])
except(IndexError):
    print("No path argument found. Using current directory.")

# Utility functions for DRY sake.
def makeComparisonDirectories(dirName):
    try:
        os.makedirs(dirName)
    except(FileExistsError):
        pass

def dupeNuke(dupeList):
    for dupeItem in dupeList:
        print('Deleting: ' + dupeItem)
        os.remove(dupeItem)

def cleanup():
    print('Cleaning up...')
    shutil.rmtree('f1')
    shutil.rmtree('f2')
    print('Cleanup complete.')

# Made this a function because DRY.
makeComparisonDirectories('f1')
makeComparisonDirectories('f2')

files = os.listdir()

dupes = 0
dupeList = []

print('Those duplicate bastards are gonna pay for taking up my space!')

# Compare the files and move any duplicates found to the f1/f2 directories for manual comparison. (this is a safety feature)
for f1, f2 in itertools.combinations(files, 2):
    if filecmp.cmp(f1, f2):
        dupes += 1
        print(f1 + " looks like " + f2)
        shutil.copy(f1, 'f1')
        shutil.copy(f2, 'f2')
        dupeList.append(f2)

print(str(dupes) + ' duplicates found.')

if dupes > 0:
    print('Look in the f1 and f2 directories to verify there were no mistakes.')

    while True:
        response = input("Shall we nuke the dupes? WARNING: THIS WILL DELETE THE DUPLICATE FILES! MAKE DAMN SURE YOU WANT TO DO THIS BEFORE YOU ANSWER! (Y/N)")
        if response in ('Y', 'y'):
            dupeNuke(dupeList)
            break
        elif response in ('N', 'n'):
            print('Leaving dupes in place.')
            break
        else:
            print('No, seriously. (Y/N)')

cleanup()