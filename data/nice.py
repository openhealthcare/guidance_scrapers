import os, sys
import urllib, urllib2
import datetime
import json
import hashlib
from lxml import html
from xml.dom.minidom import Document

def parse_data( data ):
    items = []
    page = html.fromstring(data)
    table = page.cssselect(".contentInner table#row.table") [0]
    rows = table.cssselect('tr')
    for row in rows:
        cells = row.cssselect('td')
        if len(cells) != 4:
            continue
        code = cells[0].text_content()
        title = cells[1].text_content().strip().replace('\n','')
        date_issues = cells[2].text_content().strip()
        if 'replaced' in title or 'withdrawn' in title:
            continue
        link = ""
        print 'Processing', code
        pdfpage = "http://guidance.nice.org.uk/%s/QuickRefGuide/pdf/English" % (code,)
        pdfpagedata = None
        hc = hashlib.sha224(pdfpage).hexdigest()
        if os.path.exists( os.path.join('cache', hc)):
            print '  Using cached subpage '
            pdfpagedata = open(os.path.join('cache', hc)).read()
        else:
            print '  Using and caching subpage '
            pdfpagedata = urllib2.urlopen(pdfpage).read()
            with open(os.path.join('cache', hc), 'w') as f:
                f.write( pdfpagedata )
        pp = html.fromstring( pdfpagedata )
        links = pp.cssselect('a')
        for a in links:
            if code in a.text_content():
                link = 'http://guidance.nice.org.uk' + a.attrib.get('href')
        item = { 'title': title, 'code': code, 'issue_date' :date_issues, 'url':link }                
        if link:
            pdfhash = hashlib.sha224(pdfpage).hexdigest()
            p = os.path.join('pdfs', code ) + '.pdf'
            if not os.path.exists( p ):
                print '  Fetching PDF'
                urllib.urlretrieve (link, p.lower())
        else:
            continue
        items.append(item)
    with open('output.json','w') as f:
        json.dump( items, f)
 
    doc = Document()
    guidelines = doc.createElement("guidelines")
    doc.appendChild( guidelines )
    for item in items:
        node = doc.createElement("guide")
        titleNode = doc.createElement("title")
        titleText = doc.createTextNode(item['title'])
        titleNode.appendChild( titleText )
        
        urlNode = doc.createElement("url")
        urlText = doc.createTextNode(item['url'])
        urlNode.appendChild( urlText )
    
        node.appendChild( titleNode )
        node.appendChild( urlNode )
                
        guidelines.appendChild(node)
    
    with open('output.xml', 'w') as f:
        f.write( doc.toprettyxml(indent="  ") )
    
    # <?xml version="1.0" encoding="utf-8"?>
    #<guidelines>
    #<guide><title>Acutely ill patients in hospital</title><url>http://guidance.nice.org.uk/nicemedia/live/11810/35949/35949.pdf</url></guide>


url = "http://www.nice.org.uk/guidance/index.jsp?action=ByType&type=2&status=3&p=off"
if __name__ == '__main__':
    dt = datetime.datetime.now()
    thefile = '%s_%s.html' % ( dt.year, dt.month,)
    data = None

    if os.path.exists(thefile):
        print 'Using cached month file'
        with open(thefile,'r') as f:
            data = f.read()
    else:
        print 'Fetching and creating month file'
        data = urllib2.urlopen(url).read()
        with open(thefile,'w') as f:
            f.write( data )
        
    parse_data(data)
