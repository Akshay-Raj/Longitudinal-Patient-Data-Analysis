#Code to get the statistics file

import json
import os
import datetime


#get number of days between first and last event
def getdays(data):
    datelist=[]
    #convert string format to date format
    bdate=datetime.datetime.strptime(data["birth_date"],'%Y-%m-%d')
    for i in range(len(data["events"])):
        date=datetime.datetime.strptime(data["events"][i]["date"],'%Y-%m-%d') 
        datelist.append(date)
    maxdate=max(datelist)
    mindate=min(datelist)
    diff=maxdate - mindate
    age=maxdate.year-bdate.year
    return diff.days, age

#get median from a list
def getmedian(temp):
    temp.sort()
    length = len(temp)
    if (length % 2 == 0):
        median = (temp[(length)//2] + temp[(length)//2-1]) / 2
    else:
        median = temp[(length-1)//2]
    return median

#main function
def main():
    rootdir=input("enter root path where json files are located example /Users/ap/Downloads/lumiata_take_home\n")
    #all json file names are stored in json_files
    json_files = [jfile for jfile in os.listdir(rootdir) if jfile.endswith('.json')]
    mcount=0# store count of male patients
    fcount=0# store count of female patients
    p_timeline=[]# list to store timelines of all patients
    p_age=[]# list to store age of all patients
    for filename in json_files:
        data_file=open(filename)    
        data = json.load(data_file)# load the jsondata into data
        if(data["gender"]=="M"):#access gender from json data stored in data
            mcount+=1
        else:
            fcount+=1
            
        days,age=getdays(data)# get age and timeline of patient
        if(days!=0):#ignore timeline if patient has single event
            p_timeline.append(days)
        p_age.append(age)
    #print(p_age)    
    maxt=max(p_timeline)#get max timeline from the list
    mint=min(p_timeline)#get min timeline from the list
    mediant=getmedian(p_timeline)# get median from list
    
    maxage=max(p_age)#get max age from the list
    minage=min(p_age)#get min age from the list
    mediana=getmedian(p_age)#get median from the list
    
    #to create statistics text file
    with open('statistics.txt', 'w') as f: 
        print("Number of valid male patients is {}".format(mcount), file=f)
        print("Number of valid female patients is {}\n".format(fcount), file=f)
        
        print("Maximum timeline of patients is {}".format(maxt), file=f)
        print("Minimum timeline of patients is {}".format(mint), file=f)
        print("Median timeline of patients is {}\n".format(mediant), file=f) 
            
        print("Maximum age of patients is {}".format(maxage), file=f)
        print("Minimum age of patients is {}".format(minage), file=f)
        print("Median  age of patients is {}".format(mediana), file=f)  
    
    print("The Output can be found as statistics.txt")

if __name__==main():
    main()