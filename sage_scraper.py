
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#the sage documentation page uses JS to load html, so I used selenium scraper instead of beautiful soup. 

def show_results(titles, list_url):
    parsed_result_list = list(zip(titles,list_url))
    return parsed_result_list

def parse_documentation(search_expression):
    options = Options()
    options.add_argument("--headless")  # disable headless for debugging
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(options=options)
    driver.get(f"https://support.sage.hr/en/?q={search_expression}")

    wait = WebDriverWait(driver, 15)

    links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/en/articles/']")))
    title_elements = driver.find_elements(By.CSS_SELECTOR, "div.t__h3")
    titles = [t.text.strip() for t in title_elements if t.text.strip()]
    list_url = []
    for link in links:
        href = link.get_attribute("href") 
        list_url.append(href)

    driver.quit()

    parsed_result_list = list(zip(titles,list_url))
    return parsed_result_list
