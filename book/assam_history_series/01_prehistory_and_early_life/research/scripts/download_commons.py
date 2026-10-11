import urllib.request,urllib.parse,json,pathlib,hashlib,re,time
root=pathlib.Path(__file__).resolve().parents[1];out=[]
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AxomRankResearch/1.0 (historical research catalogue)'}),timeout=60) as r:return r.read()
files=['Ambari excavations in Guwahati, Assam '+str(i)+'.jpg' for i in range(1,5)]+['Base of a rouletted ware, terracotta.jpg','Potsherd of a Roman Rouletted Ware, terracotta.jpg','Rim part of a Roman Rouletted Ware, terracotta.jpg','Roman Rouletted Potsherd, Terracotta.jpg']
for i,f in enumerate(files):
 d={'id':f'M{i+1:02}','title':f,'source':'https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(f),'chapters':[11],'scope':'Ambari transition context; object identification and date require excavation verification'}
 try:
  url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','format':'json','titles':'File:'+f,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':800})
  raw=json.loads(get(url)); info=next(iter(raw['query']['pages'].values()))['imageinfo'][0]; d.update(original_url=info['url'],metadata=info.get('extmetadata',{}));data=get(info['url']);p=root/'visuals'/('M%02d'% (i+1)+pathlib.Path(urllib.parse.urlparse(info['url']).path).suffix);p.parent.mkdir(exist_ok=True);p.write_bytes(data);d.update(path=str(p.relative_to(root)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),status='downloaded')
 except Exception as e:d.update(status='failed',error=str(e))
 out.append(d);print(d['id'],d['status'],flush=True);time.sleep(1)
(root/'media-downloads.json').write_text(json.dumps(out,indent=2))
