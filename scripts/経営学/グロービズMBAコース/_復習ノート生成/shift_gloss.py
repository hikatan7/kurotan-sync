import re,sys
f,delta=sys.argv[1],int(sys.argv[2])
s=open(f,encoding='utf-8').read()
g0=s.index('glossary=')
head,gl=s[:g0],s[g0:]
def sh(m):
    pg=m.group(2)
    new=re.sub(r'\d+',lambda n:str(int(n.group())+delta),pg)
    return m.group(1)+new+m.group(3)
gl2,n=re.subn(r'(\("[^"\n]*", "[^"\n]*", "[^"\n]*", ")([0-9,\s–\-]+)("\),)',sh,gl)
open(f,'w',encoding='utf-8').write(head+gl2); print(f,n)
