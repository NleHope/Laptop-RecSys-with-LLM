# scrape_links.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

url = "https://cellphones.com.vn/laptop.html"
driver.get(url)

wait = WebDriverWait(driver, 10)

# Keep clicking "Show More"

while True:
    try:
        show_more = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="blockFilterSort"]/div[3]/div/div[2]/a')
        ))
        ActionChains(driver).move_to_element(show_more).click().perform()
        time.sleep(2)
        
    except Exception:
        print("No more 'Show More' button.")
        break

# Collect product cards
products = driver.find_elements(By.CSS_SELECTOR, "div.product-info-container.product-item")

data = []
for product in products:
    try:
        link_tag = product.find_element(By.CSS_SELECTOR, "a.product__link")
        product_link = link_tag.get_attribute("href")
        laptop_id = product_link.split("/")[-1].replace(".html", "")
        data.append({"laptop_id": laptop_id, "laptop_link": product_link})
    except Exception as e:
        print("Error:", e)

df = pd.DataFrame(data)
df.to_csv("laptop_links.csv", index=False, encoding="utf-8-sig")

driver.quit()
print("Saved laptop_links.csv")
