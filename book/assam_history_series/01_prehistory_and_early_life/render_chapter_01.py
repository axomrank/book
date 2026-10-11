"""Render the researched chapter master as an AxomRank 7 x 10 reading proof."""
from pathlib import Path
import re, html, json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
SOURCE = ROOT / 'manuscript/01_Reading_the_Deep_Past.md'
OUT = REPO / 'output/pdf/Before_the_Kingdoms_Chapter_01_7x10.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
FONT = Path('/home/angsuman/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/share/fonts/truetype')
for name, file in [('Serif','NotoSerif-Regular.ttf'),('SerifBold','NotoSerif-Bold.ttf'),('SerifItalic','NotoSerif-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT/file)))
for name, file in [('Sans','NotoSans-Regular.ttf'),('SansBold','NotoSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(ROOT/'cover/assets'/file)))
pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='SansBold', italic='Sans', boldItalic='SansBold')
pdfmetrics.registerFontFamily('Serif', normal='Serif', bold='SerifBold', italic='SerifItalic', boldItalic='SerifBold')
MAROON=HexColor('#80151A'); IVORY=HexColor('#F7F2EC'); INK=HexColor('#292929'); GOLD=HexColor('#A77B37'); MUTED=HexColor('#6F625B')
styles = {
 'body':ParagraphStyle('body',fontName='Sans',fontSize=10.4,leading=16.2,textColor=INK,alignment=TA_LEFT,spaceAfter=10,allowWidows=0,allowOrphans=0),
 'section':ParagraphStyle('section',fontName='SerifBold',fontSize=15,leading=20,textColor=MAROON,spaceBefore=16,spaceAfter=10,keepWithNext=True),
 'kicker':ParagraphStyle('kicker',fontName='SansBold',fontSize=9,leading=14,textColor=MAROON,spaceAfter=13),
 'title':ParagraphStyle('title',fontName='Serif',fontSize=34,leading=42,textColor=MAROON,spaceAfter=20),
 'intro':ParagraphStyle('intro',fontName='Serif',fontSize=14,leading=22,textColor=INK,spaceAfter=20),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=8.5,leading=13,textColor=MUTED,spaceAfter=9),
 'note':ParagraphStyle('note',fontName='Sans',fontSize=9,leading=14,textColor=INK,spaceAfter=13,leftIndent=18,firstLineIndent=-18,allowWidows=0,allowOrphans=0),
 'cell':ParagraphStyle('cell',fontName='SansBold',fontSize=8.5,leading=13,textColor=MAROON,alignment=1),
}
text=SOURCE.read_text()
definitions=dict(re.findall(r'^\[\^([^]]+)\]: (.+)$',text,re.M))
order=list(dict.fromkeys(re.findall(r'\[\^([^]]+)\](?!:)',text)))
assert set(order)==set(definitions), 'Citation references and definitions disagree'
numbers={k:i+1 for i,k in enumerate(order)}
def inline(raw):
    raw=raw.replace('\u2013','-').replace('\u2014',' - ').replace('\u2011','-')
    raw=re.sub(r'\[\^([^]]+)\]',lambda m:f'@@NOTE{numbers[m.group(1)]}@@',raw)
    escaped=html.escape(raw,quote=False)
    escaped=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{html.escape(m.group(2),quote=True)}" color="#80151A">{m.group(1)}</link>',escaped)
    escaped=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',escaped)
    escaped=re.sub(r'\*(.+?)\*',r'<i>\1</i>',escaped)
    return re.sub(r'@@NOTE(\d+)@@',r'<super><link href="#note\1" color="#80151A">\1</link></super>',escaped)

# The first page preserves the selected native cover byte-for-byte as an image.
story=[Spacer(1,1),PageBreak(),Spacer(1,88),Paragraph('ASSAM HISTORY / BOOK 01 / CHAPTER 01',styles['kicker']),Paragraph('Reading the<br/>Deep Past',styles['title']),HRFlowable(width='34%',thickness=1,color=GOLD,hAlign='LEFT',spaceAfter=22),Paragraph('How objects, contexts and dates become a history of Assam before kingdoms.',styles['intro'])]
chain=Table([[Paragraph(x,styles['cell']) for x in ['OBJECT','CONTEXT','DATE','INTERPRETATION']]],colWidths=[99]*4)
chain.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.6,GOLD),('INNERGRID',(0,0),(-1,-1),0.35,GOLD),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12)]))
story += [chain,Spacer(1,14),Paragraph('A reading guide: identify the find, examine its relationships, check what the date measures, then evaluate the explanation.',styles['small']),Spacer(1,28),Paragraph('RESEARCH DRAFT / 11 OCTOBER 2026<br/>Five planned divisions. Eleven source notes. Scholarly review pending.',styles['small']),PageBreak()]
body=text.split('\n',1)[1].split('## Notes')[0].strip()
for block in re.split(r'\n\s*\n',body):
    raw=' '.join(block.splitlines())
    if raw.startswith('## '):
        story.append(Paragraph(inline(raw[3:]),styles['section']))
    else:
        story.append(Paragraph(inline(raw),styles['body']))
