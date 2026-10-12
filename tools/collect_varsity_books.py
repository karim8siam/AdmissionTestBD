"""Collect BOU's published HSC reference index; never invent chapter mappings."""
import concurrent.futures,html,json,re,urllib.request,urllib.parse
from pathlib import Path
BASE='https://www.ebookbou.edu.bd/hsc.php'
def fetch(url):
    return urllib.request.urlopen(url,timeout=35).read().decode('utf-8','replace')
def plain(s):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s))).strip()
def links(s):return re.findall(r'<a\b[^>]*href=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)(?=</a>|<a\b)',s,re.S|re.I)
s=fetch(BASE).split('পুরাতন ভার্সন')[0]
books=[]
for href,label in links(s):
    title=plain(label)
    if not re.search('কোর্স কোড|Course Code',title):continue
    if any(x in title for x in ['পদার্থ','রসায়ন','জীববিজ্ঞান','উচ্চতর গণিত','গার্হস্থ্য','কৃষি']):continue
    url=urllib.parse.urljoin(BASE,href)
    if any(b['url']==url and b['title']==title for b in books):continue
    business=any(x in title for x in ['হিসাববিজ্ঞান','ব্যবসায়','ফিন্যান্স','বিপণন'])
    shared=any(x in title.lower() for x in ['বাংলা','english','তথ্য','অর্থনীতি'])
    books.append(dict(id='bou-'+str(len(books)+1),title=title,url=url,tracks=['humanities','business'] if shared else ['business' if business else 'humanities'],publisher='Bangladesh Open University',kind='supplementary_hsc',mapping_status='standard_hsc_mapping_pending',chapters=[]))
urls=sorted(set(b['url'].split('#')[0] for b in books if '.php' in b['url']))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    pages=dict(zip(urls,pool.map(fetch,urls)))
for b in books:
    if '.php' not in b['url']:continue
    doc=pages[b['url'].split('#')[0]]
    anchor=urllib.parse.urlsplit(b['url']).fragment
    if anchor:
        m=re.search(r'<div\s+id=[\"\']'+re.escape(anchor)+r'[\"\'][^>]*>(.*?)</div>',doc,re.S|re.I)
        if m:doc=m[1]
    else:
        # Select a table by course code when an index contains multiple books.
        code=re.search(r'[০-৯0-9]{4}',b['title'])
        tables=re.findall(r'<table\b[^>]*>(.*?)</table>',doc,re.S|re.I)
        match=[t for t in tables if code and code[0] in plain(t[:1500])]
        if match:doc=match[0]
        else:continue
    for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',doc,re.S|re.I):
        cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row,re.S|re.I)
        if len(cells)!=3 or 'ইউনিট-' not in plain(cells[0]):continue
        a=links(cells[0])
        if not a:continue
        b['chapters'].append(dict(title=plain(cells[1]),pages=plain(cells[2]),url=urllib.parse.urljoin(b['url'],a[0][0])))
Path('content/varsity_expansion/books.json').write_text(json.dumps(dict(checked_on='2026-10-12',source=BASE,license_note='BOU website states CC BY 4.0 unless otherwise specified. Links only; no textbook copies redistributed.',note='BOU modular HSC reference books. Standard NCTB edition/short-syllabus mapping is not yet complete.',books=books),ensure_ascii=False,indent=2))
print(len(books),'book references;',sum(len(b['chapters']) for b in books),'indexed reference units')
