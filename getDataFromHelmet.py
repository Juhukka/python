#read website data from helmet
# read website data using chrome driverselenium
from selenium import webdriver
import requests


# intialize the URL

url = "https://helmet.finna.fi/Search/Results?filter%5B%5D=%7Eformat%3A%220%2FGame%2F%22&filter%5B%5D=%7Emain_date_str%3A%222024%22&lookfor=playstation+5&type=AllFields&sort=first_indexed+desc&filter%5B%5D=%7Eformat%3A%220%2FGame%2F%22&filter%5B%5D=%7Emain_date_str%3A%222024%22"
url = "https://helmet.finna.fi/Search/Results?limit=50&filter%5B%5D=~format%3A%220%2FGame%2F%22&lookfor=playstation+5&type=AllFields&sort=first_indexed+desc&filter%"

# clear data from files
findword = "dune"
open("helmet_data.txt", "w", encoding="utf-8").close()
open(f"{findword}.txt", "w", encoding="utf-8").close()

# make a request to the URL
response = requests.get(url)   

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Data retrieved successfully:")
    print(data)
else:
    print("Failed to retrieve data")

# open the website using selenium
driver = webdriver.Chrome()
driver.get(url)
# Wait for the page to load


# read 3 pages of data
master_list = []

for _ in range(5):
    # Wait for the page to load after navigation
    driver.implicitly_wait(5)
    # Scroll to bottom to ensure all content loads
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(4)
    xpath = "//h2[@class='search-title']"
    # Re-locate elements on the current page
    elements = driver.find_elements("xpath", xpath)
    if not elements:
        print("No elements found with the given XPath.")
        break
    for element in elements:
        try:
            if element.text:
                master_list.append(element.text)
        except Exception as e:
            print(f"Error occurred while processing element: {e}")
    # Try to click the next page button
    next_button_xpath = "//a[@class='page-link'][contains(@aria-label, 'Siirry se')]"
    try:
        next_button = driver.find_element("xpath", next_button_xpath)
        next_button.click()
    except Exception as e:
        print(f"Error occurred while clicking next button: {e}")
        break  # Stop if next button is not found

# clean data, delete Näytä tarkat tiedot
master_list = [item.replace("Näytä tarkat tiedot", "").strip() for item in master_list]

# check if master_list include data about ...


if master_list:
    
    for item in master_list:
        # Check if the item contains the word we're looking for
        item_lower = item.lower()
        findword_lower = findword.lower()
        if findword_lower in item_lower:
            print(f"Master list contains data about {findword}:")
            print(f" - {item}")
            # write the data to a file
            with open(f"{findword}.txt", "a", encoding="utf-8") as file:
                file.write(f"{item}\n")

for item in master_list:
    with open("helmet_data.txt", "a", encoding="utf-8") as file:
        file.write(f"{item}\n")



driver.quit()