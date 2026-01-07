from web_automation import WebAutomationClient as WAC


def main():
    # WEBDRIVER_EXE = r'C:\Users\Zach_Schulz-Behrend\dev\webdriver\edgedriver_win64_143.0.3650.96\msedgedriver.exe'
    link = 'https://imagewatch.dell.com/#/home' 
    # service = webdriver.EdgeService(executable_path=WEBDRIVER_EXE)
    #     # options = webdriver.EdgeOptions()
    #     # options.add_argument("--headless")
    #     # driver = webdriver.Edge(service=service, options=options)
    # driver = webdriver.Edge(service=service)
    # driver.get(link)
    # wait = WebDriverWait(driver, 600)
    # wait.until(EC.element_to_be_clickable((By.ID, "module-tab-default")))
    # sleep(600)
    # driver.close()
    
    WAC(link)

if __name__ == "__main__":
    main()
