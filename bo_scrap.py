from bs4 import BeautifulSoup
import requests
import json
from requests import Session


def get_house():
    """

  """
root_url = "https://www.immoweb.be/en/classified/penthouse/for-sale/gent/9000/10611711"

def get_house_info(url):
    s = requests.Session()
    house_info = s.get(url)
    soup = BeautifulSoup(house_info.text, "html.parser")
    house_info={}
    for elem in soup.find_all('div', attrs={'class':"classified__information--address"}):
      print(elem)
        
get_house_info(root_url)