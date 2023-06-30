## Immo_Scraping
#### *A property scraping project in Python 3.11 by Bo Cao, Sacha Schreuer & George Hollingdale*
***
## Description
This repository contains a program that will scrape the website [ImmoWeb](https://www.immoweb.be/) and pull property data for up to 12,000 listings.
***
## Installation
Firstly ensure that you have Python 3.11 installed on your device.

To create an environment for the scraper you will need to:
* In your terminal, navigate to the repository folder
* Enter the command line:
  > python -m venv *"name_of_environment"*
* Then, from your repository folder in terminal, enter the following command for your OS
  * Windows: 
    > *"name_of_environment"*\Scripts\activate
  * Mac/Linux:
    > source *"name_of_environment"*/bin/activate

You will also need to run the following commands within your environment to install the required modules:
  > pip install bs4
  
  > pip install pandas

You should now be ready to run main.py
***
## Usage
To use the scraper, navigate to your repository folder in terminal and enter
* >main.py
  
This will begin to run the code and should output close to 12,000 lines of property data to a file named output.csv. The code uses ten threads so be sure that your machine has enough processing power.
***
## Contributors
The project was headed by Bo with contributors Sacha and George.
***
## Timeline
The project was completed in around 75 worker hours, spread across four days. 
  * We spent around 6 hours setting up our repositories and environments
  * The initial get of a single url and outputting it's data took around 25 hours
 * The mvp building of the get_url and get_house_info functions took around 15 hours
  * Testing the code on a larger set of data (10 urls, 100 urls and 500 urls) took around 3 hours
 * Making the csv exportable took around 1 hour
  * Fine tuning the above functions took a further 10 hours
  * The remaining hours were spent implementing concurrency, error handling for larger data sets, and other cleaning of code
  * We've also tested the program on three different machines to verify that each csv had close to 12,000 property's data attached.
  ***
  ## About us
  We are three person team of Junior Data Scientists @ BeCode. This was our fourth week of our training, and it is out first attempt at a group project. Some of us have less than a month's experience of coding and we had to learn a lot of new Python techniques to reach our goal.




