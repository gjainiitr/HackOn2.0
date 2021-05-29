import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions

def get_tweet_data(card):
    # Extract data from tweet data
    username = card.find_element_by_xpath('.//span').text
    handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    try:
        postDate = card.find_element_by_xpath(".//time").get_attribute('datetime')
    except NoSuchElementException:
        return
    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    tweet = (username, handle, postDate, text)
    return tweet

options = EdgeOptions()
options.use_chromium = True
driver = Edge(options=options)

driver.get("https://www.twitter.com/login")

#################################################################
# Add logic to wait for the page to load before executing further
#################################################################
sleep(3)


username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys('GopalJa01147205')

# my_password = getpass()

password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys('Abcde@123')

password.send_keys(Keys.RETURN)

#################################################################
# Add logic to wait for the page to load before executing further
#################################################################
sleep(3)

# Finding the search bar
search_bar = driver.find_element_by_xpath('//a[@aria-label="Search and explore"]')
search_bar.click()

sleep(1)

# Inputting the text to search bar
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search_input.send_keys('#covidhelp')

search_input.send_keys(Keys.RETURN)
driver.find_element_by_link_text('Latest').click()

data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True


while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
    
    scroll_attempt = 0
    while True:
        # check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1;
            
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2)
        else:
            last_position = curr_position
            break