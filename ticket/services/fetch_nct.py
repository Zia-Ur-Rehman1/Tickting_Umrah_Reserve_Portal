from import_selenium import *
import pyotp
options = Options()
options.add_argument("--headless")
import time
# create a new Chrome browser instance
driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'))
driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
# driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'))# navigate to the login page

driver.get('https://trade.newchoudhary.com/')
username_field = driver.find_element(By.ID, 'userMailId')
password_field = driver.find_element(By.ID, 'userPasswordId')
# enter your username and password
username_field.send_keys('hasnaintravelandtours@gmail.com')
password_field.send_keys('Serene@11')
button = driver.find_element(By.XPATH, '//button[@type="submit"]')

# click the button
button.click()

time.sleep(2)
two_factor = driver.find_element(By.ID, 'mfaActivationCodeId')
secret_key = "BYRYEC7INZ7IWSDBNVH6JWY2RGN5PG2PVDJNX4U6RC3BUC23FCJA"
totp = pyotp.TOTP(secret_key)
two_factor.send_keys(totp.now())
login = driver.find_element(By.CLASS_NAME, 'login_btn')
login.click()
driver.get('https://trade.newchoudhary.com/flight/child-offline.html')

td_element = driver.find_element(By.XPATH,'//td[text()="PPPKD0"]')
tr_element = td_element.find_element(By.XPATH, '..')
i_element = tr_element.find_element(By.XPATH, './/td[@class="offline-remarks-td"]/i')
i_element.click()
a_element = driver.find_element(By.XPATH, '//a[contains(text(),"Request Refund")]')
a_element.click()