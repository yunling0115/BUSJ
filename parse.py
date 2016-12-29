import os, re, codecs, json, sys
from bs4 import BeautifulSoup
sys.setrecursionlimit(10000)

keys_long = ['Cited References:','Addresses:','Author(s):','Reprint Address:']    
keys_wide = ['Title:','ISSN:','DOI:','Publisher:','Published:','Volume:','Issue:','Special Issue:','Source:','Conference Title:','Book DOI:','Total Times Cited:','Reprint Address:']

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

os.mkdir('C:\\Users\\yling\\WOS\\JOURNAL\\csv2')
os.mkdir('C:\\Users\\yling\\WOS\\JOURNAL\\json')

################################### START #####################################
allfields = ['_ACCOUNTING','_ECONOMICS','_ENTREPRENEURSHIP','_FINANCE','_INFORMATION','_INTERNATIONAL','_MANAGEMENT','_MARKETING','_PRACTITIONER']
for field in allfields:
    print(field)
    
    path = 'C:\\Users\\yling\\WOS\\JOURNAL\\'+field
    pathjson = 'C:\\Users\\yling\\WOS\\JOURNAL\\json\\'+field
    pathcsv = 'C:\\Users\\yling\\WOS\\JOURNAL\\csv2\\'+field
    journals = os.listdir(path)
    '''
    os.mkdir(pathcsv)
    
    os.mkdir(pathjson)
    '''
    
    for journal in journals:
        # create json
        
        print(field+':'+journal)
        pages = filter(lambda x: x.endswith('.htm'), os.listdir(path+'\\'+journal))
        pages = map(lambda x: int(x.strip('.htm')), pages)
        pages.sort()
        page = pages[0]
        journaltable = []
        for page in pages:
            print(page)
            with codecs.open(path+'\\'+journal+'\\'+str(page)+'.htm','r',encoding='utf8') as f:
                txt = f.read()
            soup = BeautifulSoup(txt, 'html.parser')
            tables = soup.find_all('table')
            tables = filter(lambda x: len(re.findall('Record.*?of', x.tr.text))>0, tables)
            for table in tables:
                dic = {}
                tds = reduce(lambda x,y: x+y, [[td for td in tr('td')] for tr in table('tr')])
                keys = reduce(lambda x,y: x+y, [[b.text for b in td('b')] for td in tds])
                index = keys.pop(0)
                for i in range(0,len(keys)):
                    if keys[i] in ['Cited References:', 'Addresses:', 'Reprint Address:']:
                        td = filter(lambda x: str(x.b)=='<b>'+keys[i]+'</b>', tds)
                        if len(td)>0:
                            td = td[0]
                            value = str(td).split('<br>')
                            value = map(lambda x: re.sub('<.*?>','',x), value)
                            value = map(lambda x: re.sub(keys[i],'',x).strip(), value)
                            value = map(lambda x: re.sub('\n',' ',x), value)
                            value = map(lambda x: re.sub('\s+',' ',x), value)
                            if keys[i]=='Addresses:':
                                authors = map(lambda x: findpattern('\[(.*?)\]',x), value)
                                addresses = map(lambda i: re.sub('\['+authors[i]+'\]','',value[i]).strip(), range(len(value)))
                                value = map(lambda i: map(lambda x: x.strip()+':'+addresses[i], authors[i].split(';')), range(len(value)))  
                                value = reduce(lambda x,y: x+y, value)
                            dic[keys[i]] = value     
                    else: 
                        beg = table.text.find(keys[i])
                        if i==len(keys)-1:
                            end = len(table.text)
                        else:
                            end = table.text.find(keys[i+1])
                        value = table.text[beg+len(keys[i]):end].strip()
                        dic[keys[i]] = value
                journaltable.append(dic)
        journaljson = {}
        journaljson['papers'] = journaltable
        with codecs.open(pathjson+'\\'+journal+'.json','w',encoding='utf8') as f:
            json.dump(journaljson, f)
        
        '''    
        # create csv
        print(field+':'+journal)
        with codecs.open(pathjson+'\\'+journal+'.json','r',encoding='utf8') as f:
            txt = f.read()
        papers = json.loads(txt)['papers']
        
        content_wide_write = '\n'.join(map(lambda x: '"'+'","'.join(map(lambda key: grab(x,key), keys_wide))+'"', papers))
        with codecs.open(pathcsv+'\\'+'_'.join(journal.strip('.json').split(' '))+'.csv', 'w', encoding='utf8') as f:
            f.write(','.join(keys_wide)+'\n')
            f.write(content_wide_write)
        
        for key in keys_long:
            key_write = re.sub('\(|\)','',key.strip(':'))    
            values = map(lambda x: grab(x,key), papers)
            if key=='Author(s):':
                values = map(lambda x: x.split(';'), values)
            content_long_write = map(lambda i: map(lambda x: '"'+grab(papers[i],'Title:')+'","'+grab(papers[i],'ISSN:')+'","'+grab(papers[i],'DOI:')+'","'+x.strip()+'"', values[i]), range(len(papers)))
            content_long_write = '\n'.join(reduce(lambda x, y: x+y, content_long_write))
            with codecs.open(pathcsv+'\\['+key_write+'] '+journal.strip('.json').strip()+'.csv', 'w', encoding='utf8') as f:
                f.write('Title,ISSN,DOI,'+key+'\n')
                f.write(content_long_write)          
        '''
    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             