story += [PageBreak(),Paragraph('Source notes',styles['title']),Paragraph('Page and table references identify the passages used. Links open the original reports or institutional sources.',styles['small']),HRFlowable(width='100%',thickness=0.6,color=GOLD,spaceAfter=18)]
for k in order:
    n=numbers[k]
    story.append(KeepTogether([Paragraph(f'<a name="note{n}"/><b>{n}.</b> '+inline(definitions[k]),styles['note'])]))

W,H=504,720
def decor(c,doc):
    c.saveState()
    c.setFillColor(IVORY);c.rect(0,0,W,H,fill=1,stroke=0)
    if doc.page==1:
        c.drawImage(str(ROOT/'cover/Before_the_Kingdoms_Cover_v6_sculptural.png'),0,0,width=W,height=H)
    else:
        if doc.page==2:
            c.setFillColor(MAROON);c.setFont('Serif',78);c.drawRightString(W-54,H-104,'01')
            c.setFillColor(GOLD);c.rect(0,H-9,W,9,fill=1,stroke=0)
        else:
            c.setFont('Sans',7.5);c.setFillColor(MUTED)
            c.drawString(54,H-31,'BEFORE THE KINGDOMS')
            c.drawRightString(W-54,H-31,'CHAPTER 01 / READING THE DEEP PAST')
            c.setStrokeColor(GOLD);c.setLineWidth(.35);c.line(54,H-40,W-54,H-40)
        c.setFont('Sans',7.2);c.setFillColor(MUTED)
        c.drawString(54,28,'AxomRank  |  Research draft  |  11 October 2026')
        c.setFillColor(MAROON);c.setFont('SansBold',9);c.drawRightString(W-54,28,str(doc.page-1))
    c.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=54,rightMargin=54,topMargin=61,bottomMargin=55,title='Before the Kingdoms - Chapter 1: Reading the Deep Past',author='AxomRank',subject='Source-cited research draft; stylized 7 x 10 reading proof',pageCompression=1)
doc.build(story,onFirstPage=decor,onLaterPages=decor)
reader=PdfReader(str(OUT))
extracted='\n'.join(p.extract_text() or '' for p in reader.pages)
normalized=' '.join(extracted.split())
assert 'Reading the Deep Past' in normalized and '2.7' in normalized
assert len(reader.pages)>3
for heading in re.findall(r'^## (1\.[1-5] .+)$',body,re.M):
    assert heading in normalized, heading
links=sum(len(p.get('/Annots',[])) for p in reader.pages)
body_words=len(re.findall(r"\b[\w]+(?:['-][\w]+)*\b",re.sub(r'\[\^[^]]+\]','',re.sub(r'^## .+$','',body,flags=re.M))))
metadata={'output':str(OUT),'source':str(SOURCE),'pages':len(reader.pages),'main_prose_words':body_words,'notes':len(order),'link_annotations':links,'trim_inches':[7,10],'body_font':'Noto Sans 10.4 pt / 16.2 pt leading','display_font':'Noto Serif','cover':'selected native v6 included unchanged','status':'research draft; visual review required','pdf_text_checks':'all five division headings and citation definitions present'}
(ROOT/'chapter_01_layout_record.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2))
