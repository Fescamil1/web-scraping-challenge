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
    
    #===================Mars Facts ========================#
    #visit the Mars Facts webpage (https://galaxyfacts-mars.com)
    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass,

    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    
    #scrape the table containing facts about Mars
    table = pd.read_html(facts_url)
    mars_facts = table[1]

    # Rename the columns and set Description as the index
    mars_facts.columns = ['Description','Value']
    mars_facts.set_index('Description', inplace=True)

    # Convert the data to a HTML table
    html_table = mars_facts.to_html()

    #remove unwanted newlines to clean up the table
    html_table.replace("\n", '')

    #Save the html table
    mars_facts.to_html('Mars_Facts_table.html')

    #===================Mars Hemispheres========================#
    #Visit the astrogeology site (https://marshemispheres.com/)
    #obtain high resolution images for each of Mar's hemispheres.

    #Visit the astrogeology site
    hem_url = "https://marshemispheres.com/"
    browser.visit(hem_url)
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    hem_soup = bs(html, 'html.parser')

    # get items that has the hemispheres information
    results = hem_soup.find_all('div', class_='item')

    #create empty list for the hemisphere 
    hemisphere_image_urls = []

    #loop through each of the hemispheres
    for result in results:
        h_title= result.find('h3').text
        h_image= result.find('a',class_='itemLink product-item')['href']
        
        # Visit each of the links to the hemispheres in order to find the image url to the full resolution image.
        browser.visit(hem_url + h_image)
        
        # Scrape page into Soup
        html = browser.html
        soup = bs(html, 'html.parser')
        
        partial_url= soup.find('img', class_='wide-image')['src']
        full_url= hem_url + partial_url
        
        #add to dictionary
        hemisphere_image_urls.append({"title" : h_title, "img_url" : full_url})

    # Close the browser after scraping
    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data


