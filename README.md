# The Tellme File Extractor
Are you tired of not being able to use code to generate configuration files based on the item lists that tellme has generated? well look no more, the tell me extractor allows you to import those generated lists into a python dictionary for easier manipulation and creation of custom modpack configurations!

## CURRENT SUPPORTED DUMP FILES:
-Biome dumps
- Entity Dumps
- Item Dumps
- Dimension dumps

## REQUIREMENTS:
- Basic knowledge of python, to be able to use this library. Implementing the class for your own modpack project should be a fairly simple few lines after knowing some basic python.
- Modpack with tellme dumps, you will need to create tellme dumps of your modpack

## OTHER
- This script will extract and parse specific tellme data from a set of tellme files
- MAKE SURE YOU ADD YOUR TELLME DUMPS IN THE SAME FOLDER AS THIS PYTHON SCRIPT!!! see below line 430 to add your own python searching functions
- There is currently no GUI. Please note this script is still being worked on. use this library as you see fit for your Modpack project.


## TO START:
1. Use tellme to dump your items, entities, dimensions, and biomes. these are currently the only supported dump types for the tellme extractor.
2. rename each dump based on what type of dump they are to make it easier for yourself later on (ex. the entities dump should just be entities.txt and so on.)
3. view and modify the code below name == main to your modpack needs. it's required to know some basic python to use this library.
4. Easier veiwing and searching of all the items, entities, dimensions, and biomes in your modpack!


Feel free to send me any suggestions, comments, or you could even tell me how absolute trash this looks with so much commented out
