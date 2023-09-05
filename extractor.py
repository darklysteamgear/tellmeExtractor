#BY: Darkly SteamGear
#This script will extract and parse specific tellme data from a set of tellme files
#MAKE SURE YOU ADD YOUR TELLME DUMPS IN THE SAME FOLDER AS THIS PYTHON SCRIPT!!! see below line 430 to add your own python searching functions
#There is currently no GUI. Please note this script is still being worked on. use this library as you see fit for your
#Modpack project.
#Feel free to send me any suggestions, comments, or you could even tell me how absolute trash this looks with so much commented out

#TO START:
#1.Use tellme to dump your items, entities, dimensions, and biomes. these are currently the only supported dump
#types for the tellme extractor.
#2. rename each dump based on what type of dump they are to make it easier for yourself later on (ex. the entities dump should just be entities.txt and so on.)
#3. view and modify the code below name == main to your modpack needs. it's required to know some basic python to use this library.
#4. Easier veiwing and searching of all the items, entities, dimensions, and biomes in your modpack!

import random
import re
import time
#from difflib import SequenceMatcher
#import text2emotion as te
#from transformers import pipeline, set_seed,AutoTokenizer, AutoModelForCausalLM
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#import torch
#from nltk.corpus import wordnet as wn


#This class will extract and give specific data from tellme dumps. current supported tellme dumps are with their file ids:
#dimensions - 0
#biomes - 1
#entities - 2
#blocks - 3
#items - 4
class TellmeExtractor():
    #Specify the file name, and the file type id.
    def __init__(self, tmFiles, typeIds):
        st = time.time()
        self.tmFiles = tmFiles
        self.typeIds = typeIds
        self.realStupidText = []

        #Below are dictionaries generated from reading the given tell me dumps
        #Dimension dump dictionary
        self.dimDump = {
            "keymap": [],
          "id": [],
          "typeid" : [],
          "name": [],
          "initloaded" : [],
          "loaded": [],
          "wp": []
        }
        #Biome dump dictionary
        self.bimDump = {
            "keymap": [],
          "id": [],
          "regname": [],
          "biomename" : [],
          "temp": [],
          "tempcat" : [],
          "rain" : [],
          "snow" : [],
          "oceanic" : [],
          "biometype" : [],
          "biomedicts" : [],
          "validgen" : []
        }
        #Entity dump dictionary
        self.entDump = {
            "keymap": [],
            "modname": [],
            "regname": [],
            "classname": [],
            "id": []
        }
        #Block dump dictionary
        self.blkDump = {
            "keymap": [],
            "modname": [],
            "regname": [],
            "bid" : [],
            "subtypes": [],
             "iid" : [],
             "imeta" : [],
             "name" : [],
             "exists" : [],
             "orekeys" : []
        }
        #Item dump dictionary
        self.itmDump = {
            "keymap": [],
            "modname": [],
            "regname": [],
             "id" : [],
             "imeta" : [],
             "subtypes": [],
             "name" : [],
             "orekeys" : []
        }
        self.dimDump["keymap"].append(list(self.dimDump.keys())[1:])
        self.bimDump["keymap"].append(list(self.bimDump.keys())[1:])
        self.entDump["keymap"].append(list(self.entDump.keys())[1:])
        self.blkDump["keymap"].append(list(self.blkDump.keys())[1:])
        self.itmDump["keymap"].append(list(self.itmDump.keys())[1:])

        #Populate the dump dictionaries with the provided tellme dumps
        self.populate_data()
        et = time.time()
        print(f'Tellme extractor took {int((et-st) *1000)} ms to populate all data')

    #The main function to populate all data in the list depending on the type of file
    def populate_data(self):
        i = 0
        for tmFile in self.tmFiles:
            self.populate_dict(tmFile,self.typeIds[i])
            i+=1

    #Since python doesn't really have anything to convert a string to a proper bool
    def str2bool(self, val):
        return val.lower() in ("yes", "true", "t", "1")

    #Use case statements to create the correct types of dictionaries for each tellme dump
    def find_dump_type(self,typeId):
        dump = {}
        match typeId:
            case 0:
                dump = self.dimDump
            case 1:
                dump = self.bimDump
            case 2:
                dump = self.entDump
            case 3:
                dump = self.blkDump
            case 4:
                dump = self.itmDump
        return dump

    #Sets the dump type for each dictionary
    def set_dump(self,dump, typeId):
        match typeId:
            case 0:
                self.dimDump = dump
            case 1:
                self.bimDump = dump
            case 2:
                self.entDump = dump
            case 3:
                self.blkDump = dump
            case 4:
                self.itmDump = dump

    #The dimension populator, if filetype is a dimension
    def populate_dict(self,tmFile, typeId):
        try:
            file1 = open(tmFile, encoding="utf8")
            lines = file1.readlines()
        except UnicodeDecodeError:
            file1 = open(tmFile, encoding="ansi")
            lines = file1.readlines()

        dump = self.find_dump_type(typeId)
        i = 0
        keyindicator = 0
        isKey = False
        for line in lines:
            try:
                if ((keyindicator == 1) & (line[1] == " ")):
                    isKey = True
                if line[0] == '+':
                    keyindicator += 1
                values = re.findall(r' (.*?) \|', line)
                j = 0
                for value in values:
                    value = value.strip()
                    if isKey:
                        keymap = []
                        keymap.append(value)
                        valuet = value.replace(" ", "")
                        keymap.append(valuet)
                        value = value.lower()
                        valuet = value.replace(" ", "")
                        keymap.append(value)
                        keymap.append(valuet)
                        value = value.upper()
                        valuet = value.replace(" ", "")
                        keymap.append(value)
                        keymap.append(valuet)
                        dump["keymap"].append(keymap)
                    else:
                        dump[dump["keymap"][0][j]].append(value)
                    j+=1
                isKey = False
            except ValueError:
                continue
            self.set_dump(dump, typeId)
        file1.close()

    #Function to search for a specific entity based on the entities classname
    def find_entities_from_classname(self,searchstr):
        resdump = []
        i =0
        for x in self.entDump["classname"]:
            if re.search(searchstr.lower(), x.lower()):
                resdump.append(self.entDump["regname"][i])
            i+= 1
        return resdump
    #Function to search for an entity based on the mod an entity is from
    def find_entities_from_modname(self,searchstr):
        resdump = []
        i =0
        for x in self.entDump["modname"]:
            if re.search(searchstr.lower(), x.lower()):
                resdump.append(self.entDump["regname"][i])
            i+= 1
        return resdump

    #Function to find a block based on what mod it is from
    def find_blocks_from_modname(self,searchstr):
        resdump = []
        i =0
        for x in self.blkDump["modname"]:
            if re.search(searchstr.lower(), x.lower()):
                resdump.append(self.blkDump["regname"][i])
            i+= 1
        return resdump
    #Function to find a block based on it's name
    def find_blocks_from_name(self,searchstr):
        resdump = []
        i =0
        for x in self.blkDump["name"]:
            if re.search(searchstr.lower(), x.lower()):
                resdump.append(self.blkDump["regname"][i])
            i+= 1
        return resdump
    #Function to find a block based on it's registry name
    def find_items_from_regname(self,searchstr):
        resdump = []
        i =0
        for x in self.itmDump["regname"]:
            if re.search(searchstr.lower(), x.lower()):
                resdump.append(self.itmDump["regname"][i])
            i+= 1
        return resdump
    #Function to find an item based on it's name
    def find_items_from_name(self,searchstr):
        resdump = []
        i =0
        for x in self.itmDump["name"]:
            if re.search(searchstr.lower(), x.lower()):
                resdump.append(self.itmDump["name"][i])
            i+= 1
        return resdump

    #Print command to show the items found in a list
    def print_for_config(self, list):
        for x in list:
            print(x)


    #_____________________IGNORE___________________________________
    #Ignore. this code below was used to randomly generate srparasite assimilations for
    #All mobs in my modpack Madhaus
    # def prompt_generator(self,mobs,assimilatedforms):
    #     prompts = []
    #
    # def wn_similarity(self,word1, word2, lch_threshold=1.5):
    #     results = []
    #     for net1 in "wn.synsets(word1)":
    #         for net2 in "wn.synsets(word2)":
    #             try:
    #                 lch = net1.lch_similarity(net2)
    #             except:
    #                 continue
    #             # The value to compare the LCH to was found empirically.
    #             # (The value is very application dependent. Experiment!)
    #             if lch >= lch_threshold:
    #                 results.append((net1, net2))
    #     if not results:
    #         return 0.0
    #     for net1, net2 in results:
    #         similarity = net1.wup_similarity(net2)
    #         return similarity
    #
    # #We are the borg, resistance is futile, prepare for assimilation
    # def assimilate_mobs(self,mobs,assimilatedforms):
    #     tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
    #     model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
    #     collective = []
    #     sentiment = SentimentIntensityAnalyzer()
    #     generator = pipeline('text-generation', model=model, tokenizer=tokenizer, device=0)
    #     for x in mobs:
    #         greatestlikelihood = 0
    #         bestmob = ''
    #         scariestmob = ''
    #         bestscare = -1
    #         bestnamesimilarityscare = 0
    #         likeliestmob = ''
    #         bestscareli = ''
    #         winnerlike = ''
    #         winnerscare = ''
    #         bestnamesimilarity = 0
    #         for y in assimilatedforms:
    #             xsp = x.find(':')
    #             ysp = y.find(':')
    #             modx = x[:xsp]
    #             mody = y[2:ysp - 1]
    #             namex = x[xsp + 1:]
    #             namey = y[ysp + 1:]
    #             prompt = f'{namex} is now a {namey} {mody} and is going to'
    #             set_seed(len(namex) + len(namey))
    #             text = generator(prompt, max_length=50, pad_token_id=50256, do_sample=True, temperature=0.5)
    #             #print(text[0]['generated_text'])
    #             scores = sentiment.polarity_scores(text[0]['generated_text'])
    #             emotions = te.get_emotion(text[0]['generated_text'])
    #             #print(scores)
    #             scarefactor = ((emotions['Fear']) * 0.5) + (scores['neg'] *0.5)
    #             #print(f'SCAREFACTOR: {scarefactor}')
    #             namesimilarity = (self.wn_similarity(namex,namey)*0.75) + ((SequenceMatcher(None, namex, namey).ratio())*0.5)
    #             likelihood = namesimilarity
    #             if scarefactor > bestscare:
    #                 bestscare = scarefactor
    #                 scariestmob = y
    #                 bestnamesimilarityscare = namesimilarity
    #                 winnerscare = text[0]['generated_text']
    #             if likelihood > greatestlikelihood:
    #                 greatestlikelihood = likelihood
    #                 likeliestmob = y
    #                 bestscareli = scarefactor
    #                 bestnamesimilarity = namesimilarity
    #                 winnerlike = text[0]['generated_text']
    #         if greatestlikelihood < 0.35:
    #             bestmob = scariestmob
    #             bestnamesimilarity = bestnamesimilarityscare
    #             self.realStupidText.append(winnerscare)
    #         else:
    #             bestmob = likeliestmob
    #             bestscare = bestscareli
    #             self.realStupidText.append(winnerlike)
    #
    #         print(f'bestmob for {x} has been determined to be {bestmob}. It had a scariness factor of {bestscare * 100}% and is {bestnamesimilarity * 100}% similar to the mob text')
    #         #print(f'SCARIEST PHRASE:\n{winnerscare}\n')
    #         collective.append(x + ";" + bestmob)
    #     return collective
