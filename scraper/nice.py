"""
nice_checker.py

Checks the NICE site to work out whether there are any changes to the PDFs.
If not running on ScraperWiki then download the PDFs locally and regenerate
the JSON file that describes all of the content. For ScraperWiki we can use
the API to fetch the data as JSON when we need it.

TODO:
    * Tidy code
    * Check if the scraper is running on ScraperWiki or not and save data 
      appropriately

Source code originally from https://scraperwiki.com/scrapers/nice_scraper/
"""
import os, sys

from scraper import Scraper

import lxml.html
import lxml.etree
import urllib2
import urlparse

class NiceScraper( Scraper ):
    
    base_url = 'http://www.nice.org.uk/guidance/index.jsp?action=ByType&type=2&status=3&p=off' 
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    def run(self):
        print '+ Running NICE Scraper'
        
        print '+ Fetching base page'        
        html = self.get_content(self.base_url)
        #print html
        root = lxml.html.fromstring(html)
        rows = root.cssselect("table#row tr")
        headers = [ th.text_content().strip()  for th in rows[0] ]
        assert headers == ['Ref', 'Title', 'Date Issued', 'Review'], headers
        
        for n, row in enumerate(rows[1:]):
            assert row[1][0].tag == "a", lxml.html.tostring(row)
            data = dict(zip(headers, [ td.text_content().strip()  for td in row ]))
            data["link"] = row[1][0].attrib.get("href")
            data['Date Issued'] = self.month_date(data['Date Issued'])
            if data['Review'] in ["", "TBC"]:
                data.pop('Review')
            else:
                data['Review'] = self.month_date(data['Review'])
            data["rownumber"] = n
            pdata = self.guide_from_page(data["link"])
            data.update(pdata)
            
            print data
#            scraperwiki.sqlite.save(["rownumber"], data)


    def month_date(self, d):
        return "%s-%02d" % (d[4:], self.months.index(d[:3])+1)

    def get_direct_pdf(self, durl):
        html = self.get_content(durl)
        root = lxml.html.fromstring(html)
        dlink =root.cssselect("div.contentInner a#hyperlink")
        return urlparse.urljoin(durl, dlink[0].attrib.get("href"))

    def get_headings_from_pdf(self, pdfurl):
        return ""
        
#        pdfdata = urllib2.urlopen(pdfurl).read()
#        pdfxml = scraperwiki.pdftoxml(pdfdata)
#        root = lxml.etree.fromstring(pdfxml)
    
#        ldata = [ ]
#        for page in root:
#            for el in page:
                    # needs also to do concatenation between headings that run to two lines, 
                    # and handle headings with italics in them <i>
#                if el.tag == "text" and el.attrib.get("font") == "10" and len(el) == 1 and el[0].tag == "b":
#                    data = {"pdfurl":pdfurl, "pagenumber":int(page.attrib.get("number")), "heading":el[0].text}
#                    ldata.append(data)
#        scraperwiki.sqlite.save(["pdfurl", "pagenumber", "heading"], ldata, "subheadings")


    def guide_from_page(self, purl):
        print '+ Getting guide from ' + purl
        phtml = self.get_content(purl)
        proot = lxml.html.fromstring(phtml)
        uloptions = proot.cssselect("div.guidance-content ul.options")
        pdata = { }
        for li in uloptions[0].cssselect("li"):
            if not li.text:
                continue
            key = li.text.strip()
            if key == 'No documents found':
                continue
            if key in ['Full guideline', 'Distribution List']:
                continue
            assert key in ["NICE guidance written for patients and carers", 'Quick reference guide', 'NICE guideline', 'Full guideline'], key
            for a in li:
                assert a.tag == "a"
                format = a.text.strip()
                if format == "Fformat MS Word":
                    continue
                if format == "documents":
                    continue
                assert format in ["PDF format", "MS Word format"], format
                ckey = "%s - %s" % (key, format[:-7])
                dpdf = a.attrib.get("href")  # holding page
                pdata[ckey] = dpdf
                if format == "PDF format":
                    pdfurl = self.get_direct_pdf(dpdf)
                    pdata[key+" - PDF"] = pdfurl
                    self.get_headings_from_pdf(pdfurl)

        return pdata

if __name__ == '__main__':
    n = NiceScraper()
    n.run()

"""





#Quick reference guide - PDF

Main()
"""