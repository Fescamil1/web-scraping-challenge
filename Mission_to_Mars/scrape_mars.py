#import dependencies
import pandas as pd
import requests as req
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
     # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    return browser


def scrape_info():
    browser = init_browser()

    #==========NASA Mars News===================#
    #Collect the latest News Title and Paragraph Text. Assign the text to variables to reference later.
    
    # visit the Mars News url
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    time.sleep(2)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    
    # Scrape the latest News Title and Paragraph Text
    news_title = soup.find("div", class_ = "content_title").text
    news_p = soup.find("div", class_ = "article_teaser_body").text

    #==========JPL Mars Space Images - Featured Image ===========#
    #Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    #assign the url string to a variable called `featured_image_url`
    
    #Visit the url for JPL Mars Space Images featured Image
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    image_soup = bs(html, 'html.parser')

    #Get the url for the featured image and display it. 
    whole_image_url =image_soup.find('img',class_='headerimage fade-in')['src']
    #print(whole_image_url)

    featured_image_url = image_url+whole_image_url
    
