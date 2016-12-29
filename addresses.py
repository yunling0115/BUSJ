import os, re, codecs, json, sys
sys.setrecursionlimit(10000)

keys_long = ['Reprint Address:','Addresses:']    

def findpattern(pattern,x):
    if len(re.findall(pattern,x))>0:
        return re.findall(pattern,x)[0]
    else:
        return ''
        
def grab(x, key):
    if key in x.keys():
        if type(x[key])==list:
            return map(lambda y: re.sub('"',"'",re.sub('\n',';',y)).strip(), x[key])
        else:
            return re.sub('"',"'",re.sub('\n',';',x[key])).strip()
    else:
        return ''

################################### ADDRESSES #####################################

allfields = ['_ACCOUNTING','_ECONOMICS','_ENTREPRENEURSHIP','_FINANCE','_INFORMATION','_INTERNATIONAL','_MANAGEMENT','_MARKETING','_PRACTITIONER']

for field in allfields:
    print(field)
    
    path = 'C:\\Users\\yling\\WOS\\JOURNAL\\'+field
    pathjson = 'C:\\Users\\yling\\WOS\\JOURNAL\\json\\'+field
    pathcsv = 'C:\\Users\\yling\\WOS\\JOURNAL\\addresses\\'+field
    
    os.mkdir(pathcsv)
    
    journals = os.listdir(path)
    
    for journal in journals:
        print(field+':'+journal)
        with codecs.open(pathjson+'\\'+journal+'.json','r',encoding='utf8') as f:
            txt = f.read()
        papers = json.loads(txt)['papers']
        with codecs.open(pathcsv+'\\addresses_'+journal+'.csv','w',encoding='utf8') as f:
            f.write('Title,ISSN,DOI,Author,Address\n')
            for i in range(len(papers)):
                if 'Addresses:' in papers[i].keys():
                    for j in range(len(papers[i]['Addresses:'])):
                        f.write('"'+grab(papers[i],'Title:')+'",')
                        f.write('"'+grab(papers[i],'ISSN:')+'",')
                        f.write('"'+grab(papers[i],'DOI:')+'",')
                        f.write('"'+papers[i]['Addresses:'][j].split(':')[0]+'",')
                        f.write('"'+papers[i]['Addresses:'][j].split(':')[1]+'"\n')
                        
################################### REPRINT ADDRESSES #####################################

allfields = ['_ACCOUNTING','_ECONOMICS','_ENTREPRENEURSHIP','_FINANCE','_INFORMATION','_INTERNATIONAL','_MANAGEMENT','_MARKETING','_PRACTITIONER']

for field in allfields:
    print(field)
    
    path = 'C:\\Users\\yling\\WOS\\JOURNAL\\'+field
    pathjson = 'C:\\Users\\yling\\WOS\\JOURNAL\\json\\'+field
    pathcsv = 'C:\\Users\\yling\\WOS\\JOURNAL\\reprint address\\'+field
    
    os.mkdir(pathcsv)
    
    journals = os.listdir(path)
    
    for journal in journals:
        print(field+':'+journal)
        with codecs.open(pathjson+'\\'+journal+'.json','r',encoding='utf8') as f:
            txt = f.read()
        papers = json.loads(txt)['papers']
        with codecs.open(pathcsv+'\\reprint address_'+journal+'.csv','w',encoding='utf8') as f:
            f.write('Title,ISSN,DOI,Reprint Address\n')
            for i in range(len(papers)):
                if 'Reprint Address:' in papers[i].keys():
                    for j in range(len(papers[i]['Reprint Address:'])):
                        f.write('"'+grab(papers[i],'Title:')+'",')
                        f.write('"'+grab(papers[i],'ISSN:')+'",')
                        f.write('"'+grab(papers[i],'DOI:')+'",')
                        f.write('"'+papers[i]['Reprint Address:'][j]+'"\n')
