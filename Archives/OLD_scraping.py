#!/usr/bin/env python
# coding: utf-8


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Create function that will initialize browser, create data dictionary, end WebDriver and return scraped data
def scrape_all():
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #set news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    #Run all scraping functions & store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres_list": scrape_hemispheres(browser),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemisphere_image_urls(browser)
    }
    #Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html=browser.html
    news_soup = soup(html, 'html.parser')

# Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()


    except AttributeError:
        return None, None
    
    return news_title, news_p



def featured_image(browser):
   #Scrape space images site
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None 

    # add the base URL to our code. / Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url



def mars_facts():
    try:
        #use 'read_html' to scrape the facts table into a df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    #Assign columns and index
    # df.columns=['Description', "Mars', 'Earth"]
    # df.set_index('Description', inplace=True)

    #Convert df into html format, add bootstrap
    return df.to_html(classes="table table-striped")

def 
def scrape_hemispheres(browser):
    html = browser.html
    hemispheres_html = soup(html, 'html.parser')
    hemispheres_list = []
    hemispheres_atags= hemispheres_html.find_all("a", class_= "itemLink")
    for i in range(0, len(hemispheres_atags)):
        if i % 2 != 0:
            browser.visit(f'https://astrogeology.usgs.gov{hemispheres_atags[i]["href"]}')
            html = browser.html
            hemisphere_html = soup(html, 'html.parser')
            hemisphere_dict = {
                "title": hemispheres_atags[i].find("h3").text,
                "img_url": "https://upload.wikimedia.org/wikipedia/commons/0/02/OSIRIS_Mars_true_color.jpg"
            }
            hemispheres_list.append(hemisphere_dict)
    return hemispheres_list

if __name__ == "__main__":
    print(scrape_all())

