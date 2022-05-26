from typing import Optional

import uvicorn
from fastapi import FastAPI
from config import get_env

from models import (insert_data_usa_website, insert_data_canadian_website)

from scraper import (get_anchor_links_for_usa_website, get_scraped_table_data_of_usa_website,
                     load_driver_properties, load_page_for_usa_website, canadian_website_load_page, get_anchor_links_of_canadian_website)

app = FastAPI()
app_config = get_env()

# insert funciton need to be fixed and  called from models file

@app.get("/run_scrapper")
def run_scrapper():
    driver = load_driver_properties()
    page_loader = load_page_for_usa_website(driver)
    data_in_lists = get_anchor_links_for_usa_website(page_loader)
    scraped_data = get_scraped_table_data_of_usa_website(data_in_lists, driver)
    insert_data_usa_website(scraped_data)
    driver.quit()
    
    return {'status': 200, 'massage': 'code running completed'}
    


@app.get("/run_canadian_website_scrapper")
def run_scrapper():
    driver = load_driver_properties()
    page_loader = canadian_website_load_page(driver)
    scraped_data = get_anchor_links_of_canadian_website(page_loader, driver)
    insert_data_canadian_website(scraped_data)
    driver.quit()
    
    return {'status': 200, 'massage': 'code running completed'}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=get_env().APP_PORT, reload=True)
