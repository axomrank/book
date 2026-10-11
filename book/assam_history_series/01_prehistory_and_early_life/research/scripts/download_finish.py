import urllib.request,urllib.parse,json,pathlib,hashlib,time
r=pathlib.Path(__file__).resolve().parents[1]
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AxomRankResearch/1.0'}),timeout=35) as response:return response.read()
media=json.loads((r/'media-downloads.json').read_text())
for id,f,ch,scope in [('M12','India Assam relief map.svg',[2,9],'Modern relief and state outline; neither prehistoric boundaries nor reconstructed river courses'),('M13','Lungzubel Meghalaya.JPG',[9,10],'Meghalaya regional comparison; modern photograph. Ancient maker, date and use remain unresolved')]:
 d={'id':id,'title':f,'chapters':ch,'scope':scope,'source':'https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(f)}
 try:
  info=next(iter(json.loads(get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','format':'json','titles':'File:'+f,'prop':'imageinfo','iiprop':'url|extmetadata'})))['query']['pages'].values()))['imageinfo'][0];d.update(original_url=info['url'],metadata=info['extmetadata']);data=get(info['url']);p=r/'visuals'/(id+pathlib.Path(urllib.parse.urlparse(info['url']).path).suffix);p.write_bytes(data);d.update(status='downloaded',path=str(p.relative_to(r)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e:d.update(status='failed',error=str(e))
 media.append(d)
for d in media:
 if d.get('status')=='failed' and '429' in d.get('error','') and d.get('original_url'):
  try:
   data=get(d['original_url']);p=r/'visuals'/(d['id']+pathlib.Path(urllib.parse.urlparse(d['original_url']).path).suffix);p.write_bytes(data);d.update(status='downloaded',path=str(p.relative_to(r)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest());d.pop('error',None)
  except Exception as e:d['retry_error']=str(e)
  time.sleep(2)
(r/'media-downloads.json').write_text(json.dumps(media,indent=2));print([(d['id'],d['status']) for d in media])
