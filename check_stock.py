"""
Big W Stock Checker

Repeatedly check stock at Big W (http://www.bigw.com.au) for a given SKU near a given postcode. Useful
when you're waiting for something to come back into stock; run this script and check in on the output
from time to time to see when the product is available again.

This depends on an (undocumented) AJAX handler that could break at any time.

"""

import requests, time
from bs4 import BeautifulSoup

# How often to check stock levels.
DELAY_SECONDS = 500

# Your post code. Will return stock levels for any nearby stores.
# In this example: 3000 is Melbourne CBD.
POST_CODE = 3000

# The product SKU to check. Follows /p/ in the URL.
# In this example: https://www.bigw.com.au/product/eko-70-4k-ultra-hd-android-tv-with-google-assistant/p/116376/
SKU = 116376

# Format codes for pretty output on success.
class terminalColors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

# Initialize with user specified delay.
current_delay = DELAY_SECONDS

while True:
    try:
        r = requests.get('https://www.bigw.com.au/p/{}/ajaxlistavailablestores?locationQuery={}'
            .format(SKU, POST_CODE), timeout=5) 
        soup = BeautifulSoup(r.text, 'html.parser')
        if soup.strong:
            print (terminalColors.OKGREEN + "Product in stock near you!" + terminalColors.ENDC)
        else:
            print ("Product not in stock near you.")
        # Reset the wait time to match the user specified delay whenever we have a success.
        current_delay = DELAY_SECONDS

    except:
        # If something went wrong, back off exponentially.
        current_delay = current_delay * 2
        print ("Something went wrong. Backing off (current delay: {})".format(current_delay))

    time.sleep(current_delay)
