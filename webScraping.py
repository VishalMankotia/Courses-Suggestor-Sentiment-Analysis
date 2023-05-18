from bs4 import BeautifulSoup
import urllib.request, json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from comments import *
path="chromedriver.exe"
# create a new Chrome browser instance
# driver = webdriver.Chrome(path)

 


def WebScraping(link, platform):
    print("link: ", link)
    site = platform
    c_url = link
    comments = []
    
    c = []
    result = {}
    if site == "Coursera":
        result['platform'] = 'Coursera'
         
        if '?' in c_url:
            c_url = c_url[:c_url.index("?")]
        url = c_url
       
        response = requests.get(url)
        htmlcontent = response.content
        soup = BeautifulSoup(htmlcontent, "html.parser")
        
        c = soup.findAll('h1', {'class': 'banner-title banner-title-without--subtitle m-b-0'})
       
        for i in c:
           
            ti=result["title"] = i.text
        
            
        c = soup.findAll('div', {'class': 'm-t-1 description'})
        for i in c:

            dec=result["description"] = i.text
            # print("Vishal = ", dec) # isse description milta   haii


        c = soup.findAll('div', {'class': '_16ni8zai m-b-0 m-t-1s'})
        for i in c:
            ti=result["duration"] = i.text
            # print("Vishal = ", ti) # time milta haii
        c = soup.findAll('h3', {'class': 'instructor-name headline-3-text bold'})
        for i in c:

            ins=result["instructor"] = i.text
            # print("Vishal = ", ins) # instructor milta haii
        c = soup.findAll('div', {'class': '_1fpiay2'})
        for i in c:
            result["learner_count"] = i.text

        buttons = soup.find_all("a", class_="_o4kklvw rc-TopReviewsList__button")
        # print(href)
        for button in buttons:
            href1 = button["href"]
            # print(href1)
             
             
     
        c_url = "https://in.coursera.org"+href1
        # print(c_url)
        
        k=0
        while(1):
            k=k+1
            url =c_url + "?page=" + str(k)
            try:
                response = requests.get(url)
                if(response.status_code==404):
                    break
                

                htmlcontent = response.content
              
              
                soup = BeautifulSoup(htmlcontent, "html.parser")
                container = soup.findAll('div', {'class': 'rc-ReviewsList m-b-3'})
                # print("Vishal = ", container)
                if(len(container)==0):
                    break
                for j in container:
                    comments.append(j.text)

                print("page number "+ str(k) + " done")
                # if(k==5):
                #     break
                
            except:
                
                break
            
             
              
            

           
        result["comments"] = comments
        # print("Vishal = ", com) # comments milta haii
        return result

    elif site =="Youtube":
        result['v'] = link[link.index('=')+1:]
        videoId = c_url[(c_url.index("=") + 1):]
        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}'.format(
            videoId, 'AIzaSyDEgmEzXQ7GCRXqAa8ctgc6jA50vZJLhR4')
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        duration = data["items"][0]["contentDetails"]["duration"]
        result["duration"] = ''
        if duration.find('H')!=-1:
            result["duration"] = result["duration"] + (duration[duration.find('T') + 1:duration.find('H')] + ' Hr ')
        if duration.find('M')!=-1 and duration.find('H')!=-1:
            result["duration"] = result["duration"] + ' ' + (duration[duration.find('H') + 1:duration.find('M')] + ' Mins')
        elif duration.find('M')!=-1:
            result["duration"] = result["duration"] + ' ' +(duration[duration.find('T') + 1:duration.find('M')] + ' Mins')

        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(
            videoId, 'AIzaSyDEgmEzXQ7GCRXqAa8ctgc6jA50vZJLhR4')
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        result["learner_count"] = data["items"][0]["statistics"]["viewCount"] + ' views'

        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}'.format(
            videoId, 'AIzaSyDEgmEzXQ7GCRXqAa8ctgc6jA50vZJLhR4')
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        result["platform"] = "YouTube"
        result["title"] = data["items"][0]["snippet"]["title"]
        result["instructor"] = data["items"][0]["snippet"]["channelTitle"]
        result["description"] = data["items"][0]["snippet"]["description"]

        url = 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&videoId={}&key={}'.format(
            videoId, 'AIzaSyDEgmEzXQ7GCRXqAa8ctgc6jA50vZJLhR4')
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        for i in range(len(data["items"])):
            if data['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'] is not None:
                comments.append(data['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'])
        com=result["comments"] = comments
        # print("Vishal Mankotia ",com)
        return result
    
    elif site == "Udemy":
       
        response = requests.get(c_url)
        htmlcontent = response.content
        soup = BeautifulSoup(htmlcontent, "html.parser")
        
        result["platform"] = "Udemy"
        c = soup.findAll('h1', {'class': 'ud-heading-xl clp-lead__title clp-lead__title--small'})
 
        for i in c:
            print(i.text)
            result["title"] = i.text
       
        c = soup.findAll('span', {'class': 'instructor-links--names--3U_NU'})

        for i in c:

            ins=result["instructor"] = i.text

        c = soup.findAll('div', {'class': 'ud-text-md clp-lead__headline'})
        for i in c:

            dec=result["description"] = i.text

        result["duration"] = "17 hours 34 min"

        c = soup.findAll('div', {'class': 'enrollment'})
        for i in c:
            result["learner_count"] = i.text
        # create a new Chrome browser instance


        
        # driver = webdriver.Chrome(path)

        # driver.get(c_url)
        # print(c_url)
        # a=input("Enter the number of pages you want to scrape: ")

        # retry_count = 0

        # time_duration = driver.find_element(By.CLASS_NAME,"component-margin incentives--container--1TRoZ incentives--hide-on-tablet--ZuHn5")
        # print(time_duration.text)
        # a=input("Enter the number of pages you want to scrape: ")

        # while True:
        #     try:
        #         show_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ud-btn.ud-btn-medium.ud-btn-ghost.ud-heading-sm.show-more-button--button--s7DhA.ud-link-underline")))
        #         show_more_button.click()
        #         break
        #     except:
        #           print("Element not found, retrying...")
        #FETCH information under div tag with class="reviews-modal--reviews-list-section--Bk11v"

        # reviews = driver.find_element(By.CLASS_NAME,"reviews-modal--reviews-list-section--Bk11v")
        # # print(type(reviews))
    
        # div_main = driver.find_element(By.CLASS_NAME,"reviews-modal--reviews-list-section--Bk11v")

        # ul = div_main.find_element(By.TAG_NAME,"ul")

        # li = ul.find_elements(By.TAG_NAME,"li")
        li = comm
        split_lists = [item.strip() for sublist in li for item in sublist.split("Filled StarStarStarStarStar")]
        
         
        # convert li list into individuals lists

        
        # print(type(li))
        # input("Enter the number of pages you want to scrape: ")

        # list = []

        # i=li[0]
        # print(i.text)
        # a=input("Enter the number of pages you want to scrape: ")
        # div1= i.find_element(By.CLASS_NAME,"reviews-modal--reviews-list-item--31udc ud-block-list-item ud-block-list-item-large ud-block-list-item-neutral ud-text-md")
        # div2= div1.find_element(By.CLASS_NAME,"ud-block-list-item-content")
        # div3= div2.find_element(By.CLASS_NAME,"review--review-container--snUvY reviews-modal--review--1s2ta review--review-desktop-container--r0Nor review--review-desktop-inline--OL1n-")
        # div4= div3.find_element(By.CLASS_NAME,"show-more-module--container--2QPRN")
        # div5= div4.find_element(By.CLASS_NAME,"ud-text-md show-more-module--content--cjTh0")
        # final_div = div5.find_element(By.TAG_NAME,"div")
        # text_ = final_div.find_element(By.TAG_NAME,"p")

        # list.append(text_.text)
        # print(text_.text)
        # a=input("Enter the number of pages you want to scrape: ")

        # list = [i.text for i in li]


        # lis=split_lists+split_lists+split_lists
       

        result["comments"] = split_lists


        
                
            

        
         
        return result

        
       
       


         

 

