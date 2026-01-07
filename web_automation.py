import time
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebAutomationClient:
    def __init__(self, link: str | None = None) -> None:
        if link is None:
            print("WARNING: No link provided. Class not instantiated.")
        self.link = link
        
        print(os.getenv("WEBDRIVER.EXE"))
        self.service = Service(os.getenv("WEBDRIVER_EXE"))
        # self.options = webdriver.EdgeOptions()
        # self.options.add_argument("--headless")
        self.driver = webdriver.Edge(service=self.service) #option
        self.driver.get(self.link)
        self.wait = WebDriverWait(self.driver, 600)
        self.wait.until(EC.element_to_be_clickable((By.ID, "module-tab-default")))
        print('closed')
        self.driver.close()
        return
    
    # def open_page(self):
    #     if self.link is None:
    #         raise RuntimeError("No default link set. Provide a link or set self.link first.")
    #     self.driver.get(self.link)
        