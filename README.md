Inspiration: 
[Scrapy Course – Python Web Scraping for Beginners](https://www.youtube.com/watch?v=mBoX_JCKZTE)  
Website to scrape: [BestWatch](https://bestwatch.com.hk/sale.html), [Strata](https://strata.ca) (WIP), 

Installation

```
python3.11 -m venv venv
source venv/bin/activate
pip install scrapy ipython
```

Configuration
```
# In scrapy.cfg:
shell = ipython

```

Practice area
```
scrapy shell

# Server side
fetch('http://strata.ca/')
response
response.css('div.listingTile')
response.css('div.listingTile').get()
listings = response.css('div.listingTile')
```