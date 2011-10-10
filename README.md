
NICE Scraper
============

What is it?
-----------

This is an extension of the original NICE scraper which is currently [hosted at ScraperWiki](https://scraperwiki.com/scrapers/nice_scraper/). Other tools that are part of this collection are for presentation of the data via a web browser using a [UI](https://views.scraperwiki.com/run/nice_html_view/) from the original scraper which was implemented by [Zarino](http://www.zarino.co.uk/)


How does it work?
-----------------

The scraper accesses the NICE website daily to check that the PDF files that we currently have are indeed the latest, and to also pull the new PDFs as they are added. Once we've determined if there is any new content we optionally regenerate the source JSON and HTML used to render the data to the client.


How do I install it?
--------------------

* git clone git://github.com/openhealthcare/nice_scraper.git
* cd nice_scraper
* virtualenv . --no-site-packages
* pip install -r requirements.txt
* ....