#_____________________IGNORE__________________________________


#Unfinished class for creating a mods list based on files found in the tellme dump. ignore
def updatemodslist(file):
    return

#fragement method I used to generate mob assimilations for srparasite parasites.
#I repurposed it to generate wood files a little bit ago. it's still here for an unknown reason
#TODO: DEEP CLEAN THIS CODE BECAUSE IT IS VERY UGLY
def assimilate_all(entity,assim):
    file1 = open('items2.txt')
    lines = file1.readlines()
    found = []
    i = 0

    for line in lines:
        linetemp = line[47:]
        fbi = linetemp.find("   ")
        linetemp = linetemp[:fbi]
        if (linetemp.find(entity) == -1):
            print("no")
        else:
            i += 1
            found.append('var wood' + str(i) + '(<' + linetemp + '>);')

    for assimmob in found:
        print(assimmob)

#This will find dimension info based on the name of a given dimension
def find_dimensions(dimname):
    file1 = open('dim.txt')
    lines = file1.readlines()
    foundid = []
    foundname = []
    i = 0

    for line in lines:
        id = line[:12]
        name = line [32:67]
        linetemp = name
        if (linetemp.find(dimname) != -1):
            i += 1
            foundid.append(int(id[1:-2]))
            endofname = name.find('   ')
            foundname.append(name[0:endofname])
    i = 0
    for dimid in foundid:
        print("id: " + str(foundid[i]) + " name: " + foundname[i])
        i+=1

