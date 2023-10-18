from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re


driver = webdriver.Chrome()

with open('test_item.txt', 'r') as file:
    test_items = file.read().splitlines()

all_links = []
all_asin_codes = []


for item in test_items:
    query_text = f"{item} ASIN CODE site:amazon.com"
    driver.get(f"https://www.google.com/search?q={query_text}")


    # try:
    #     amazon_link = driver.find_element(By.CSS_SELECTOR, "div.yuRUbf a").get_attribute('href')
    #     if amazon_link.startswith("https://www.amazon.eg/") or amazon_link.startswith("https://www.amazon.com/"):
    #         all_links.append(amazon_link)
    #         # Extract ASIN code using regular expression
    #         asin_code = re.search(r'/dp/([A-Z0-9]{10})', amazon_link).group(1)
    #         all_asin_codes.append(asin_code)
    #         print("true")
    #     else:
    #         all_links.append("Not found")
    #         all_asin_codes.append("Not found")
    #
    # except Exception as e:
    #     print(f"the following error occurred {e}")
    try:
        amazon_links = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")

        for amazon_link in amazon_links:
            link = amazon_link.get_attribute('href')

            if link.startswith("https://www.amazon.com/") or link.startswith("https://www.amazon.eg/"):
                all_links.append(link)
                print(f"Link = {link}")
            else:
                all_links.append("Not Found")
            # Extract ASIN code using regular expression
            asin_code = re.search(r'/dp/([A-Z0-9]+)', link)
            if asin_code:
                asin_code = asin_code.group(1)
            else:
                asin_code = "Not found"
            all_asin_codes.append(asin_code)
            print("true")
            break  # Break the loop if the condition is met



    except Exception as e:
        print(f"the following error occurred: {e}")
time.sleep(5)
result_dict = {}

print(test_items)
print(len(test_items))
print(all_links)
print(len(all_links))
print(all_asin_codes)
print(len(all_asin_codes))

# Iterate through the lists and create the dictionary
for serial_number, (item_name, item_link, asin_code) in enumerate(zip(test_items, all_links, all_asin_codes), start=1):
    # Create a list with item name, item link, and ASIN code
    item_data = [item_name, item_link, asin_code]
    # Add the list to the dictionary with serial number as key
    result_dict[serial_number] = item_data

# print(result_dict)

for key, value in result_dict.items():
    serial_number = key
    name, link, asin_code = value

    sheet_link = "https://docs.google.com/forms/d/e/1FAIpQLSdeMwFjvDH0pR9wi-Gi7QiNIZEEERfgTEBN-4VQ5QZwrpe_6w/viewform"
    form_item = driver.get(sheet_link)
    time.sleep(1)
    item_name = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/textarea')
    item_name.send_keys(name)
    time.sleep(1)
    item_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/textarea')
    item_link.send_keys(link)
    time.sleep(1)
    item_href = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[2]/textarea')
    item_href.send_keys(asin_code)
    time.sleep(1)
    item_submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    item_submit.click()
    time.sleep(1)


driver.quit()