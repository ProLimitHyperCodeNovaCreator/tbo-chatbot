import sys
sys.path.append('c:\\Users\\ayush\\Desktop\\tbo-chatbot\\hotel-search-engine')
from search_engine import HotelSearchEngine

engine = HotelSearchEngine()
res = engine._scrape_hotel_listings("hotels in Pune", 3)
print("Scraping results:", res)
