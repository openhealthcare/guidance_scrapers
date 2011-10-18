import os, sys
from optparse import OptionParser
from ConfigParser import ConfigParser
import urllib2
import urlparse


class Scraper(object):
    
    def __init__(self, *args, **kwargs):
        parser = OptionParser()
        parser.add_option("-c", "--config", dest="config",
                          help="Path to the configuration file", metavar="FILE")
        parser.add_option("-v", "--verbose",
                          action="store_true", dest="verbose", default=False,
                          help="Write verbose output")                  
        (self.settings, args) = parser.parse_args()
        self.load_config()

    def load_config(self):
        if (not self.settings.config) or (not os.path.exists(self.settings.config)):
            print """
                    Can't run unless we have a config file
                    Please specify the path to the file with the -c option\n"""
            
            sys.exit(1)

        config = ConfigParser()
        config.readfp( open( self.settings.config ) )

        output_folder = config.get('scraper_settings', 'pdf_output')
        output_folder = os.path.join( os.path.dirname(__file__), output_folder)
        output_folder = os.path.abspath(output_folder)
        if self.settings.verbose:
            print 'Will save output files to %s' % (output_folder,)
        self.settings.output_folder = output_folder
        
    def get_content(self, url):
        return urllib2.urlopen(url).read()
    