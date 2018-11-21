# coding: utf-8

# In[102]:
def scrape():

    # Import Dependencies #
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser
    import pandas as pd


    # # NASA Mars News

    # In[3]:


    # URL to be scraped #
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


    # In[4]:


    # Retrieve page with the requests module
    response = requests.get(news_url)


    # In[32]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, "lxml")#'html.parser'#


    # In[33]:


    # In[57]:


    # Grab all news objects
    news = soup.find_all("div", class_="slide")

    # Get latest news article's title without new line characters
    news_title = news[0].find("div", class_="content_title").find("a").text
    news_title = news_title[1:-1]

    # Get latest news article's description without new line characters
    news_p = news[0].find("div", class_="rollover_description_inner")
    news_p = news_p.text[1:-1]


    # # JPL Mars Space Images - Featured Image

    # In[65]:


    # Use splinter to find featured image url
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # Click the 'FULL IMAGE' button on page
    browser.click_link_by_partial_text('FULL IMAGE')


    # In[67]:


    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')


    # In[89]:


    featured_image_url = soup.find_all("article", class_="carousel_item")
    featured_image_url = featured_image_url[0].find('a')['data-fancybox-href']


    # In[90]:


    featured_image_url = "https://www.jpl.nasa.gov/" + featured_image_url




    # # Mars Weather

    # In[94]:


    tweet_url = "https://twitter.com/marswxreport?lang=en"

    # Retrieve page with the requests module
    response = requests.get(tweet_url)

    soup = bs(response.text, 'html.parser')



    # In[100]:


    mars_weather = soup.find_all("div", class_="content")
    mars_weather = mars_weather[0].p.text



    # # Mars Facts

    # In[108]:


    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    df = tables[0]
    html_string = df.to_html()


    # # Mars Hemispheres

    # In[112]:


    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(hemi_url)

    soup = bs(response.text, 'html.parser')
    hemisphere_titles = soup.find_all("div", "item")


    # In[121]:


    hemisphere_image_urls = []
    hemi_dict = {}

    for i in range (0,4):
        hemisphere_title = hemisphere_titles[i].find("h3").text
        browser.visit(hemi_url)
        browser.click_link_by_partial_text(hemisphere_title)
        html = browser.html
        image_soup = bs(html, "html.parser")
        img_url = image_soup.find('div', class_="downloads").find('a')['href']
        hemi_dict = {"title":hemisphere_title,"img_url":img_url}
        hemisphere_image_urls.append(hemi_dict)



    final_dict = {"news_title" : news_title,
                  "news_p" : news_p,
                  "featured_image_url" : featured_image_url,
                  "mars_weather" : mars_weather,
                  "html_string" : html_string,
                  "hemisphere_image_urls" : hemisphere_image_urls
    }

    return final_dict
