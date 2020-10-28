#!/usr/bin/env python
# coding: utf-8

# # Step 1 - Scraping

# ### Part.1 : NASA Mars News
# 

# In[1]:


# import dependencies 
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os


# In[2]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)


# In[4]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[5]:


soup


# In[6]:


latest_articles = soup.find_all('div', class_='list_text')
latest_articles


# In[7]:


# collect the latest News Title and Paragraph Text.

# Loop through returned latest_articles
for latest_article in latest_articles:
    
    # Retrieve the news title
    title = latest_article.find('div', class_='content_title')
    
    
    # Access the news text content
    news_title = title.a.text
#     print(news_title)

    try:
        # Access the paragraph text
        paragraph = latest_article.find('div', class_='article_teaser_body').text    

        # Access the href attribute with bracket notation
        title_link = title.a['href']

        print('\n-----------------\n')
        print(news_title)
        print('Description:', paragraph)
        print('Link:', title_link)
        
    except AttributeError as e:
        print(e)


# In[8]:


# variable reference for news title and paragraph
title_p = "NASA InSight's 'Mole' Is Out of Sight"
paragraph_p = "Now that the heat probe is just below the Martian surface, InSight's arm will scoop some additional soil on top to help it keep digging so it can take Mars' temperature."


# ### Part 2 : JPL Mars Space Images - Featured Image

# In[9]:


# Use splinter to navigate the site and find the image url for the current Featured Mars Image 
# and assign the url string to a variable called featured_image_url.

# Make sure to find the image url to the full size .jpg image.

# Make sure to save a complete url string for this image.


# In[10]:


from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup


# In[11]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[12]:


featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(featured_url)


# In[13]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[14]:


featured_images = soup.find_all('ul', class_='articles')


# In[15]:


featured_images


# In[16]:


# collect the featured image urls

featured_images = soup.find('ul', class_='articles')

image_url = featured_images.find_all('li')

url_list = []
title_list = []

for image in image_url:
    fimg_url = image.find('a')['data-fancybox-href']
    url_list.append(fimg_url)
    title_fimg = image.find('a')['data-title']
    title_list.append(title_fimg)
    
image_url_list = ['https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' + url for url in url_list]

featured_image_urls = zip(url_list)

try:
    for x in featured_image_urls:
        browser.links.find_by_partial_text('more')
except ElementDoesNotExist:
    print("Scraping Complete")


# In[17]:


image_url_list


# In[18]:


featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA24098_hires.jpg'


# ### Part 3: Mars Facts

# In[19]:


# Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.


# In[20]:


import pandas as pd


# In[21]:


mars_url = "https://space-facts.com/mars/"


# In[22]:


facts_about_mars = pd.read_html(mars_url)
facts_about_mars


# In[23]:


type(facts_about_mars)


# In[24]:


mars_facts_df = facts_about_mars[0][1]
mars_df = pd.DataFrame(mars_facts_df)

mars_df.index = ["Equatorial Diameter", "Polar Diameter", "Mass", "Moons", "Orbt Distance", "Orbit Period",
                "Surface Temperature", "First Record", "Recorded By"]
mars_df.columns = ["About Mars"]
mars_df


# In[25]:


# Confirm the equatorial diameter of Mars
mars_df.loc['Equatorial Diameter']


# In[26]:


# Confirm the polar diameter of Mars
mars_df.loc['Polar Diameter']


# In[27]:


# Confirm the mass of Mars
mars_df.loc['Mass']


# In[28]:


# Use Pandas to convert the data to a HTML table string.


# In[29]:


mars_html = mars_df.to_html()
mars_html


# In[30]:


# Clean up unwanted characters


# In[31]:


cleaned_mars_html = mars_html.replace('\n', '')
cleaned_mars_html


# In[32]:


mars_df.to_html('Mars_Facts.html')


# In[33]:


# This is for OSX users command
# OR, open the created html file manually 
# !open Mars_Facts.html


# ### Mars Hemispheres

# In[34]:


# Visit the USGS Astrogeology site  https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
# And, obtain high resolution images for each of Mar's hemispheres

# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

# Save both the image url string for the full resolution hemisphere image, 
# and the Hemisphere title containing the hemisphere name. 
# Use a Python dictionary to store the data using the keys img_url and title.


# ### First Mars Image: Cerberus

# In[95]:


# collect the first high res image of Mars
first_img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
first_response = requests.get(first_img_url)

soup = BeautifulSoup(first_response.text, 'html.parser')

print(soup.prettify())


# In[97]:


first_results = soup.find_all('li')
first_results


# In[98]:


for first_result in first_results:
    # Error handling
    try:
        # Identify and return link to listing
        first_img_link = first_result.a['href']

        # Print results only if title, price, and link are available
        if (first_img_link):
            print('-------------')
            print(first_img_link)
    except AttributeError as e:
        print(e)


# In[99]:


first_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'


# ### Second Mars Image: Schiaparelli

# In[91]:


# collect the second high res image of Mars
second_img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
second_response = requests.get(second_img_url)

soup = BeautifulSoup(second_response.text, 'html.parser')

print(soup.prettify())


# In[92]:


second_results = soup.find_all('li')
second_results


# In[93]:


for second_result in second_results:
    # Error handling
    try:
        # Identify and return link to listing
        second_img_link = second_result.a['href']

        # Print results only if title, price, and link are available
        if (second_img_link):
            print('-------------')
            print(second_img_link)
    except AttributeError as e:
        print(e)


# In[94]:


# save variable for the second image of Mars
second_img_Mars ='https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'


# ### Third Mars Image: Syrtis

# In[100]:


# collect the third high res image of Mars
third_img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
third_response = requests.get(third_img_url)

soup = BeautifulSoup(third_response.text, 'html.parser')

print(soup.prettify())


# In[101]:


third_results = soup.find_all('li')
third_results


# In[102]:


for third_result in third_results:
    # Error handling
    try:
        # Identify and return link to listing
        third_img_link = third_result.a['href']

        # Print results only if title, price, and link are available
        if (third_img_link):
            print('-------------')
            print(third_img_link)
    except AttributeError as e:
        print(e)


# In[103]:


# save variable for the second image of Mars
third_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'


# ### Fourth Mars Image: Valles

# In[104]:


# collect the fourth high res image of Mars
fourth_img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
fourth_response = requests.get(fourth_img_url)

soup = BeautifulSoup(fourth_response.text, 'html.parser')

print(soup.prettify())


# In[105]:


fourth_results = soup.find_all('li')
fourth_results


# In[106]:


for fourth_result in fourth_results:
    # Error handling
    try:
        # Identify and return link to listing
        fourth_img_link = fourth_result.a['href']

        # Print results only if title, price, and link are available
        if (fourth_img_link):
            print('-------------')
            print(fourth_img_link)
    except AttributeError as e:
        print(e)


# In[107]:


# save variable for the second image of Mars
fourth_img_Mars = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'


# In[109]:


# Append the dictionary with the image url string and the hemisphere title to a list. 
# This list will contain one dictionary for each hemisphere.
hemisphere_image_urls = [
    {"title": "Cerberus Hemisphere", "img_url": {first_img_Mars}},
    {"title": "Schiaparelli Hemisphere", "img_url": {second_img_Mars}},
    {"title": "Syrtis Major Hemisphere", "img_url": {third_img_Mars}},
    {"title": "Valles Marineris Hemisphere", "img_url": {fourth_img_Mars}}
]


# In[110]:


hemisphere_image_urls


# In[ ]:





# In[ ]:




