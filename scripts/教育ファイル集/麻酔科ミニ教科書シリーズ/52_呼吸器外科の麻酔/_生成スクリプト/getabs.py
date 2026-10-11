import sys, time, urllib.request, re
ids=sys.argv[1].split(',')
out=open(sys.argv[2],'a',encoding='utf-8')
for i in range(0,len(ids),10):
    ch=ids[i:i+10]
    u="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=abstract&retmode=text&id="+",".join(ch)
    t=urllib.request.urlopen(u,timeout=90).read().decode('utf-8')
    # drop author affiliation blocks
    t=re.sub(r'Author information:.*?\n\n','',t,flags=re.S)
    t=re.sub(r'Collaborators:.*?\n\n','',t,flags=re.S)
    out.write(t+'\n'); time.sleep(0.5)
