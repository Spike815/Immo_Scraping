from bs4 import BeautifulSoup
import requests
import json
from requests import Session
import re
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def get_house_info(url,session):
   """
   this function takes a url from a propertie on immoweb and pirates the data into a dictionary
   """
   house_info = session.get(url)
   soup = BeautifulSoup(house_info.text, "html.parser")


   house_info={}
   # captures {<any text>} within window.classified
   regex = r"window.classified = (\{.*\})"

   # returns a list containing {<any text}
   script_text=soup.find('div',attrs={"id":"main-container"}).script.text
   # applies regex to scrip_text
   script_after_regex = re.findall(regex, script_text)

   # returns first element of script_after_regex (full clustered dictionary of property attributes)
   script_text_dict = json.loads(script_after_regex[0])
   properties = script_text_dict['property']

   # adds 'key : value' pairs to house_info dictionary. If value does not exist, it is replaced by a 0.
   try:
      house_info['id'] = script_text_dict['id']
   except:
      house_info['id'] = 0

   try:
      house_info['type of property'] = properties['type']
   except:
      house_info['type of property'] = 0

   try:
      house_info['subtype of property'] = properties['subtype']
   except:
      house_info['subtype of property'] = 0

   try:
      house_info['locality'] = properties['location']['locality']
   except:
      house_info['locality'] = 0
   try:
      house_info["province"] = properties['location']['province']
   except:
      house_info['province'] = 0
   try:
      house_info['postalCode']= properties['location']['postalCode']
   except:
      house_info['postalCode']
      
   try:
      house_info['price'] = script_text_dict['price']['mainValue']
   except:
      house_info['price'] = 0

   try:
      house_info['type of sale'] = script_text_dict['price']['type']
   except:
      house_info['type of sale'] = 0

   try:  
      house_info['number of bedrooms'] = properties['bedroomCount']
   except:
      house_info['number of bedrooms'] = 0

   try:  
      house_info['living area'] = properties['livingRoom']['surface']
   except:
      house_info['living area'] = 0

   try:
      house_info['fully equipped kitchen'] = script_text_dict['property']['kitchen']['type'].lower()
   except:
      house_info['fully equipped kitchen'] = 0

   try:
      house_info['furnished'] = script_text_dict['transaction']['sale']['isFurnished']
   except:
      house_info['furnished'] = 0

   try:
      house_info['open fire'] = properties['fireplaceExists']
   except:
      house_info['open fire'] = 0

   try:
      house_info['terrace'] = properties['hasTerrace']
   except:
      house_info['terrace'] = 0

   try:
      house_info['terrace area'] = properties['terraceSurface']
   except:
      house_info['terrace area'] = 0

   try:
      house_info['garden'] = properties['hasGarden']
   except:
      house_info['garden'] = 0

   try:
      house_info['garden area'] = properties['gardenSurface']
   except:
      house_info['garden area'] = 0

   try:
      house_info['total property area'] = properties['netHabitableSurface']
   except:
      house_info['total property area'] = 0

   try:
      house_info['total land area'] = properties['land']['surface']
   except:
      house_info['total land area'] = 0

   try:
      house_info['number of facades'] = properties['building']['facadeCount']
   except:
      house_info['number of facades'] = 0

   try:
      house_info['swimming pool'] = properties['hasSwimmingPool']
   except:
      house_info['swimming pool'] = 0

   try:
      house_info['state of the building'] = properties['building']['condition'].lower()
   except: 
      house_info['state of the building'] = 0

   # for k in house_info:
   #    if house_info[k] == False:
   #       house_info[k] == 0
   #    elif house_info[k] == None:
   #       house_info[k] = 0
   #    elif house_info[k] == True:
   #       house_info[k] = 1
   #    else:
   #       pass
         
   return house_info


def get_url(session, i=1):
    root_house_list_url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&isNewlyBuilt=false&isALifeAnnuitySale=false&isAPublicSale=false&page={i}&orderBy=relevance"
    root_apartment_list_url = f"https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&isNewlyBuilt=false&isAPublicSale=false&isALifeAnnuitySale=false&isUnderOption=false&isAnInvestmentProperty=false&page={i}&orderBy=relevance"

    house_list = session.get(root_house_list_url)
    apartment_list = session.get(root_apartment_list_url)

    soup_house = BeautifulSoup(house_list.text, "html.parser")
    soup_apartment = BeautifulSoup(apartment_list.text, "html.parser")
    url_list = []

    for block in soup_house.find_all("h2",{'class':"card__title card--result__title"}):
        tag_a = block.find('a')['href']
        url_list.append(tag_a)
    
    for block in soup_apartment.find_all("h2",{'class':"card__title card--result__title"}):
        tag_a = block.find('a')['href']
        url_list.append(tag_a)
    
    return(url_list)



def get_all_urls(page = 200):
   """
    this function takes one parameter 'page'(int), returns a list of urls scraped from\
        immoweb search page. The list contains page*60 urls in total.
   """
   with ThreadPoolExecutor(max_workers=12) as executor:
      with requests.Session() as session:
         futures = [executor.submit(get_url, session, i) for i in range(1,page+1)]
         list_of_url_temp= [item.result() for item in futures]
         final_url_list = [element for innerList in list_of_url_temp for element in innerList]
   return final_url_list




def scraper(final_url_list): 
    """This function takes one parameter final_url_list, returns a list of dictionary scraped from\
        immoweb page."""       
    data_list = []
    added = 0
    futures = []
    #build up pool of tasks to be executed
    with ThreadPoolExecutor(max_workers=15) as executor:
        with requests.Session() as session:
            for url in final_url_list:
                futures.append(executor.submit(get_house_info,url,session))
            #try to excute the get_house_info function, append the result to final list
            #capture the errors and print out the url
            for item in futures:
               try:
                  data_list.append(item.result())
                  percent = 100*added/len(final_url_list)
                  print(f"Data being processed : {round(percent,2)}%", end="\r")
               except:
                  i = futures.index(item)
                  print(f"There is an error while scraping this website:{final_url_list[i]}")
               finally:
                  added += 1
    
    return data_list




def data_to_csv(data_list):
    df = pd.DataFrame(data_list)
    df.to_csv('output.csv', index=False)

