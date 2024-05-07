from import_selenium import *
options = Options()
options.add_argument("--headless")

# create a new Chrome browser instance
# driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)

# driver.get('https://www.airblue.com/Agents/')
# driver.get('https://ta1.flydubai.com/en/user/signin/?external=true')
driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'))
driver.get('https://sprintauth.flydubai.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3DTA_FZ_P2%26state%3DbThIQ2FQbjcuclVvdHlyUE8wN0tnUFpwNmhCV3JMUTQzaktJYTFmWjVKWTVysemicolon%25252F%26redirect_uri%3Dhttps%253A%252F%252Fta.flydubai.com%252F%26scope%3Doffline_access%2520openid%2520sprintauthapi%2520travelagencyapi%2520reservationapi%26code_challenge%3D1-IOnWLkFuiXKuf3YJhZTav_OdB8-1Ew_sjLEFYr-VA%26code_challenge_method%3DS256%26nonce%3DbThIQ2FQbjcuclVvdHlyUE8wN0tnUFpwNmhCV3JMUTQzaktJYTFmWjVKWTVy')



# username_field = driver.find_element(By.ID, 'UserName')
username_field = driver.find_element(By.ID, 'username')

password_field = driver.find_element(By.ID, 'passwordWrap')
username_field.send_keys('27910260hasna')
password_field.send_keys('S@hil2010')
iframe = driver.find_element(By.XPATH,'//iframe[@title="reCAPTCHA"]')
driver.switch_to.frame(iframe)
element = driver.find_element(By.ID, 'recaptcha-anchor')
element.click()

driver.execute_script("arguments[0].setAttribute('aria-checked', 'true')", element)
login_button = driver.find_element(By.NAME, 'button')
login_button.click()
