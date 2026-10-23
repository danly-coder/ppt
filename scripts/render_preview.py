import os,shutil,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
lo=shutil.which('libreoffice') or shutil.which('soffice')
if not lo:sys.exit('LibreOffice missing; rendering did not run.')
try:
 import fitz
 from PIL import Image,ImageDraw,ImageFont
except ImportError:sys.exit('Install pymupdf and Pillow for render checks.')
out=R/'output/preview';out.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['XDG_CACHE_HOME']=str(R/'work/cache');Path(env['XDG_CACHE_HOME']).mkdir(parents=True,exist_ok=True)
subprocess.run([lo,'-env:UserInstallation=file://'+str(R/'work/lo-profile'),'--headless','--convert-to','pdf','--outdir',str(out),str(R/'output/ai-agent-harness-talk.pptx')],check=True,env=env)
pdf=out/'ai-agent-harness-talk.pdf';doc=fitz.open(pdf)
plan=json.loads((R/'content/slide_plan.json').read_text())['slides']
if len(doc)!=len(plan):sys.exit('Rendered page count mismatch')
report=[];thumbs=[]
for i,p in enumerate(doc):
 pix=p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False);pix.save(str(out/f'slide-{i+1:02}.png'))
 text=p.get_text();blocks=p.get_text('dict')['blocks'];span_count=sum(len(l['spans']) for b in blocks if 'lines' in b for l in b['lines'])
 off=[]
 for b in blocks:
  if 'lines' not in b:continue
  for line in b['lines']:
   for span in line['spans']:
    x0,y0,x1,y1=span['bbox']
    if x0<-.5 or y0<-.5 or x1>p.rect.width+.5 or y1>p.rect.height+.5:off.append(span['text'])
 normalize=lambda t:''.join(t.split())
 title_found=normalize(plan[i]['title']) in normalize(text)
 if not title_found:sys.exit(f'Title missing after rendering: {i+1}')
 if '\ufffd' in text:sys.exit(f'Replacement glyph in page {i+1}')
 if off:sys.exit(f'Off-page text in {i+1}: {off}')
 report.append(dict(slide=i+1,title_found=title_found,text_spans=span_count,off_page_text=off))
 im=Image.open(out/f'slide-{i+1:02}.png').convert('RGB');im.thumbnail((480,270));tile=Image.new('RGB',(500,306),'#e9edf3');tile.paste(im,(10,8));ImageDraw.Draw(tile).text((12,282),f'{i+1:02}',fill='#142238');thumbs.append(tile)
montage=Image.new('RGB',(500*4,306*((len(thumbs)+3)//4)),'#e9edf3')
for i,im in enumerate(thumbs):montage.paste(im,((i%4)*500,(i//4)*306))
montage.save(R/'output/montage.png')
(R/'output/render-check.json').write_text(json.dumps(dict(renderer='LibreOffice + PyMuPDF',pages=len(doc),checks=report,limitations='Text bounds are not an overlap/semantic correctness guarantee; visual inspection required.'),ensure_ascii=False,indent=2))
print(f'PASS: {len(doc)} rendered pages, titles present, no off-page text or replacement glyph; montage saved. Visual inspection required.')
