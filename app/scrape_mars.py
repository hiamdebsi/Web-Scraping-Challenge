#Import Dependencies 
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    #Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Create dictionary for scraped information
    mars_data = {}

    ###########################################################
   
    #NASA MARS NEWS SCRAPING
    news_url = 'https://redplanetscience.com/'
    #Visit the url
    browser.visit(news_url)
    #Scrape page into Soup
    news_html = browser.html
    news_soup = bs(news_html,'html.parser')
    #Get title and paragraph
    news_title = news_soup.find('div', class_='content_title').text.strip()
    news_p = news_soup.find('div', class_='article_teaser_body').text.strip()
   
    ###########################################################

    #JPL Mars Space Images - Featured Image
    image_url='https://spaceimages-mars.com'
    #Visit the url
    browser.visit(image_url)
    #Scrape page into Soup
    image_html = browser.html
    image_soup = bs(image_html,'html.parser')
    #Find feature image 
    image_path = image_soup.find_all('img', class_='headerimage fade-in')[0]['src']
    featured_image_url = image_url + '/' + image_path

    ###########################################################
    
    #MARS FACTS
    facts_url = 'https://galaxyfacts-mars.com'
    #Read the url in html format
    tables = pd.read_html(facts_url)
    #Find the specific table and convert into html
    second_table = tables[0] 
    facts_table = second_table.rename(columns={0:'Description',1:'Mars',2:'Earth'}).set_index('Description').copy()
    facts_table_html = facts_table.to_html()

    ###########################################################

    #MARS HEMISPHERES
    hem_url = 'https://marshemispheres.com/'
    #Visit the url
    browser.visit(hem_url)
    hem_html = browser.html
    #Scrape page into Soup
    hem_soup = bs(hem_html, 'html.parser')
    items = hem_soup.find_all('div', class_='item')
    #Create a list which we will append later
    hemisphere_image_urls = []

    #Loop through the items
    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hem_url + partial_img_url)
        partial_img_html = browser.html
        partial_soup = bs( partial_img_html, 'html.parser')
        img_url = hem_url + partial_soup.find('img', class_='wide-image')['src']
        #Append the information into created list
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    ###########################################################
    
    #Add scraped information into dictionary created
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "facts_table": facts_table_html,
        "hemisphere_images": hemisphere_image_urls
    }

    browser.quit()
    print("Scraping complete", len(mars_data))

    return mars_data


