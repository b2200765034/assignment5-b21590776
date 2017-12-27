# -*- coding: utf-8 -*-

import os,sys


print(" ---HUBM DVD----")
print("A:\tAdd new dvd")
print("R:\tRemove dvd")
print("S:\tSearch dvd")
print("L:\tList dvd")
print("E:\tEdit dvd")
print("H:\tHire dvd")
print("Q:\tQuit")

serials = []
prices = []
names = []
genres = []
directors = []
states = []

file_name = sys.argv[1]

if os.path.exists(file_name):
    file = open(file_name,"r")
    input_file = file.readlines()
    file.close()
    for line in input_file:
        try:
            line = line.replace("\n","")
            line = line[:-1]
            line = line.split(",")
            
            serials.append(int(line[0].strip(" ")))
            prices.append(line[1].strip(" "))
            names.append(line[2].strip(" ").replace("\"",""))
            genres.append(line[3].strip(" ").replace("\"",""))
            directors.append(line[4].strip(" ").replace("\"",""))
            states.append(line[5].strip(" ").replace("\"",""))
        except:
            continue

"""
    searchs for names
"""
def searchWithName(key):
    key = key.replace('"',"").strip(" \t")
    index_found_names = [] 
    
    if len(key)<3:
        print("Min. 3 character for searching.")
    else:
        for i in range(len(serials)):
            name = names[i]
            if key==name[:len(key)]:
                index_found_names.append(i)
        return index_found_names
        
        


def add_dvd(command):
    serial = int(command[0])
    if serial in serials:
        print("The DVD exists.")
    else:
        serials.append(int(command[0].strip(" ")))
        prices.append(command[1].strip(" "))
        names.append(command[2].strip(" ").replace("\"",""))
        genres.append(command[3].strip(" ").replace("\"",""))
        directors.append(command[4].strip(" ").replace("\"",""))
        states.append(command[5].strip(" ").replace("\"",""))

def indexOfSerial(serial):
    for i in range(len(serials)):
        if serials[i]==serial:
            return i
    return -1

def delete_entry(serial):
    i = indexOfSerial(int(serial)) 
    if i==-1:
        print("The DVD doesn't exist.")
    else:
        del serials[i]
        del prices[i]
        del names[i]
        del genres[i]
        del directors[i]
        del states[i]

# edits an dvd
def edit(command):
    serial = int(command[1])
    index = indexOfSerial(serial)
    
    for i in range(2,len(command)):
        t = command[i].strip("{}").split("=")
        attribute = t[0]
        if attribute=="Price":
            prices[index]=t[1].replace("\"","")
        elif attribute=="Name":
            names[index]=t[1].replace("\"","")
        elif attribute=="Genre":
            genres[index]=t[1].replace("\"","")
        elif attribute=="Director":
            directors[index]=t[1].replace("\"","")
        elif attribute=="State":
            states[index]=t[1].replace("\"","")
            
    
"""
    Lists the DVDs
"""
def list_DVDs():
    founds = []
    for i in range(len(serials)):
        founds.append( (i,names[i]) )
    founds.sort(key=lambda x: x[1])
    
    print("Serial\tPrice\tName\tGenre\tDirector\tState")
    print("---\t---\t--------\t-------\t-------\t----------")
    for j in range(len(founds)):
        i = founds[j][0]
        print(str(serials[i])+"\t"+str(prices[i])+"\t"+names[i]+"\t"+genres[i]+"\t"+directors[i]+"\t"+states[i])
             


        
            
#hires an dvd
def hireDVD(serial):
    i = indexOfSerial(serial)
    print("Serial\tPrice\tName\tGenre\tDirector\tState")
    print("---\t---\t--------\t-------\t-------\t----------")
    print(str(serials[i])+"\t"+str(prices[i])+"\t"+names[i]+"\t"+genres[i]+"\t"+directors[i]+"\t"+states[i])
    if states[i] == "Hired":
        print("The DVD cannot be hired. Because it is already hired.")
    else:
        states[i] = "Hired"
        print("The DVD is hired.")
    

def save_dvds():
    output = open(file_name, "w")
    for i in range(len(serials)):
        record = str(serials[i])+","+str(prices[i])+","+names[i]+","+genres[i]+","+directors[i]+","+states[i]+";\n"
        output.write(record)
    output.close()


while(True):
        line = input("Enter a command:").split(",")
        command = line[0]

        if command=="A":
            add_dvd(line[1:])
        elif command=="S":
            dvds = searchWithName(line[1])
            if len(dvds)==0:
                print("No entry.")
                continue
            
            print("Serial\tPrice\tName\tGenre\tDirector\tState")
            print("---\t---\t--------\t---------\t---------\t----------")
            for i in dvds:
                print(str(serials[i])+"\t"+str(prices[i])+"\t"+names[i]+"\t"+genres[i]+"\t"+directors[i]+"\t"+states[i])

        elif command=="H":
            hireDVD(int(line[1]))
        elif command=="R":
            delete_entry(line[1])        
        elif command=="E":
            edit(line)
        elif command=="L":
            list_DVDs()
        elif command=="Q":
            save_dvds()
            break
        else:
            print("No command such that")



    
