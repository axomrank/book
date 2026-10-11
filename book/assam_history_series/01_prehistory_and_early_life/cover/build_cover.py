from pathlib import Path
import base64,html,json,shutil
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PIL import Image
root=Path(__file__).resolve().parent; workspace=root.parents[4];brand=workspace/'Social_Media_asset/brand-kit/v1';asset=root/'artwork-v1.png'
for name in ['NotoSans-Regular.ttf','NotoSans-Bold.ttf','OFL.txt','DISTRIBUTION-COPYRIGHT.txt']:shutil.copyfile(brand/'fonts'/name,root/'assets'/name)
shutil.copyfile(brand/'logo/png/rang-ghar-master-2048.png',root/'assets/rang-ghar.png')
pdfmetrics.registerFont(TTFont('Noto',str(root/'assets/NotoSans-Regular.ttf')));pdfmetrics.registerFont(TTFont('NotoBold',str(root/'assets/NotoSans-Bold.ttf')))
W,H=504,720;maroon='#80151A';ivory='#F7F2EC';charcoal='#292929';gold='#A77B37'
text=[('AxomRank',96,677,16,'NotoBold',maroon),('ASSAM: A HISTORY OF ITS LAND AND PEOPLE',42,646,8.5,'Noto',charcoal),('BEFORE THE',40,585,44,'NotoBold',maroon),('KINGDOMS',38,529,59,'NotoBold',maroon),('Prehistory and Early Life in Assam',42,491,15.5,'Noto',charcoal)]
for s,x,y,size,font,col in text:
 assert x+pdfmetrics.stringWidth(s,font,size)<=W-30,(s,pdfmetrics.stringWidth(s,font,size))
pdf=root/'Before_the_Kingdoms_Cover_v1_7x10.pdf';c=Canvas(str(pdf),pagesize=(W,H));c.setTitle('Before the Kingdoms: Prehistory and Early Life in Assam');c.setAuthor('AxomRank');c.setSubject('Book 01 front cover design proof; modern illustrative artwork');c.setFillColor(HexColor(ivory));c.rect(0,0,W,H,fill=1,stroke=0)
# Native document layout: artwork is embedded intact, with proportional letterboxing if necessary.
im=Image.open(asset);iw,ih=im.size;scale=min(W/iw,432/ih);aw,ah=iw*scale,ih*scale;ax=(W-aw)/2;ay=32+(432-ah)/2;c.drawImage(ImageReader(str(asset)),ax,ay,width=aw,height=ah,mask='auto')
logo=root/'assets/rang-ghar.png';lw,lh=Image.open(logo).size;logo_w=42;logo_h=logo_w*lh/lw;c.drawImage(str(logo),42,671,width=logo_w,height=logo_h,mask='auto')
for s,x,y,size,font,col in text:c.setFillColor(HexColor(col));c.setFont(font,size);c.drawString(x,y,s)
c.setStrokeColor(HexColor(gold));c.setLineWidth(.7);c.line(42,473,86,473);c.setFillColor(HexColor(maroon));c.setFont('NotoBold',7.5);c.drawString(42,17,'BOOK 01');c.setFillColor(HexColor(charcoal));c.setFont('Noto',7.5);c.drawRightString(462,17,'AxomRank History Series');c.showPage();c.save()
# Editable native SVG mirrors the proof; typography, logo and artwork remain separate elements.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="7in" height="10in" viewBox="0 0 504 720">','<defs><style>@font-face{font-family:Noto;src:url(assets/NotoSans-Regular.ttf)}@font-face{font-family:Noto;src:url(assets/NotoSans-Bold.ttf);font-weight:700}</style></defs>',f'<rect width="504" height="720" fill="{ivory}"/>',f'<image href="artwork-v1.png" x="{ax}" y="{H-ay-ah}" width="{aw}" height="{ah}"/>',f'<image href="assets/rang-ghar.png" x="42" y="{H-671-logo_h}" width="42" height="{logo_h}"/>']
for s,x,y,size,font,col in text:svg.append(f'<text x="{x}" y="{H-y}" font-family="Noto" font-size="{size}" font-weight="{700 if font=="NotoBold" else 400}" fill="{col}">{html.escape(s)}</text>')
svg += [f'<path d="M42 247H86" stroke="{gold}" stroke-width=".7"/>',f'<text x="42" y="703" font-family="Noto" font-size="7.5" font-weight="700" fill="{maroon}">BOOK 01</text>',f'<text x="462" y="703" text-anchor="end" font-family="Noto" font-size="7.5" fill="{charcoal}">AxomRank History Series</text>','</svg>'];(root/'Before_the_Kingdoms_Cover_v1.svg').write_text('\n'.join(svg)+'\n')
(root/'layout_record.json').write_text(json.dumps({'trim_inches':[7,10],'pdf_points':[504,720],'artwork_pixels':[iw,ih],'artwork_placement_points':[ax,ay,aw,ah],'fonts':['NotoSans-Regular','NotoSans-Bold'],'status':'Front cover design proof; printer bleed/profile/spine not specified','original_logo_preserved':True,'author_credit':'No personal author supplied; none invented'},indent=2)+'\n');print(str(pdf))
