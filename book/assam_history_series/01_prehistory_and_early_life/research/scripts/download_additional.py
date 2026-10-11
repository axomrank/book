import pathlib
exec(open(pathlib.Path(__file__).with_name('download_initial.py')).read().split('out=list(')[0])
items=[('D06','Assam stone jars overview 2019','https://www.jna.uni-kiel.de/index.php/jna/article/download/192/325/1576'),('D07','Gauhati University swamp pollen 2025','https://palaeobotanicalsociety.org/geophytology/vol55_1_2025/4.%20Trivedi%20et%20al.pdf'),('D08','Sakali wetland NPP study 2026','https://journals.sagepub.com/doi/pdf/10.1177/05529360251409913'),('D09','Holocene Lower Brahmaputra climate 2012','https://www.ias.ac.in/article/fulltext/jess/121/01/0135-0147'),('D10','Sarutaru and Neolithic traditions 1977','https://scholarspace.manoa.hawaii.edu/server/api/core/bitstreams/ce6eadd8-52da-4d22-8aab-f733db9e7596/content'),('D11','ASI field review 1966–67','https://nmma.nic.in/nmma/NAS1/nmma_doc/IAR/Indian%20Archaeology%201966-67%20A%20Review.pdf')]
old=json.loads((root/'downloads.json').read_text());out=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(fetch,items));(root/'downloads.json').write_text(json.dumps(old+out,indent=2));print(json.dumps(out,indent=2))
media=json.loads((root/'media-downloads.json').read_text())
for id,title,url,ch in [('M09','Ambari excavation — ASI photograph 1','https://asiguwahaticircle.gov.in/images/ambariexcavation.JPG',[11]),('M10','Ambari excavation — ASI photograph 2','https://asiguwahaticircle.gov.in/images/ambariexcavation2.jpg',[11]),('M11','Assam stone jar survey — publisher Figure 3','https://media.springernature.com/m312/springer-static/image/art%3A10.1007%2Fs41826-022-00043-3/MediaObjects/41826_2022_43_Fig3_HTML.png',[9,10])]:
 d={'id':id,'title':title,'source':url,'chapters':ch,'scope':'Research reference; caption and chronological association must be verified','rights':'Permission required; no open reuse license verified'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AxomRankResearch/1.0'}),timeout=60) as r:data=r.read()
  if data[:5].lower()==b'<!doc':raise ValueError('HTML instead of image')
  p=root/'visuals'/ (id+pathlib.Path(urllib.parse.urlparse(url).path).suffix.lower());p.parent.mkdir(exist_ok=True);p.write_bytes(data);d.update(path=str(p.relative_to(root)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status='downloaded')
 except Exception as e:d.update(status='failed',error=str(e))
 media.append(d)
(root/'media-downloads.json').write_text(json.dumps(media,indent=2))
