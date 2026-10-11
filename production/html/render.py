"""Render an editable HTML master without a browser. Requires WeasyPrint 70.0, pypdf."""
from pathlib import Path
from html.parser import HTMLParser
import argparse, json
from urllib.parse import unquote, urlsplit
from weasyprint import HTML
from pypdf import PdfReader

class Images(HTMLParser):
    def __init__(self):
        super().__init__(); self.paths=[]
    def handle_starttag(self, tag, attrs):
        if tag=='img': self.paths.append(dict(attrs).get('src',''))

def main():
    p=argparse.ArgumentParser();p.add_argument('html');p.add_argument('pdf');a=p.parse_args()
    source=Path(a.html).resolve();out=Path(a.pdf).resolve()
    content=source.read_text()
    if 'data-template="true"' in content:
        raise ValueError('Fill and review the template, then remove data-template before rendering.')
    parser=Images();parser.feed(content)
    for src in parser.paths:
        if not urlsplit(src).scheme and not (source.parent/unquote(src)).exists():
            raise FileNotFoundError(src)
    out.parent.mkdir(parents=True,exist_ok=True)
    doc=HTML(filename=str(source)).render();doc.write_pdf(str(out))
    reader=PdfReader(out)
    if not reader.pages: raise RuntimeError('Empty PDF')
    report={'html':str(source),'pdf':str(out),'pages':len(reader.pages),'image_count':len(parser.paths),'engine':'WeasyPrint 70.0','visual_review':'pending','publication_ready':False}
    out.with_suffix('.render.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
