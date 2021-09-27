#!/usr/bin/env python
# coding: utf-8



# DEPENDENCIES: Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter (creating instance of a Splinter browser)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)





# ### VISIT THE NASA MARS NEWS SITE 
# Visit the mars nasa news site (tell Splinter which site I want to visit by assigning link to a URL)
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and use BeautifulSoup to parse the HTML
html = browser.html
news_soup = soup(html, 'html.parser')

#assign slide_elem as the variable to pinpoint the div tag with the class of list_text
slide_elem = news_soup.select_one('div.list_text')


#look inside the slide_elem variable to find this specific data: a div with a class of content_title
slide_elem.find('div', class_='content_title')


# Use the parent element variable (slide_elem) & return only the title of the news article by chaining .get_text onto .find(), so only the text of the element is returned.
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p





# ### JPL SPACE IMAGES FEATURED IMAGE
# Visit URL to begin scraping
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Start getting code ready to automate all of the clicks it will take to get the full-size version of the Featured Image 
#Button 1: Use indexing to stipulate that I want the browser to click the 2nd button ~ Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the new page that was loaded onto the automated browser, so you can continue scraping full-size image URL
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# find the relative image url by using .get('src') to pull the link to the image. (telling BeautifulSoup this is where the image I want lives, so use the link that's inside these tags)
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Add the baes URL to the relative URL to get the complete link (Use the base url to create an absolute url)
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url





# ### MARS FACTS: Scrape a table from another website to add to the app
#Scrape entire table with Pandas' .read_html()
#Step 1: search for & return a list of tables. The index of 0 tells Pandas to ull only the 1st table it encounters. Then, turn it into a DataFrame
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


#Step 2: Assign new columns to the df
df.columns=['Description', 'Mars', 'Earth']

#Step 3: turn the description column into the df's index. inPlace=True so that the updated index will remain in place.
df.set_index('Description', inplace=True)
df


# Add the table to the web app by Converting dataframe back into html-ready code
df.to_html()

#I have the image, the article, and the table. Now, automate the scraping by converting this code into a .py file 





# # D1: SCRAPE HIGH-RES MARS' HEMISPHERE IMAGES & TITLES 

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# # 2. Create a list to hold the images and titles.
# hemisphere_image_urls = []

# #3. Write code to retrieve the titles for each hemisphere (and then image urls)
# html = browser.html
# html_soup = soup(html, 'html.parser')
# html_soup

# a_tags = html_soup.find_all('a', class_ = 'itemLink')

# for i in a_tags:
#     hemisphere = {}
#     # Get Hemisphere title
#     hemisphere['title'] = browser.find_by_tag('h3')
    
#     #Get image urls
#     #links = browser.links.find_by_text('itemLink product-item')[i].click()
# #    links = browser.links.find_by_partial_text('.html')
#     #links = browser.find_by_css('a.product-item img')



# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# First, get a list of all of the hemispheres
links = browser.find_by_css('a.product-item img')

# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css('a.product-item img')[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()



# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()





