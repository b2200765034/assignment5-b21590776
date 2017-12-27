# -*- coding: utf-8 -*-


file = open("input3.data","r")
output = open("output.txt","w")

name = []
place = []


for line in file.readlines():
    splt = line.strip("\n").split(":")
    name.append(splt[0])
    place.append(splt[1])

value = "Abel"      
print("Searching value is: ", value,"\n",file=output)

st = " ".join(name[0:len(name)-1]) #prints the current range
print(st,file=output)


def swap(lst, i, j):
    temp = lst[i] 
    lst[i] = lst[j]
    lst[j] = temp
    return lst

#insertion sort
for i in range(len(name)-1):    
    min_index = i
    for j in range(i+1,len(name)):
        if name[j]<name[min_index]:
            min_index=j
    name = swap(name, i, min_index)
    place = swap(place, i, min_index)

def search(lo,hi):

    if lo>hi:
        return -1

    s = " ".join(name[lo:hi])
    print(s,file=output)
    
    mid = int((lo+hi)/2)
    
    if value==name[mid]:
        return mid
    elif value>name[mid]:
        return search(mid+1,hi)
    elif value<name[mid]:
        return search(lo,mid-1)
    return -1

t = search(0, len(name)-1)

if t!=-1:
    print(value,file=output)
    print("\nThe search string is",value,"and the city is",place[t],file=output)
else:
    print("\nThe search string was not found in file",file=output)

file.close()
output.close()

