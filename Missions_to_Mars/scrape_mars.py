# Dependencies and Setup
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars = {}
    hemisphere_image_urls = []

#NASA headline and paragraph
    nasa = 'https://mars.nasa.gov/news/'
    browser.visit(nasa)
    html = browser.html

    news_soup = BeautifulSoup(html, 'html.parser')
    slide_element = news_soup.select_one("ul.item_list li.slide")
    news_title = slide_element.find("div", class_="content_title").get_text()
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    
    mars['news_title'] = news_title
    mars['news_paragraph'] = news_paragraph
    browser.quit()

 #Jet Propulsion Lab Mars image   
    jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl)
    html=browser.html

    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()
    
    img_soup = BeautifulSoup(html, 'html.parser')
    img_url = img_soup.select_one("figure.lede a img").get("src")
    
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    
    mars['Featured_Image'] = img_url

    browser.quit()

#Mars facts
    facts = 'https://space-facts.com/mars/'
    browser.visit(facts)
    html=browser.html
    facts_soup = BeautifulSoup(html, 'html.parser')
    mars_df = ((pd.read_html(facts_soup))[0]).rename(columns={0: "Attribute", 1: "Value"}).set_index(['Attribute'])
    html_table = (mars_df.to_html()).replace('\n', '')
    mars['Mars_Facts'] = html_table

#Hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    hemispheres_soup = BeautifulSoup(html, "html.parser")
    items = hemispheres_soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    for item in items:
        title = item.find('h3').text
        image_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_url + image_url)
        image_html = browser.html
        soup = BeautifulSoup( image_html, 'html.parser')
        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})

    mars["hemisphere_urls"] = hemisphere_image_urls
    
    browser.quit()
    return mars