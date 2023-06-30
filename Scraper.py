from bs4 import BeautifulSoup
import requests
import json
from requests import Session
import re
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def get_house_info(url):
  s = requests.Session()
  house_info = s.get(url)
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


  """
  if house_info['state of the building'] == "to_be_done_up" or house_info['state of the building'] == "to_renovate" or ['state of the building'] == "to_refurbish":
    house_info['state of the building'] = 0
  else:
    house_info['state of the building'] = 1
    """
  if house_info['fully equipped kitchen'] == "undefined" or house_info['fully equipped kitchen'] == "uninstalled" or house_info['fully equipped kitchen'] == "semi_equipped" or house_info['fully equipped kitchen'] == "usa_uninstalled" or house_info['fully equipped kitchen'] == "usa_semi_equipped":
    house_info['fully equipped kitchen'] = 0
  else:
    house_info['fully equipped kitchen'] = 1
  for key in house_info.keys():
    if house_info[key] == None:
      house_info[key] = 0
    elif house_info[key] == False:
      house_info[key] = 0
    elif house_info[key] == True:
      house_info[key] = 1
    else:
      pass
  return house_info


def get_url(i=1):
    root_house_list_url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&isNewlyBuilt=false&isALifeAnnuitySale=false&isAPublicSale=false&page={i}&orderBy=relevance"
    root_apartment_list_url = f"https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&isNewlyBuilt=false&isAPublicSale=false&isALifeAnnuitySale=false&isUnderOption=false&isAnInvestmentProperty=false&page={i}&orderBy=relevance"
    s = requests.Session()

    house_list = s.get(root_house_list_url)
    apartment_list = s.get(root_apartment_list_url)

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

with ThreadPoolExecutor(max_workers=12) as executor:
    futures = [executor.submit(get_url, i) for i in range(1,5)]
    list_of_url_temp= [item.result() for item in futures]
    final_url_list = [element for innerList in list_of_url_temp for element in innerList]

with ThreadPoolExecutor(max_workers=12) as executor:
    futures = [executor.submit(get_house_info, url) for url in final_url_list]
    data_dict= [item.result() for item in futures]

df = pd.DataFrame(data_dict)
df.to_csv('output.csv', index=False)