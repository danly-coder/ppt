import json,re,zipfile,sys
from pathlib import Path
from xml.etree import ElementTree as ET
R=Path(__file__).resolve().parent.parent
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
plan=json.loads((R/'content/slide_plan.json').read_text())['slides'];errors=[]
for filename,expected in [('ai-agent-harness-talk.pptx',len(plan)),('architecture-diagrams.pptx',8)]:
 with zipfile.ZipFile(R/'output'/filename) as z:
  assert z.testzip() is None
  slides=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)])
  notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)]
  if len(slides)!=expected or len(notes)!=expected:errors.append(f'{filename}: slide/notes count mismatch')
  image_count=0;native_count=0
  for f in slides:
   el=ET.fromstring(z.read(f));image_count+=len(el.findall('.//p:pic',ns));native_count+=len(el.findall('.//p:sp',ns))
   for sp in el.findall('.//p:sp',ns):
    txt=''.join(sp.itertext());off=sp.find('.//a:xfrm/a:off',ns)
    if off is not None and int(off.attrib['y'])>6.5*914400 and int(off.attrib['x'])<2*914400 and ('AI 技术交流' in txt or 'AI交流会' in txt):errors.append('unwanted footer')
  if image_count:errors.append(f'{filename}: diagrams unexpectedly contain raster images')
  if native_count<100:errors.append(f'{filename}: missing native shapes')
  if filename.startswith('ai-agent'):
   for s in plan:
    el=ET.fromstring(z.read(f"ppt/notesSlides/notesSlide{s['id']}.xml"));txt=''.join(el.itertext())
    if s['notes'] not in txt or s['transition'] not in txt:errors.append(f"notes mismatch {s['id']}")
    for id in s['sources']:
     if id not in txt or 'https://' not in txt:errors.append(f"citation missing {s['id']}")
  print(f'{filename}: {len(slides)} slides, {len(notes)} notes, {native_count} native shapes, {image_count} raster images')
g=json.loads((R/'output/layout-geometry.json').read_text())
for e in g['elements']:
 if min(e['x'],e['y'],e['w'],e['h'])<0 or e['x']+e['w']>g['width']+.01 or e['y']+e['h']>g['height']+.01:errors.append(f'out of bounds: slide {e["slide"]}: {e.get("text",e["type"])}')
if errors:sys.exit('\n'.join(errors))
