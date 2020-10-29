import pandas as pd
from splinter.exceptions import ElementDoesNotExist
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import os
import time
import simplejson as json


def init_browser():
    json = FlaskJSON(mars_data)
    # Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit mars.nasa.gov latest news url site
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Latest article news title and description
    title_p = "NASA InSight's 'Mole' Is Out of Sight"
    paragraph_p = "Now that the heat probe is just below the Martian surface, InSight's arm will scoop some additional soil on top to help it keep digging so it can take Mars' temperature."

    # Featured image of Mars
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA24098_hires.jpg'

    # Mars Facts

    # Use Pandas to convert the data to a HTML table string.
    mars_url = "https://space-facts.com/mars/"
    
    facts_about_mars = pd.read_html(mars_url)

    mars_facts_df = facts_about_mars[0][1]
    mars_df = pd.DataFrame(mars_facts_df)

    mars_df.index = ["Equatorial Diameter", "Polar Diameter", "Mass", "Moons", "Orbt Distance", "Orbit Period",
                    "Surface Temperature", "First Record", "Recorded By"]
    mars_df.columns = ["About Mars"]

    mars_html = mars_df.to_html()

    # Clean up unwanted characters
    cleaned_mars_html = mars_html.replace('\n', '')

    mars_df.to_html('Mars_Facts.html')

    # First Mars Image: Cerberus
    first_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'

    # Second Mars Image: Schiaparelli
    second_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'

    # Third Mars Image: Syrtis
    third_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'

    # Fourth Mars Image: Valles
    fourth_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    # Append all data in the scraping and put individuals into list of dictionaries.
    mars_data = [
        title_p,
        paragraph_p,
        featured_image_url,
        mars_df,
        {"title": "Cerberus Hemisphere", "img_url": {first_img_Mars}},
        {"title": "Schiaparelli Hemisphere", "img_url": {second_img_Mars}},
        {"title": "Syrtis Major Hemisphere", "img_url": {third_img_Mars}},
        {"title": "Valles Marineris Hemisphere", "img_url": {fourth_img_Mars}}
    ]

    # Close the browser after scraping
    browser.quit()

    # Return results
    return json.load(mars_data)
