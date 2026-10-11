import urllib.request,json,pathlib,hashlib,re,concurrent.futures
r=pathlib.Path(__file__).resolve().parents[1];(r/'acquisition').mkdir(exist_ok=True)
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AxomRankResearch/1.0'}),timeout=60) as resp:return resp.read()
url='https://gyan.iitg.ac.in/server/api/core/bitstreams/bdf44f07-e5c5-42a4-8b35-ae4e8d12fd9f/content'
try:
 data=get(url)
 if not data.startswith(b'%PDF'):raise ValueError('Not PDF')
 (r/'documents/D04.pdf').write_bytes(data);print('Thesis downloaded',len(data),flush=True)
except Exception as e:print('Thesis',str(e),flush=True)
urls={'publisher':'https://link.springer.com/article/10.1007/s41826-022-00043-3','anu':'https://www.anu.edu.au/news/all-news/mysterious-giant-stone-jars-found-in-india','architexturez':'https://architexturez.net/file/nick-jars-4-jpg'}
for name,url in urls.items():
 try:(r/'acquisition'/f'{name}.html').write_bytes(get(url));print(name,'saved',flush=True)
 except Exception as e:print(name,str(e),flush=True)
html=(r/'acquisition/publisher.html').read_text() if (r/'acquisition/publisher.html').exists() else ''
links=sorted(set(re.findall(r'https://media\.springernature\.com/[^"<>\s]+',html)));links=[__import__('html').unescape(u) for u in links if 'Fig' in u];print(json.dumps(links),flush=True)
results=[]
for n in range(1,11):
 urls=[u for u in links if f'Fig{n}_' in u]
 if not urls:continue
 url=urls[0];id=f'JAR22-F{n:02}';d={'id':id,'url':url,'source':urls[0],'figure':n}
 try:
  data=get(url);p=r/'visuals'/f'{id}.png';p.write_bytes(data);d.update(status='downloaded',path=str(p.relative_to(r)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
 except Exception as e:d.update(status='failed',error=str(e))
 results.append(d)
(r/'acquisition/jar-figures.json').write_text(json.dumps(results,indent=2));print([(d['id'],d['status']) for d in results],flush=True)
