import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


username = os.getenv("INSTAGRAM_USERNAME")  
password = os.getenv("INSTAGRAM_PASSWORD")  

def login(driver):
    
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)  

    
    username_input = driver.find_element(By.NAME, "username")  
    password_input = driver.find_element(By.NAME, "password")  
    
    
    username_input.send_keys(username)  
    password_input.send_keys(password)  
    
    
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")  
    login_button.click()
    
    
def collect_comments(driver, post_url):
    driver.get(post_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'Mr508')]")))

    user_data = {}  
    comment_elements = driver.find_elements(By.XPATH, "//span[@class='comment_text_class']")
    
    for element in comment_elements:
        comment_text = element.text
        username = element.find_element(By.XPATH, ".//preceding-sibling::span[@class='username_class']").text  
        
        
        if username not in user_data:
            user_data[username] = {
                'comment_count': 0,  
                'mention_count': 0  
            }

        
        user_data[username]['comment_count'] += 1
        
        
        mentions = [word[1:] for word in comment_text.split() if word.startswith('@')]  
        

        user_data[username]['mention_count'] += int(len(mentions) // 5) 

    return user_data 


def collect_likes(driver, post_url):
    
    driver.get(post_url)
    
    
    likes_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'likes')]")))
    likes_button.click()  
    
    time.sleep(3) 
    
    likes = []  
    like_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/')]//div[@class='e1e1d']//span")  
    for element in like_elements:
        likes.append(element.text)  
    
    return likes  

def collect_followers(driver, username):
    
    driver.get(f"https://www.instagram.com/{username}/") 
    
    
    followers_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]")))
    followers_button.click()  
    
    time.sleep(3)  
    
    followers = []  
    follower_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/')]//div[@class='e1e1d']//span")  # پیدا کردن کاربران فالوور
    for element in follower_elements:
        followers.append(element.text)  
    
    return followers  



