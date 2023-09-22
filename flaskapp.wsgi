import sys
import logging
 
sys.path.insert(0, '/home/pedro_751806/FioDaMeada')
sys.path.insert(0, '/home/pedro_751806/FioDaMeada/env/Lib/site-packages/')
 
# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
 
# Import and run the Flask app
from app import app as application