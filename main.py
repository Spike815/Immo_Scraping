from functions import get_house_info, get_url, get_all_urls, scraper, data_to_csv

# Call get_all_urls to get the list of URLs
url_list = get_all_urls(page=200)

# Call scraper to scrape the data from the URLs
data_list = scraper(url_list)

# Call data_to_csv to save the data to a CSV file
data_to_csv(data_list)
