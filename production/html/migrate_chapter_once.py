"""One-time migration of the retained Chapter 01 draft. Future edits use HTML directly."""
from pathlib import Path
import re,html,json
ROOT=Path(__file__).resolve().parents[2]
B=ROOT/'book/assam_history_series/01_prehistory_and_early_life'
if (B/'manuscript/01_Reading_the_Deep_Past.html').exists():
    raise SystemExit('Migration already completed. Edit the HTML master directly; refusing to overwrite it.')
src=(B/'manuscript/01_Reading_the_Deep_Past.md').read_text()
def inline(s):
    s=html.escape(s)
    s=re.sub(r'\[\^(\d+)\]',r'<sup><a href="#note-\1">[\1]</a></sup>',s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s)
    return s
def convert(s):
    lines=s.splitlines();out=[];i=0
    while i<len(lines):
        l=lines[i]
        if not l.strip():i+=1;continue
        if l.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                row=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[-:]+',x) for x in row):rows.append(row)
                i+=1
            out.append('<table><thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>' for row in rows[1:])+'</tbody></table>');continue
        if l.startswith('### Q'):
            out.append('<div class="question"><h3>'+inline(l[4:])+'</h3>');i+=1
            while i<len(lines) and not lines[i].startswith('#'):
                if lines[i].strip():out.append('<p>'+inline(lines[i])+'</p>')
                i+=1
            out.append('</div>');continue
        if l.startswith('#'):
            n=len(l)-len(l.lstrip('#'));text=l[n:].strip();id=''
            m=re.match(r'1\.(\d)',text)
            if m:id=' id="B01-C01-D0'+m[1]+'"'
            cls=' class="revision"' if text=='Quick revision' else ' class="questions"' if text=='Practice questions' else ''
            out.append(f'<h{n}{id}{cls}>{inline(text)}</h{n}>');i+=1;continue
        if re.match(r'^\d+\. ',l):
            out.append('<ol>')
            while i<len(lines) and re.match(r'^\d+\. ',lines[i]):out.append('<li>'+inline(re.sub(r'^\d+\. ','',lines[i]))+'</li>');i+=1
            out.append('</ol>');continue
        paragraph=[l];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|')):paragraph.append(lines[i]);i+=1
        text=' '.join(paragraph);cls=' class="callout"' if text.startswith(('**Remember','**Common confusion','**Read correctly','**Exam pitfall','**Research caution')) else ''
        out.append('<p'+cls+'>'+inline(text)+'</p>')
    return '\n'.join(out)
body,notes=src.split('## Source notes',1)
body=body.split('## 1.1',1)[1];body='## 1.1'+body
body=convert(body)
fig='''<figure class="plate" id="B01-C01-F01"><div class="image-mat"><img src="../research/visuals/DJL17-F3B.png" alt="Published photograph of Daojali Hading stone celts, with source scale"></div><figcaption><span class="figure-tag">FIGURE 1.1 / DAOJALI HADING · ASSAM</span><br>Observe the range of tool forms and the source scale. Shape alone does not give a calendar date. Sharma and Singh (2017), figure 3, printed p.495 / PDF p.4; see note 2. Photograph date not independently established. Original image retained; reproduction clearance pending. Internal research proof.</figcaption></figure>'''
# Figure 3 is on printed p.495? Confirm source PDF header during visual QA and amend if needed.
body=body.replace('<h2 id="B01-C01-D02">',fig+'\n<h2 id="B01-C01-D02">')
fig2='''<figure class="plate" id="B01-C01-F02"><div class="image-mat"><img src="../research/visuals/DJL17-F2B.png" alt="Published photograph of Gawak Abri pottery panels with source scales"></div><figcaption><span class="figure-tag">FIGURE 1.2 / GAWAK ABRI · MEGHALAYA</span><br>A neighbouring comparison, not an Assam find. Retain object labels and source scale. Sharma and Singh (2017), figure 2, printed p.494 / PDF p.3; see note 2. Photograph date not independently established. Reproduction clearance pending. Internal research proof.</figcaption></figure>'''
body=body.replace('<h2 id="B01-C01-D04">',fig2+'\n<h2 id="B01-C01-D04">')
note_rows={int(n):t.strip() for n,t in re.findall(r'\[\^(\d+)\]: (.*?)(?=\n\n\[\^|\Z)',notes,re.S)}
note_html='<section class="notes"><h2>Source notes</h2><ol>'+''.join(f'<li id="note-{n}">{inline(note_rows[n])}</li>' for n in sorted(note_rows))+'</ol></section>'
opener='''<section class="opener" id="B01-C01"><img class="logo" src="../../../../production/html/assets/rang-ghar.png" alt="AxomRank Rang Ghar mark"><p class="kicker">BEFORE THE KINGDOMS / BOOK 01 / CHAPTER 01</p><h1 class="chapter-name">Reading the<br>Deep Past</h1><p class="deck">Learn to read an object, its context and its date before drawing a historical conclusion.</p><img class="hero" src="../../../../production/html/assets/reading-evidence-3d-v1.png" alt="Modern 3D conceptual illustration of archaeological study"><p class="small">Modern AI conceptual illustration. The objects are teaching props, not documented excavated finds.</p><div class="goals"><strong>What you will learn</strong><ul><li>Identify the main kinds of archaeological evidence.</li><li>Distinguish stratigraphic sequence from scientific dating.</li><li>Match Assam sites to their reported finds.</li><li>Separate traditions, observations and interpretations.</li></ul></div><p><strong>Study route:</strong> Concepts · site–find table · dating comparisons · rapid revision · original questions.</p><p class="small">Layout proof of the existing draft. Regional evidence review is in progress; this chapter is not editorially approved.</p></section>'''
page='<!doctype html><html lang="en"><meta charset="utf-8"><title>Reading the Deep Past | AxomRank</title><link rel="stylesheet" href="../../../../production/html/book.css"><body><nav class="screen-nav"><a href="../../../../production/html/CHAPTER_DESIGN_PLAN.html">Design plan</a><a href="../research/regional/index.html">Regional research</a></nav><main class="book">'+opener+body+note_html+'</main></body></html>'
(B/'manuscript/01_Reading_the_Deep_Past.html').write_text(page)
print('Migrated chapter; future production reads HTML directly.')
