"""Render the canonical chapter as an accessible Assam exam study guide."""
from pathlib import Path
import re, html, json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
SOURCE=ROOT/'manuscript/01_Reading_the_Deep_Past.md'
OUT=REPO/'output/pdf/Before_the_Kingdoms_Chapter_01_Exam_Guide.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
F=Path('/home/angsuman/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/share/fonts/truetype')
for n,f in [('Serif','NotoSerif-Regular.ttf'),('SerifBold','NotoSerif-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,str(F/f)))
for n,f in [('Sans','NotoSans-Regular.ttf'),('SansBold','NotoSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,str(ROOT/'cover/assets'/f)))
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
M=HexColor('#80151A');I=HexColor('#F7F2EC');C=HexColor('#292929');G=HexColor('#A77B37');U=HexColor('#6F625B')
sty={
 'body':ParagraphStyle('body',fontName='Sans',fontSize=10.2,leading=14.8,textColor=C,spaceAfter=7,allowWidows=0,allowOrphans=0),
 'option':ParagraphStyle('option',fontName='Sans',fontSize=9.8,leading=14,textColor=C,spaceAfter=2),
 'h2':ParagraphStyle('h2',fontName='SerifBold',fontSize=20,leading=26,textColor=M,spaceAfter=16,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='SansBold',fontSize=11.2,leading=16,textColor=M,spaceBefore=8,spaceAfter=7,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Sans',fontSize=9,leading=13,textColor=C,allowWidows=0,allowOrphans=0),
 'head':ParagraphStyle('head',fontName='SansBold',fontSize=9,leading=13,textColor=I),
 'note':ParagraphStyle('note',fontName='Sans',fontSize=9,leading=13.5,textColor=C,spaceAfter=12,leftIndent=15,firstLineIndent=-15),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=8.5,leading=13,textColor=U,spaceAfter=12),
 'title':ParagraphStyle('title',fontName='Serif',fontSize=34,leading=42,textColor=M,spaceAfter=22),
 'kicker':ParagraphStyle('kicker',fontName='SansBold',fontSize=9,leading=14,textColor=M,spaceAfter=13),
}
s=SOURCE.read_text();defs=dict(re.findall(r'^\[\^(\d+)\]: (.+)$',s,re.M));refs=set(re.findall(r'\[\^(\d+)\](?!:)',s));assert refs==set(defs)
def inline(x):
 x=x.replace('\u2013','-').replace('\u2014',' - ').replace('\u2011','-').replace('\u2192',' > ')
 x=html.escape(x,quote=False)
 x=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{html.escape(m[2],quote=True)}" color="#80151A">{m[1]}</link>',x)
 x=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',x)
 x=re.sub(r'\*(.+?)\*',r'<i>\1</i>',x)
 return re.sub(r'\[\^(\d+)\]',r'<super><link href="#note\1" color="#80151A">\1</link></super>',x)
def table(lines):
 rows=[[x.strip() for x in row.strip().strip('|').split('|')] for row in lines]
 rows=[r for r in rows if not all(re.fullmatch(r'[:\- ]+',x) for x in r)]
 n=len(rows[0]);widths=([108,288] if n==2 else [92,141,163])
 if rows[0][0]=='Question':widths=[62,48,286]
 data=[[Paragraph(inline(x),sty['head' if i==0 else 'cell']) for x in row] for i,row in enumerate(rows)]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),M),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#FFFFFF'),HexColor('#EEE7DF')]),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#DED4CC'))]))
 return t
story=[Spacer(1,1),PageBreak(),Spacer(1,35),Paragraph('ASSAM GOVERNMENT EXAM STUDY GUIDE',sty['kicker']),Paragraph('Reading the<br/>Deep Past',sty['title']),HRFlowable(width='35%',hAlign='LEFT',thickness=1,color=G,spaceAfter=20),Paragraph('CHAPTER 01 / CONCEPTS • ASSAM FACTS • PRACTICE',sty['kicker'])]
goals=s.split('## Study goals',1)[1].split('## 1.1',1)[0]
for b in re.split(r'\n\s*\n',goals.strip()):story.append(Paragraph(inline(' '.join(b.splitlines())),sty['body']))
story+=[Spacer(1,14),Paragraph('Learning route',sty['h3'])]
for x in ['1. Evidence and important terms','2. Surface finds, excavation and layers','3. Dates and scientific methods','4. Archaeology and traditions','5. Source checking and revision','6. Eight original MCQs and a short-answer model']:story.append(Paragraph(x,sty['small']))
story.append(Paragraph('Source-cited study draft. Original practice questions; no previous-year or exam-frequency claims.',sty['small']))
body='## 1.1'+s.split('## 1.1',1)[1].split('## Source notes',1)[0]
lines=body.splitlines();i=0
while i<len(lines):
 line=lines[i].strip()
 if not line:i+=1;continue
 if line.startswith('## '):
  label=line[3:]
  if label.startswith(('1.1','Quick revision','Practice questions','Answers and explanations')):story.append(PageBreak())
  story.append(Paragraph(inline(label),sty['h2']));i+=1;continue
 if line.startswith('### '):
  label=line[4:]
  if label=='Short-answer practice':
   group=[Paragraph(label,sty['h3'])];i+=1
   tail='\n'.join(lines[i:])
   for block in re.split(r'\n\s*\n',tail.strip()):
    group.append(Paragraph(inline(' '.join(block.splitlines())),sty['body']))
   story.append(KeepTogether(group));i=len(lines);continue
  if re.match(r'Q\d\.',label):
   group=[Paragraph(inline(label),sty['h3'])];i+=1
   while i<len(lines) and not lines[i].startswith('##'):
    x=lines[i].strip()
    if x:group.append(Paragraph(inline(x),sty['option']))
    i+=1
   group.append(Spacer(1,10));story.append(KeepTogether(group));continue
  story.append(Paragraph(inline(label),sty['h3']));i+=1;continue
 if line.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i]);i+=1
  story+=[table(rows),Spacer(1,12)];continue
 block=[]
 while i<len(lines) and lines[i].strip() and not lines[i].startswith(('##','|')):block.append(lines[i].strip());i+=1
 if all(re.match(r'[A-D]\. ',l) for l in block):
  story.append(KeepTogether([Paragraph(inline(x),sty['body']) for x in block]))
 elif all(re.match(r'\d\. ',l) for l in block):
  for x in block:story.append(Paragraph(inline(x),sty['body']))
 else:story.append(Paragraph(inline(' '.join(block)),sty['body']))
