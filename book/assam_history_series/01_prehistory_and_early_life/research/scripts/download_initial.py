import urllib.request,json,pathlib,hashlib,concurrent.futures
root=pathlib.Path(__file__).resolve().parents[1]; root.mkdir(exist_ok=True)
items=[('D01','Daojali pottery luminescence dating','https://www.currentscience.ac.in/Volumes/113/03/0492.pdf'),('D02','Karbi Langpi ceramic explorations','https://www.heritageuniversityofkerala.com/JournalPDF/Volume7/43.pdf'),('D03','Man and Environment 1977 including Sarutaru report','https://ignca.gov.in/Asi_data/61362.pdf'),('D04','Digaru–Kolong archaeological thesis','https://gyan.iitg.ac.in/bitstreams/bdf44f07-e5c5-42a4-8b35-ae4e8d12fd9f/download'),('D05','IGNOU prehistoric archaeology teaching material','https://egyankosh.ac.in/bitstream/123456789/41364/1/MAN-002B7E.pdf')]
def fetch(x):
 id,title,url=x; d={'id':id,'title':title,'url':url,'rights':'Publicly accessible; reproduction permission unverified','read_status':'Downloaded; review pending'}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'AxomRank research catalogue (private scholarly research)'})
  with urllib.request.urlopen(req,timeout=90) as r: data=r.read(); d['final_url']=r.url
  if not data.startswith(b'%PDF'): raise ValueError('Response is not PDF')
  p=root/'documents'/f'{id}.pdf';p.parent.mkdir(exist_ok=True);p.write_bytes(data);d.update(path=str(p.relative_to(root)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status='downloaded')
 except Exception as e:d.update(status='failed',error=str(e))
 return d
out=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(fetch,items));(root/'downloads.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
