# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
import time


def scrape_all():
    # Inititate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # OR,
    # Replace the path with your actual path to the chromedriver
    # executable_path = {'executable_path': 'chromedriver.exe'}    
    # browser = Browser("chrome", **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results ina dictionary
    data = {
        "news_title": news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "facts":mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified":dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit mars.nasa.gov and get latest news title
    url = 'https://mars.nasa.gov/news/' 
    browser.visit(url)

    # Optional delay for loading the page
    time.sleep(1)

    # Convert the browser html to a soup object (in other terms, scrape page into Soup) and then quit the browser 
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try: 
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    # full_image_elem = browser.find_by_id('full_image')[0]
    # full_image_elem.click()

    # Find the more info button and click that
    # browser.is_element_not_present_by_text('more info', wait_time=1)
    # more_info_elem = browser.links.find_by_partial_text('more info')
    # more_info_elem.click()

    # Parse the result of the html with the soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find_all('img')[2]["src"]
        # print(img_url_rel)

    except AttributeError:
        return None

    # Use the base url to create an absolute url 
    # img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url = f'{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        mars_df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # assign columns and set index of dataframe
    mars_df.columns = ['Description', 'Mars']
    mars_df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return mars_df.to_html(classes="table table-striped")


def hemispheres(browser):
    # Set up the url - A way to break up long strings
    url = (
        "https://astrogeology.usgs.gov"
        "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )

    browser.visit(url)

    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):
        # Fine the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)
        # Finally, we navigate backwards
        browser.back()

    return hemisphere_image_urls


def scrape_hemisphere(html_text):
    # Parse html text
    hemi_soup = soup(html_text, "html.parser")

    # Adding try/except for error handling
    try: 
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        # Image error will return Non, for better front-end handling
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())



#########################################################
############### Old Code Below ##########################
#########################################################

# import pandas as pd
# from splinter.exceptions import ElementDoesNotExist
# from splinter import Browser
# from bs4 import BeautifulSoup as bs
# from flask import request
# import requests
# import os
# import time
# import simplejson as json



# def init_browser():
#     json = request.get_json()
#     # Replace the path with your actual path to the chromedriver
#     executable_path = {'executable_path': 'chromedriver.exe'}
#     return Browser('chrome', **executable_path, headless=False)


# def scrape_info():
#     browser = init_browser()

#     # Visit mars.nasa.gov latest news url site
#     url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
#     browser.visit(url)

#     time.sleep(1)

#     # Scrape page into Soup
#     html = browser.html
#     soup = bs(html, 'html.parser')

#     # Latest article news title and description
#     title_p = "NASA InSight's 'Mole' Is Out of Sight"
#     paragraph_p = "Now that the heat probe is just below the Martian surface, InSight's arm will scoop some additional soil on top to help it keep digging so it can take Mars' temperature."

#     # Featured image of Mars
#     featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA24098_hires.jpg'

#     # Mars Facts

#     # Use Pandas to convert the data to a HTML table string.
#     mars_url = "https://space-facts.com/mars/"
    
#     facts_about_mars = pd.read_html(mars_url)

#     mars_facts_df = facts_about_mars[0][1]
#     mars_df = pd.DataFrame(mars_facts_df)

#     mars_df.index = ["Equatorial Diameter", "Polar Diameter", "Mass", "Moons", "Orbt Distance", "Orbit Period",
#                     "Surface Temperature", "First Record", "Recorded By"]
#     mars_df.columns = ["About Mars"]

#     mars_html = mars_df.to_html()

#     # Clean up unwanted characters
#     mars_html.replace('\n', '')

#     mars_df.to_html('Mars_Facts.html')

#     # First Mars Image: Cerberus
#     first_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'

#     # Second Mars Image: Schiaparelli
#     second_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'

#     # Third Mars Image: Syrtis
#     third_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'

#     # Fourth Mars Image: Valles
#     fourth_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

#     # Append all data in the scraping and put individuals into list of dictionaries.
#     mars_data = [
#         title_p,
#         paragraph_p,
#         featured_image_url,
#         mars_df,
#         {"title": "Cerberus Hemisphere", "img_url": {first_img_Mars}},
#         {"title": "Schiaparelli Hemisphere", "img_url": {second_img_Mars}},
#         {"title": "Syrtis Major Hemisphere", "img_url": {third_img_Mars}},
#         {"title": "Valles Marineris Hemisphere", "img_url": {fourth_img_Mars}}
#     ]

#     # Close the browser after scraping
#     browser.quit()

#     # Return results
#     mars_data[0].encode('ascii','ignore').decode()
#     return mars_data
