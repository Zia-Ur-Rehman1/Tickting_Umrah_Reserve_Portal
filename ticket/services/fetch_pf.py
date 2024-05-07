from import_selenium import *

options = Options()
options.add_argument("--headless")

# create a new Chrome browser instance
driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
# driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'))# navigate to the login page

driver.get('http://www.airsial.net/eticket/')
driver.switch_to.frame('mainFrame')

# find the username and password fields
username_field = driver.find_element(By.NAME, 'uname')
password_field = driver.find_element(By.ID, 'upass')
# enter your username and password
username_field.send_keys('hasnainmuxtvl')
password_field.send_keys('Serene11')
# username_field.send_keys('hassaantvl')
# password_field.send_keys('tgv567')
# find the login button and click it
login_button = driver.find_element(By.ID, 'loginbtn')
login_button.click()
try:
    close_button = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//button[@data-dismiss="modal"]'))
    )
    close_button.click()
except Exception as e:
    print(f"An error occurred: {e}")

# at this point, you should be logged in
# you can add more code here to navigate the website, scrape data, etc.

# find the dl element with the class acc-cpanel
dl_element = driver.find_element(By.CSS_SELECTOR, 'dl.acc-cpanel')

# find the fourth dt and dd elements
dt_elements = dl_element.find_elements(By.TAG_NAME, 'dt')
dd_elements = dl_element.find_elements(By.TAG_NAME, 'dd')

# get the text of the fourth dt and dd elements
# note that we use index 3 because list indices start at 0
dt_text = dt_elements[2].text
dd_text = dd_elements[2].text

print(f'{dt_text} : {dd_text}')
driver.get('http://www.airsial.net/eticket/tkt_agent_sales_detail.php?cc=1')


# get the current month first and last date
current_date = datetime.date.today()
first_date = current_date.replace(day=1).strftime('%d-%m-%Y')
last_date = (current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
last_date = last_date.strftime('%d-%m-%Y')

# find the d_from and d_to fields
d_from_field = driver.find_element(By.NAME, 'd_from')
d_to_field = driver.find_element(By.NAME, 'd_to')

# set the dates using JavaScript
driver.execute_script("arguments[0].value = arguments[1]", d_from_field, first_date)
driver.execute_script("arguments[0].value = arguments[1]", d_to_field, last_date)
# when you're done, close the browser
select_element = driver.find_element(By.NAME, 'staff_code')
select_object = Select(select_element)
select_object.select_by_index(1)

# find the select element
select_element = driver.find_element(By.NAME, 'dom')

# create a Select object
select_object = Select(select_element)

# select the second option
select_object.select_by_index(1)
input_element = driver.find_element(By.NAME, 'B1')

# click the input element
input_element.click()
link_element = driver.find_element(By.LINK_TEXT, 'TICKET SALE')
link_element.click()

# find the table by its class name
table = driver.find_element(By.CLASS_NAME, 'tableReport')

# find all the rows in the table
rows = table.find_elements(By.TAG_NAME, 'tr')

# create a list to hold the data
data = []

# iterate over the rows
for row in rows[:-1]:
    # find the cells within each row
    cells = row.find_elements(By.TAG_NAME, 'td')
    # check if the cells exist
    if cells:
        data.append([cells[1].text, cells[2].text, cells[4].text, cells[20].text])

# print the data
for row in data:
    print(row)

driver.quit()