#CODE BELOW IS FOR SIMPLE DIFFICULTY JSON GENERATION
#This will generate a json line based on a given temperature and armor.
def sd_armor_json_generator(armor, temp):
    print("   \""+ armor + "\": [")
    print("     {")
    print("         \"identity\": {")
    print("             \"metadata\": -1")
    print("             },")
    print("     \"temperature\":" + str(temp))
    print("         }")
    print("   ],")

#This will generate a json line for simple difficultie's json based on a given item, temperature, duration, and group.
def sd_consumable_generator(item,temp,duration, group):
    print("\""+ item + "\": [")
    print("{")
    print("\"identity\": {")
    print("\"metadata\": -1")
    print("}")
    print("\"group\":" + group + ",")
    print("\"temperature\":" + str(temp) + ",")
    print("\"duration\":" + str(duration))
    print("}")
    print("],")

#This is for randomizing doom like dungeons items based on a given loot type, and a list of items for that loot type
#see the doom like dungeons loot configuration for more info on loot types that it can generate
def dld_loot_table_randomizer(type, items):
    i = 0
    out1 = ""
    out2 = ""
    out3 = ""
    out4 = ""
    out5 = ""
    for item in items:
        rando = random.randint(1, 5)
        if rando == 1:
            out1 += type + ", " + str(rando) +", " + item + " , 1,1\n"
        if rando == 2:
            out2 += type +", " + str(rando) +", " + item + " , 1,1\n"
        if rando == 3:
            out3 += type + ", " + str(rando) +", " + item + " , 1,1\n"
        if rando == 4:
            out4 += type + ", " + str(rando) +", " + item + " , 1,1\n"
        if rando == 5:
            out5 += type +", " + str(rando) +", " + item + " , 1,1\n"

    print(out1 + "\n\n")
    print(out2 + "\n\n")
    print(out3 + "\n\n")
    print(out4 + "\n\n")
    print(out5 + "\n\n")


