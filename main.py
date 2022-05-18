from typing import Optional

import uvicorn
from fastapi import FastAPI

from scraper import (get_anchor_Links, get_scraped_table_data, insert_data,
                     load_driver_properties, load_page)

app = FastAPI()

@app.get("/run_scrapper")
def run_scrapper():
    driver = load_driver_properties()
    page_loader = load_page(driver)
    data_in_lists = get_anchor_Links(page_loader)
    scraped_data = get_scraped_table_data(data_in_lists, driver)
    insert_data(scraped_data)
    
    return {'status': 200, 'massage': 'code running completed'}
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
