"""
rcog.py

Check the website of 
"""
import os, sys

from scraper import Scraper

import lxml.html
import lxml.etree
import urllib2
import urlparse

class RCOGScraper( Scraper ):
    
    base_url = 'http://www.rcog.org.uk/guidelines?filter=**ALL**' 
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    def run(self):
        print '+ Running RCOG Scraper'
        html = self.get_content(self.base_url)
        page = lxml.html.fromstring(html)
        table = page.cssselect( 'div.view-content-clinical-health-documents table')[0]
        for row in table.cssselect('tbody tr'):
            href = row[0][0]
            
            name = href.text_content()
            link = href.attrib.get('href')
            published = row[1].text_content()
            
            print name, link, published
        
        

if __name__ == '__main__':
    n = RCOGScraper()
    n.run()