#This is the main function. add whatever python code you want to interface with your tellme dumps here/
if __name__ == '__main__':
    #print(torch.cuda.is_available())


    #Replace this with the names of your tellme dumps.
    #MAKE SURE YOU ADD YOUR TELLME DUMPS IN THE SAME FOLDER AS THIS PYTHON SCRIPT!!!
    tellmedumps = ["dimensions.txt","biomes.txt","entities.txt", "blocks.txt", "items.txt"]
    #Replace this with the types of your tellme dumps you wish to have parsed into the extractor
    dumptypes = [0, 1, 2, 3, 4]
    dumps = TellmeExtractor(tellmedumps,dumptypes)

    #This will create integers based on how many of each type of thing are in your tellme dumps
    dimensions = len(dumps.dimDump["id"])
    biomes = len(dumps.bimDump["id"])
    entities = len(dumps.entDump["id"])
    blocks = len(dumps.blkDump["bid"])
    items = len(dumps.itmDump["id"])
    dimIds = dumps.dimDump["id"]
    print(f' Number of dimensions {dimensions}\n'
           f' Number of biomes {biomes}\n '
           f'Number of entities {entities}\n '
           f'Number of blocks {blocks}\n'
           f' Number of items {items}\n total number of things {items + blocks + entities + biomes + dimensions}')

    #Here is a small example of how you could find all entities with the name Cow in your list and print it out.
    animaldumps = []
    cows = dumps.find_entities_from_classname("Cow")
    print("\nCOW ENTITIES IN YOUR MODLIST:")
    for x in cows:
        animaldumps.append(x)
    dumps.print_for_config(animaldumps)
    #Below is some of the code I used to generate configuration files for my modpack Madhaus.
    #A lil bit of a mess at the moment. but you should be able to figure out how to use it with the comments I left.

    #IGNORE/USE BELOW CODE AS EXAMPLE OF FUNCTIONALITY FOR LIBRARY

    # animaldumps = []
    # cows = dumps.find_entities_from_classname("Cow")
    # zoocraftMobs = dumps.find_entities_from_modname("Zoocraft")
    # wildMobs = dumps.find_entities_from_modname("wild")
    # parasites = dumps.find_entities_from_modname("parasites")
    # herobrines = dumps.find_entities_from_modname("more creeps")
    # scpblks = dumps.find_blocks_from_name("reinforced")
    # blockgns = dumps.find_items_from_regname("ammo")
    # leggings = dumps.find_items_from_regname("thermalfoundation:tool")
    # generators = dumps.find_items_from_regname("mekanism")
    # heatpro = dumps.find_items_from_regname("atum:body_of")
    #chestplates = dumps.find_items_from_regname("thermalfoundation:armor.plate_")
    #helmets = dumps.find_items_from_regname("thermalfoundation:armor.helmet_")
    #boots = dumps.find_items_from_regname("thermalfoundation:armor.boots_")
    # mobdump = []
    # i = 0
    # for x in dumps.entDump["modname"]:
    #     if x not in "SRParasites":
    #         mobdump.append(dumps.entDump["regname"][i])
    #     i+=1
    #
    # for x in dumps.bimDump["regname"]:
    #     print(x)
    #
    #
    # for x in cows:
    #     animaldumps.append(x)
    # for x in zoocraftMobs:
    #     animaldumps.append(x)
    # for x in wildMobs:
    #     animaldumps.append(x)
    #parasites = [x for x in parasites if 'ada_' not in x]
    #parasites = [x for x in parasites if 'anc_' not in x]
    #parasites = [x for x in parasites if 'pri_' not in x]
    #parasites = [x for x in parasites if 'warden' not in x]
    #parasites = [x for x in parasites if 'overseer' not in x]
    #parasites = [x for x in parasites if 'bogle' not in x]
    #parasites = [x for x in parasites if 'iii' not in x]
    #parasites = [x for x in parasites if '_siv' not in x]
    #parasites = [x for x in parasites if 'haunter' not in x]
    #parasites = [x for x in parasites if 'carrier' not in x]
    #parasites = [x for x in parasites if 'wave' not in x]
    #parasites = [x for x in parasites if 'monarch' not in x]
    #parasites = [x for x in parasites if 'infested' not in x]
    #parasites = [x for x in parasites if 'source' not in x]
    #parasites = [x for x in parasites if 'remain' not in x]
    #parasites = [x for x in parasites if 'ball' not in x]
    #parasites = [x for x in parasites if 'bomb' not in x]
    #parasites = [x for x in parasites if 'missile' not in x]
    #parasites = [x for x in parasites if 'ancientball' not in x]
    #parasites = [x for x in parasites if 'heavy' not in x]
    #parasites = [x for x in parasites if 'homming' not in x]
    #parasites = [x for x in parasites if 'wraith' not in x]
    #parasites = [x for x in parasites if 'cloudtoxic' not in x]
    # for coolarmor in heatpro:
    #     sd_armor_json_generator(coolarmor, -2.0)
    #dumps.print_for_config(animaldumps)
    #dumps.print_for_config(parasites)
    #assimilation = dumps.assimilate_mobs(mobdump, parasites)
    #dumps.print_for_config(assimilation)
    #for text in dumps.realStupidText:
        #print(text)