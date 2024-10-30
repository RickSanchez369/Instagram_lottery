from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re





def login_to_instagram():
    
    driver = webdriver.Chrome(executable_path='C:/Users/Almas/Desktop/chromedriver-win64/chromedriver.exe')
    driver.get("https://www.instagram.com/accounts/login/")
    
    username = "sina_afkhamiii"
    password = "Sina79afkhami@"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
    
    time.sleep(3)  
    return driver

def collect_comments(driver, post_url):
    driver.get(post_url)
    time.sleep(2)
    
    comments = []
    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load more comments')]"))
            )
            load_more_button.click()
            time.sleep(1)
        except:
            break
    
    comment_elements = driver.find_elements(By.XPATH, "//span[@class='comment_text_class']")
    for comment in comment_elements:
        comments.append(comment.text)
    
    
    mention_counts = {}
    for comment in comments:
        mentions = re.findall(r"@\w+", comment)
        for mention in mentions:
            mention_counts[mention] = mention_counts.get(mention, 0) + 1

    return comments, mention_counts

def collect_likes(driver, post_url):
    driver.get(post_url)
    time.sleep(2)

    users_liked = []
    
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    
    like_elements = driver.find_elements(By.XPATH, "//a[@class='user_link_class']")
    for user in like_elements:
        users_liked.append(user.text)
        
    return users_liked

def collect_followers(driver, profile_url):
    driver.get(profile_url)
    time.sleep(2)
    
    followers = []
    
    
    followers_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "followers"))
    )
    followers_link.click()
    time.sleep(2)
    
    
    followers_popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='isgrP']"))
    )
    
    last_height = driver.execute_script("return arguments[0].scrollHeight", followers_popup)
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup)
        time.sleep(2)
        
        new_height = driver.execute_script("return arguments[0].scrollHeight", followers_popup)
        if new_height == last_height:
            break
        last_height = new_height

    
    follower_elements = driver.find_elements(By.XPATH, "//a[@class='user_link_class']")
    for follower in follower_elements:
        followers.append(follower.text)
        
    return followers
