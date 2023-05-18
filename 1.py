from webScraping import *
# button class _o4kklvw rc-TopReviewsList__button
# review class rc-ReviewsList m-b-3
# result = WebScraping("https://in.coursera.org/learn/html?specialization=web-design","Coursera")
# result = WebScraping("https://in.coursera.org/learn/python-project-for-ai-application-development","Coursera")
result = WebScraping("https://in.coursera.org/learn/android-app","Coursera")
# result = WebScraping("https://www.udemy.com/course/memory-leak-detector/","Udemy")
# result = WebScraping("https://www.udemy.com/course/the-complete-web-development-bootcamp/", "Udemy")
# result = WebScraping("https://in.coursera.org/specializations/fundamentos-de-ciencia-de-datos-con-python-y-sql","Coursera")


#iterating over the dictionary
for key,value in result.items():
    if key == "comments":
        for i in value:
           
           print("\n")
           print(i)
           print("\n")
    else:
        print("\n")
        print(key,":",value)
        print("\n")
         
# 


