from pathlib import Path
import subprocess,json,hashlib
from PIL import Image
r=Path(__file__).resolve().parents[1];a=r/'acquisition/extracted';a.mkdir(exist_ok=True)
for id,pages in [('D06',None),('D01',[3,4]),('D04',[62,63,238,245,253,260])]:
 for page in pages or [None]:
  prefix=a/(id+(f'-p{page}' if page else ''));cmd=['pdfimages']+(['-f',str(page),'-l',str(page)] if page else [])+['-png',str(r/'documents'/f'{id}.pdf'),str(prefix)];subprocess.run(cmd,check=True,stderr=subprocess.DEVNULL)
print([(p.name,Image.open(p).size) for p in a.glob('*.png') if Image.open(p).size!=(395,400) and min(Image.open(p).size)>100])
