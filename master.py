import os, re, string

# - run 'master1.imm'
# (1) get the list of journals
os.chdir('C:\\Users\\yling\\WOS\\_master')
files = os.listdir('.')
files = filter(lambda x: x.endswith('.htm'), files)
e = {} # valid
for filename in files:
    with open(filename) as f:
        txt = f.read().lower()
    try:
        qid = re.findall('qid=([0-9]+)',txt)[0]
        e[filename] = qid
    except:
        pass
os.chdir('C:\\Users\\yling\\WOS')
with open('JournalList-valid.csv','w') as f:
    f.write('\n'.join(['"'+key.strip('.htm').strip() for key in e.keys()]))
# create folders
os.chdir('C:\\Users\\yling\\WOS\\_journals')
folders = os.listdir('.')
[os.remove(f) for f in folders]
for filename in e.keys():
    os.makedirs(filename.strip('.htm'))

# - run 'master2.imm'    
# (2) get journal qid

    
# (3) write iim files
sid = 'Z1Gnwosw9gGntYZChWv' # fetch everyday
sid = '4Euh5lgsRNo1KzLhKSv'
os.chdir('C:\\Users\\yling\\Documents\\iMacros\\Macros\\WOS\\_journals')
files = os.listdir('.')
[os.remove(f) for f in files]
for filename in e.keys():
    qid = e[filename]
    folder = 'C:\\Users\yling\WOS\_journals\\' + re.sub(' ','<SP>',filename.strip('.htm').strip())
    with open(filename.strip('.htm').strip()+'.iim', 'w') as f:
        f.write('VERSION BUILD=8970419 RECORDER=FX\n')
        f.write('TAB T=1\n')
        f.write('TAB CLOSEALLOTHERS\n')
        f.write('SET !LOOP 1\n')
        f.write('URL GOTO=http://apps.webofknowledge.com.libproxy1.usc.edu/summary.do?product=WOS&colName=WOS&qid='+ qid + '&SID='+ sid + \
                '&search_mode=GeneralSearch&formValue(summary_mode)=GeneralSearch&update_back2search_link_param=yes&page={{!LOOP}}&pageSize=50\n')
        f.write('WAIT SECONDS=1\n')
        f.write('SAVEAS TYPE=CPL FOLDER=' + folder + ' FILE={{!LOOP}}')


