#complete json template:
#{
#   "birth_date": "1974-09-02",
#   "gender": "F",
#   "events": [
#        {
#            "date": "2016-03-01",
#            "system": "http://hl7.org/fhir/sid/icd-10",
#            "code": "Z01.00"
#        },
#        {
#            "date": "2014-05-23",
#            "system": "http://hl7.org/fhir/sid/icd-9-cm",
#            "code": "367.0"
#        }
#    ]
#}
#icd9url = "http://hl7.org/fhir/sid/icd-9-cm"
#icd10url= "http://hl7.org/fhir/sid/icd-10"

#get event format of json
def getevent(line):
    info=line.split('|')
    #Default tenplate for json string 
    tempstring='''  
        {
         "date": "%s",
         "system": "%s",
         "code": "%s"
        }
        '''
    tempurl="http://hl7.org/fhir/sid/icd-9-cm"
    if info[2]=="10": #if system equals icd-10
        tempurl= "http://hl7.org/fhir/sid/icd-10"
    events=tempstring%(info[1], tempurl, info[3])
    return events

#create dictionary for events.psv with key as patient_id
def p_events(filename):
    events_dict=dict()
    file=open(filename,'r')
    next(file)
    for line in file: 
        line=line.rstrip()
        info=line.split('|')
        if len(info)==4 and "" not in info: #if line contains all the information
            events=getevent(line)
            #since patients have multiple events in events_psv, the events are stored as lists
            if info[0] in events_dict: #event template of patient appended in dictionary
                events_dict[info[0]].append(events)
            else:
                events_dict[info[0]] = [events]
    return events_dict
                
#create dictionary for demo.psv with key as patient_id
def p_demo(filename):
    demo_dict=dict()
    file=open(filename,'r')
    next(file)
    for line in file:
        line=line.rstrip() #rstrip to remove trailing whitespaces and newlines
        info=line.split('|')
        if len(info)==3: #if line contains all the information
            demo_dict[info[0]]=info #entire demo entry of patient sent as list
    return demo_dict

#create jsonfiles for each patient
def jsonseries(events_dict, demo_dict):
    #default template for json file
    jsontemp=''' 
    {
        "birth_date": "%s",
        "gender": "%s",
        "events": [
            %s
        ]
    }
    '''
    for key, value in demo_dict.items(): #key=patient_id,value=patients_demo_entry as list
        if key in events_dict: #check if patient_id is present in both the dictionaries
            st=",".join(events_dict[key])
            #info=value.split('|')
            jsonf=jsontemp%(value[1],value[2],st)
            filename=value[0]+".json" #patient_id.json file
            file=open(filename,'w') 
            file.write(jsonf)

#main function
def main():
    fevents="events.psv"
    fdemo="demo.psv"
    pevent_dict=p_events(fevents)
    pdemo_dict=p_demo(fdemo)
    jsonseries(pevent_dict,pdemo_dict)
    
if __name__==main():
    main()