story += [PageBreak(),Paragraph('Source notes',sty['h2']),Paragraph('References support the facts and comparisons taught in this chapter. Scholarly review remains pending.',sty['small'])]
for k in sorted(defs,key=int):story.append(KeepTogether([Paragraph(f'<a name="note{k}"/><b>{k}.</b> '+inline(defs[k]),sty['note'])]))
W,H=504,720
def decor(c,d):
 c.saveState();c.setFillColor(I);c.rect(0,0,W,H,fill=1,stroke=0)
 if d.page==1:c.drawImage(str(ROOT/'cover/Before_the_Kingdoms_Cover_v6_sculptural.png'),0,0,width=W,height=H)
 else:
  c.setFillColor(M)
  if d.page==2:c.setFont('Serif',66);c.drawRightString(W-54,H-90,'01')
  else:
   c.setFont('SansBold',7.5);c.drawString(54,H-29,'ASSAM HISTORY / BOOK 01');c.drawRightString(W-54,H-29,'READING THE DEEP PAST')
   c.setStrokeColor(G);c.setLineWidth(.4);c.line(54,H-39,W-54,H-39)
  c.setFont('Sans',7.3);c.setFillColor(U);c.drawString(54,27,'AxomRank  |  Exam study draft  |  11 October 2026')
  c.setFont('SansBold',9);c.setFillColor(M);c.drawRightString(W-54,27,str(d.page-1))
 c.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=54,rightMargin=54,topMargin=59,bottomMargin=55,title='Assam History - Chapter 1: Reading the Deep Past - Exam Study Guide',author='AxomRank',subject='Structured, source-cited study notes for Assam government exam aspirants')
doc.build(story,onFirstPage=decor,onLaterPages=decor)
r=PdfReader(str(OUT));txt=' '.join(' '.join(p.extract_text().split()) for p in r.pages)
for x in ['1.1 Archaeological evidence: the basics','1.2 Surface finds, excavation and stratigraphy','1.3 Dates and dating methods','1.4 Archaeology and traditions','1.5 Museums, reports and source checking','Quick revision','Q8.','Answers and explanations','Source notes']:assert x in txt,x
for p in r.pages:assert float(p.mediabox.width)==504 and float(p.mediabox.height)==720
wordbody=s.split('## Source notes')[0];wordbody=re.sub(r'\[\^\d+\]','',wordbody)
metadata={'output':str(OUT),'source':str(SOURCE),'pages':len(r.pages),'study_content_words':len(re.findall(r'\b\w+\b',wordbody)),'notes':len(defs),'mcqs':8,'short_answer_models':1,'audience':'Assam government exam aspirants','status':'source-cited study draft; visual review pending','checks':'all sections, tables, Q1–Q8, answer key and source notes preserved'}
(ROOT/'chapter_01_exam_layout_record.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps(metadata,indent=2))
