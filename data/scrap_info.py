from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
from bs4 import BeautifulSoup

def normalize_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    return name
def normalize_name_from_id(laptop_id: str) -> str:
    # Remove the "laptop-" or "apple-" prefix if present
    name = re.sub(r"^(laptop-|apple-)", "", laptop_id)
    # Replace dashes with spaces
    name = name.replace("-", " ")
    # Capitalize first letters
    name = " ".join(word.capitalize() for word in name.split())
    return name

links_df = pd.read_csv("laptop_links.csv")

options = Options()
options.add_argument("--headless")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

rows = []

for _, row in links_df.iterrows():
    laptop_id = row["laptop_id"]
    link = row["laptop_link"]

    driver.get(link)
    time.sleep(2)

    # --- click "Show full specs" if available ---
    try:
        show_full_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="thong-so-ky-thuat"]/div/button'))
        )
        driver.execute_script("arguments[0].click();", show_full_btn)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.technical-modal-container"))
        )
    except:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")



    # --- price ---
    try:
        price_tag = soup.select_one("div.sale-price")
        price = price_tag.get_text(strip=True) if price_tag else None
    except:
        price = None

    specs = {}

    # --- inline specs ---
    inline_rows = soup.select("#thong-so-ky-thuat tr.technical-content-item")
    for r in inline_rows:
        tds = r.find_all("td")
        if len(tds) >= 2:
            label = tds[0].get_text(strip=True)
            value = tds[1].get_text(strip=True).replace("\n", " ")
            specs[label] = value

    # --- modal specs ---
    modal_rows = soup.select("div.technical-modal-container tr.technical-content-item")
    for r in modal_rows:
        tds = r.find_all("td")
        if len(tds) >= 2:
            label = tds[0].get_text(strip=True)
            value = tds[1].get_text(strip=True).replace("\n", " ")
            specs[label] = value  # override inline if duplicate
    product_name = normalize_name_from_id(laptop_id)
    # --- assemble row ---
    row_data = {
        "laptop_id": laptop_id,
        "product_name": product_name,
        "price": price,
        "link": link
    }
    row_data.update(specs)
    rows.append(row_data)

driver.quit()

# save
df = pd.DataFrame(rows)
df.to_csv("laptop_specs.csv", index=False, encoding="utf-8-sig")
