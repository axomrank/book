"""Render the editable first chapter as a 7 x 10 inch reading PDF."""
from pathlib import Path
import re, html, json
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]
SOURCE=ROOT/'manuscript/01_How_We_Know_Ahom_History.md'
OUT=BASE/'output/pdf/Ahom_Volume_I_Chapter_01_7x10.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
FONT=Path('/home/angsuman/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/share/fonts/truetype')
for name,filename in [('Book','NotoSerif-Regular.ttf'),('BookBold','NotoSerif-Bold.ttf'),('BookItalic','NotoSerif-Italic.ttf'),('BookBoldItalic','NotoSerif-BoldItalic.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(FONT/filename)))
pdfmetrics.registerFontFamily('Book',normal='Book',bold='BookBold',italic='BookItalic',boldItalic='BookBoldItalic')
INK=HexColor('#202B2A'); GREEN=HexColor('#264B43'); MUTED=HexColor('#69736E'); RULE=HexColor('#BDAD85')
styles={
 'body':ParagraphStyle('body',fontName='Book',fontSize=11,leading=15.5,textColor=INK,alignment=TA_JUSTIFY,spaceAfter=8,allowWidows=0,allowOrphans=0),
 'section':ParagraphStyle('section',fontName='BookBold',fontSize=12.3,leading=17,textColor=GREEN,spaceBefore=13,spaceAfter=8,keepWithNext=True),
 'kicker':ParagraphStyle('kicker',fontName='BookBold',fontSize=9,leading=12,textColor=GREEN,spaceAfter=10),
 'title':ParagraphStyle('title',fontName='Book',fontSize=25,leading=31,textColor=INK,spaceAfter=14,keepWithNext=True),
 'subtitle':ParagraphStyle('subtitle',fontName='BookItalic',fontSize=10,leading=14,textColor=MUTED,spaceAfter=8),
 'draft':ParagraphStyle('draft',fontName='Book',fontSize=8.5,leading=12,textColor=MUTED,spaceAfter=18),
 'note':ParagraphStyle('note',fontName='Book',fontSize=9,leading=12.5,textColor=INK,spaceAfter=8,leftIndent=15,firstLineIndent=-15,allowWidows=0,allowOrphans=0),
}

text=SOURCE.read_text().split('## Development notes')[0]
definitions=dict(re.findall(r'^\[\^([^]]+)\]: (.+)$',text,re.M))
order=[]
for k in re.findall(r'\[\^([^]]+)\](?!:)',text):
 if k not in order: order.append(k)
numbers={k:i+1 for i,k in enumerate(order)}

def inline(raw):
 raw=raw.replace('\u2014',' - ').replace('\u2013','-').replace('\u2011','-')
 raw=re.sub(r'\[\^([^]]+)\]',lambda m:f'@@NOTE{numbers[m.group(1)]}@@',raw)
 escaped=html.escape(raw,quote=False)
 escaped=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{html.escape(m.group(2),quote=True)}" color="#264B43">{m.group(1)}</link>',escaped)
 escaped=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',escaped)
 escaped=re.sub(r'\*(.+?)\*',r'<i>\1</i>',escaped)
 return re.sub(r'@@NOTE(\d+)@@',r'<super><link href="#note\1" color="#264B43">\1</link></super>',escaped)

story=[Paragraph('VOLUME I / CHAPTER 1',styles['kicker']),Paragraph('How We Know<br/>Ahom History',styles['title']),Paragraph('Origins, Foundation, and Expansion to 1603',styles['subtitle']),Paragraph('Opening research draft - Version 0.1 - 10 October 2026<br/>Requires wider scholarly and manuscript comparison.',styles['draft']),HRFlowable(width='100%',thickness=0.6,color=RULE,spaceAfter=11)]
body=text.split('## 1.1',1)[1].split('## Notes',1)[0]
body='## 1.1'+body
for block in re.split(r'\n\s*\n',body.strip()):
 block=' '.join(block.splitlines())
 if block.startswith('## '): story.append(Paragraph(inline(block[3:]),styles['section']))
 else: story.append(Paragraph(inline(block),styles['body']))
story += [PageBreak(),Paragraph('Notes',styles['section']),HRFlowable(width='100%',thickness=0.6,color=RULE,spaceAfter=12)]
for k in order:
 n=numbers[k]
 story.append(Paragraph(f'<a name="note{n}"/><b>{n}.</b> '+inline(definitions[k]),styles['note']))

WIDTH,HEIGHT=504,720
def page_decor(c,doc):
 c.saveState()
 if doc.page>1:
  c.setFont('Book',8); c.setFillColor(MUTED)
  label='AHOM DYNASTY / VOLUME I' if doc.page%2==0 else 'HOW WE KNOW AHOM HISTORY'
  c.drawString(52,HEIGHT-33,label)
  c.setStrokeColor(RULE); c.setLineWidth(0.35); c.line(52,HEIGHT-41,WIDTH-52,HEIGHT-41)
 c.setFont('Book',7.5); c.setFillColor(MUTED)
 c.drawString(52,30,'Research draft / 10 October 2026')
 c.setFont('Book',9); c.setFillColor(INK); c.drawRightString(WIDTH-52,30,str(doc.page))
 c.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=(WIDTH,HEIGHT),rightMargin=52,leftMargin=52,topMargin=54,bottomMargin=52,title='Ahom Dynasty - Volume I - Chapter 1: How We Know Ahom History',author='Ahom History Book Project',subject='Chapter 1 reading proof, 7 x 10 inches; opening research draft',pageCompression=1)
doc.build(story,onFirstPage=page_decor,onLaterPages=page_decor)
reader=PdfReader(str(OUT))
metadata={'output':str(OUT),'source':str(SOURCE),'pages':len(reader.pages),'width_inches':7,'height_inches':10,'aspect_ratio':'7:10','body_font':'Noto Serif 11 pt','body_leading_pt':15.5,'notes':len(order),'development_notes_included':False,'page_boxes':[[float(p.mediabox.width),float(p.mediabox.height)] for p in reader.pages]}
(OUT.parent/'Ahom_Volume_I_Chapter_01_7x10_layout.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2))
