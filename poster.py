import time
import urllib.request
import random
from random import randrange
from random import randint
import pyautogui
pyautogui.FAILSAFE = False
from bs4 import BeautifulSoup as bs
import lxml
from lxml import etree
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

query = (input("Enter MLS# or Address: "))

"""print(open('Proxies.txt', 'r').read())
account_number = str(input('Acct #? '))
total_posts = int(input('How many? '))
posts_remaining = total_posts
post_number = 0

while post_number <= total_posts:
    post_number += 1
    print('Post #' + str(post_number)+ '...')"""
driver = webdriver.Chrome()
xpath = driver.find_element_by_xpath
iframe = driver.switch_to.frame
id = driver.find_element_by_id
driver.get('https://fl.flexmls.com')
time.sleep(1)
xpath('//*[@id="j_username"]').clear()
xpath('//*[@id="j_username"]').send_keys('277011416')
xpath('//*[@id="password"]').click()
xpath('//*[@id="password"]').clear()
xpath('//*[@id="password"]').send_keys('Carmen1732')
xpath('//*[@id="loginbtn"]').click()
time.sleep(2)



            ####       SEARCH        ####



driver.get('https://fl.flexmls.com/')
try:
    iframe(id("top_frame"))
except:
    driver.get('https://fl.flexmls.com/')
    iframe(id("top_frame"))

xpath('//*[@id="quick-launch"]/div/div/input').click()
xpath('//*[@id="quick-launch"]/div/div/input').send_keys(query)
time.sleep(3)
xpath('//*[@id="quick-launch"]/div/div/input').send_keys(Keys.ENTER)


#GO TO DATA
time.sleep(3)
driver.switch_to_default_content()
iframe(id("top_frame"))
iframe(id("view_frame"))
time.sleep(2)
xpath('//*[@id="tab_detail"]').click()
iframe(id("iframe_detail"))
f = open('mls_html.txt', 'w+')
f.write(driver.page_source)
#GRAB THE IMAGES
driver.switch_to_default_content()
iframe(id("top_frame"))
iframe(id("view_frame"))
time.sleep(1)
xpath('//*[@id="tab_tour"]').click()
iframe(id("iframe_tour"))
time.sleep(2)
image_number = 0
all_images = ""
src = str(xpath("//*[@id='listing-photo']").get_attribute("src"))
while image_number < int(xpath('//*[@id="photo-count"]/table/tbody/tr/td[3]').text) :
    if image_number < 24:
        image_name = "image" + str(image_number) + ".jpg" #CREATE A UNIQUE FILE NAME
        image_number  += 1
        urllib.request.urlretrieve(src, image_name) #DOWNLOAD IMAGE AND ASSIGN FILE NAME
        all_images += image_name + " " #ADD FILE NAME TO all_images STRING (see uploader in cl_poster.py)
        xpath('//*[@id="photo-switcher-right"]').click() #SWITCH TO NEXT IMAGE
        src = str(xpath("//*[@id='listing-photo']").get_attribute("src"))
    else:
        break
image_list = all_images.split() #CREATE LIST FROM all_images #WILL NEED TO UPLOAD
f = open('mls_html.txt', 'r')



    ###        GRAB DATA        ###



mls_html = f.read()
mls_soup = bs(mls_html, "lxml")
span = mls_soup.findAll("span")
td = mls_soup.findAll("td")
address = span[5].text 
zip = address[-5:]
price = span[8].text
status = span[12].text
area = span[17].text
geo_area = span[23].text
year = td[26].text
city = span[30].text
if 'Riviera' in city:
    city = 'Singer Island'
county = span[37].text
subdivision = span[54].text
pets_allowed = span[58].text
bedrooms = span[74].text
bathrooms_full = span[85].text
square_feet = span[88].text
bathrooms_total = span[105].text
listing_company = span[168].text
listing_agent = span[171].text
phone_number = span[172].text
email = span[173].text
garage_spaces = span[192].text
view = span[200].text
flooring = span[202].text
waterfront_details = span[205].text
heating = span[206].text
interior_features = span[208].text
restrict = span[211].text
cooling = span[213].text
exterior_features = span[215].text
parking = span[217].text
appliances = span[219].text
furnished = span[225].text
type = span[232].text
x = lxml.etree.HTML(mls_html)
public_remarks = x.xpath('/html/body/text()')[-5]
public_remarks = public_remarks[1:]
#CLEAN TEXT
city = re.sub('City: ', '', city)
year = re.sub('[^0-9]', '', year)
pets_allowed = re.sub('Pets Allowed: ', '', pets_allowed)
bedrooms = re.sub('[^0-9]', '', bedrooms)
bathrooms_total = re.sub('[^0-9]', '', bathrooms_total)
square_feet = re.sub('[^0-9]', '', square_feet)
furnished = re.sub('Furnished: ', '', furnished)
type = re.sub('Type: ', '', type)
type = re.sub('/Coop', '', type)
type = re.sub('Single Family Detached', 'Single Family Home', type)
type = re.sub('Duplex/Triplex/Quadplex', 'Duplex', type)
bathrooms_total = bathrooms_total[0]
bathrooms_total = re.sub(' ', '', bathrooms_total)

    

        ###        TITLE GENERATOR        ###



#   bed_bath & type RANDOMIZER
bbint = randint(1, 6)
if bbint == 1 or bbint == 5:
    bed_bath = bedrooms + '/' + bathrooms_total
if bbint == 2 or bbint == 6:
   bed_bath = bedrooms + ' bed ' + '/ ' + bathrooms_total + ' bath'
if bbint == 3:
    bed_bath =  bedrooms + ' Br | ' + bathrooms_total + ' Bath'
if bbint ==4:
    bed_bath = bedrooms + '|' + bathrooms_total
if 'Condo' in type:
    if randint(1, 2) == 1:
        type = 'Apartment'
tl = [bed_bath, ''] 
random.shuffle(tl)
#   ADD waterfront_details
if 'Intracoastal' in waterfront_details:
    waterfront_title = 'True'
    ptstr = 'On Intracoastal'
else:
    waterfront_title = 'False'
    ptstr = "in"
#   CREATE TITLE    
if waterfront_title == 'True':
    posting_title = "{} {} {}".format(tl[0], tl[1], ptstr)
else:
    if randint(1, 3) == 1:
        posting_title = "{} {} {}".format(tl[0], tl[1], city)
    else:
        posting_title = "{} {} {} {}".format(tl[0], tl[1], ptstr, city)
#   TITLE LENGTHENER
tlint = randint(1, 8)
if len(posting_title) < 50:
    #25% ADD ADJECTIVE
    if tlint == 2 or tlint == 3 or tlint == 5 or tlint == 6:
        adjective = randint(1, 10)
        if adjective == 1:
            posting_title =  'Gorgeous ' + posting_title
        if adjective == 2:
            posting_title =  'Beautiful ' + posting_title
        if adjective == 3:
            posting_title =  'ENORMOUS ' + posting_title
        if adjective == 4:
            posting_title =  'Regal ' + posting_title
        if adjective == 5:
            posting_title =  'Spacious ' + posting_title
        if adjective == 6:
            posting_title =  'Modern ' + posting_title
        if adjective == 7:
            posting_title =  'Breath-taking ' + posting_title
        if adjective == 8:
            posting_title =  'Charming ' + posting_title
        if adjective == 9:
            posting_title =  'Elegant ' + posting_title
        if adjective == 10:
            posting_title =  'Luxurious ' + posting_title
#   ! RANDOMIZER
random_number = randint(1, 4)
if randint(1, 2) == 1:
    posting_title += ' '
if  random_number == 1:
    posting_title += '!'
if random_number == 2:
    posting_title += '!!'
#   CAPS RANDOMIZER
if randint(1, 2) == 1: 
    posting_title = posting_title.upper()

    

posting_body = """{}

{}

Call Sonia (786) 486-8174
If this property doesn't fit your needs, feel free to call or text me and I may have other properties to pass by you!

{}
{} Bedrooms
{} Bathrooms
{} ft²

{} Per Month










Sonia Quesada is a licensed Realtor at Premier Properties.
MLS Listing courtesy of {}""".format(address, public_remarks, address, bedrooms, bathrooms_total, square_feet, price, listing_company)





        ###        LOGIN TO CRAIGSLIST        ###



password = 'Myidis0603009548'
login = 'richard.quesada@hotmail.com'
driver.get('https://accounts.craigslist.org/login?lang=en&cc=us&rt=P&rp=%2Fk%2Fgt630Uxr6BGyuWlnewAnlQ%2FoXnAw')    
id('inputEmailHandle').send_keys(login)
time.sleep(1)
id('inputPassword').send_keys(password)
time.sleep(1)
id('inputPassword').send_keys(Keys.ENTER)
time.sleep(1)
driver.get('https://miami.craigslist.org/')
try: #MAKE SURE PAGE LOADED
    xpath('//*[@id="post"]').click()#POST TO CLASSIFIEDS
except:
    driver.get('https://miami.craigslist.org/')
time.sleep(1)
xpath('/html/body/article/section/form/ul/li[3]/label/input').click()
time.sleep(1)
xpath('/html/body/article/section/form/button').click()#PALM BEACH COUNTY
time.sleep(1)
xpath('/html/body/article/section/form/ul/li[4]/label/span[1]/input').click()
time.sleep(2)
xpath('//*[@id="new-edit"]/div/label/label[2]/input').click()
time.sleep(2)



        ###        GENERATE POST        ###



xpath('//*[@id="PostingTitle"]').clear()
xpath('//*[@id="PostingTitle"]').send_keys(posting_title)
xpath('//*[@id="GeographicArea"]').clear()
xpath('//*[@id="GeographicArea"]').send_keys(city + ', ' + 'FL')
xpath('//*[@id="postal_code"]').clear()
xpath('//*[@id="postal_code"]').send_keys(address[-5:])
xpath('//*[@id="PostingBody"]').clear()
xpath('//*[@id="PostingBody"]').send_keys(posting_body)
xpath('//*[@id="new-edit"]/div/fieldset[1]/div/div[1]/label[2]/label/input').clear()
xpath('//*[@id="new-edit"]/div/fieldset[1]/div/div[1]/label[2]/label/input').send_keys(square_feet)
xpath('//*[@id="new-edit"]/div/fieldset[1]/div/div[1]/label[1]/label/input').clear()
xpath('//*[@id="new-edit"]/div/fieldset[1]/div/div[1]/label[1]/label/input').send_keys(price)
xpath('//*[@id="Bedrooms-button"]/span[2]').click()
bedroom_number = str(int(bedrooms)+8)
xpath('//*[@id="ui-id-%s"]'%bedroom_number).click()
xpath('//*[@id="ui-id-4-button"]').click()
time.sleep(1)

if bathrooms_total == 1:
    xpath('//*[@id="ui-id-20"]').click()
if bathrooms_total == 2:
    xpath('//*[@id="ui-id-22"]').click()
if bathrooms_total == 3:
    xpath('//*[@id="ui-id-24"]').click()
if bathrooms_total == 4:
    xpath('//*[@id="ui-id-26"]').click()

if "Single Family" in type:
    xpath('//*[@id="ui-id-1-button"]').click()
    xpath('//*[@id="ui-id-42"]').click()

if "Yes" in pets_allowed:
    xpath('//*[@id="new-edit"]/div/fieldset[1]/div/div[3]/label[1]/input').click()
    xpath('//*[@id="new-edit"]/div/fieldset[1]/div/div[3]/label[2]/input').click()
xpath('//*[@id="new-edit"]/div/fieldset[2]/div/div[1]/div[2]/label/label[2]/input').click() #Show Email
xpath('//*[@id="new-edit"]/div/fieldset[2]/div/div[2]/label/input').click() #Show phone number
xpath('//*[@id="new-edit"]/div/fieldset[2]/div/div[2]/div[2]/label[1]/label/input').send_keys('(786) 486-8174')
xpath('//*[@id="new-edit"]/div/fieldset[2]/div/div[2]/div[2]/label[3]/label/input').send_keys('Sonia Quesada')
xpath('//*[@id="new-edit"]/div/fieldset[3]/div/label/input').click()#Show address
xpath('//*[@id="new-edit"]/div/fieldset[3]/div/div/label[1]/label/input').send_keys(address)
xpath('//*[@id="new-edit"]/div/div[4]/div/button').click()
xpath('//*[@id="leafletForm"]/button').click()
if 'geoverify' in driver.current_url:
    xpath('//*[@id="leafletForm"]/button').click() #MAP PAGE



        ###        UPLOAD IMAGES        ###


       
try:
    xpath('//*[contains(@id, "img")]/form/button')
    while xpath('//*[contains(@id, "img")]/form/button'):
        xpath('//*[contains(@id, "img")]/form/button').click()
except:
    pass
time.sleep(1)
try:
    xpath('//*[@id="classic"]').click()#SWITCH TO CLASSIC UPLOADER
except:
    xpath('//*[@id="classic"]').click()
for i in range(len(image_list)): #USE IMAGE LIST TO LOCATE AND UPLOAD IMAGES
    if i < 24: #STOP UPLOADING AFTER UPLOAD LIMIT
        image_location = str(os.getcwd() + '\\%s'%image_list[i])#ASSIGN IMAGE LOCATION TO VARIABLE
        xpath('//*[@id="uploader"]/form/input[3]').send_keys(image_location)#TYPE IMAGE LOCATION INTO UPLOADER
        os.remove(os.getcwd() + '\\%s'%image_list[i]) # DELETE IMAGES 
xpath('/html/body/article/section/form/button').click()#PUBLISH PAGE
xpath('//*[@id="publish_top"]/button').click()#PUBLISH
driver.get('https://accounts.craigslist.org/login/home') #ACCT PAGE
driver.get('https://accounts.craigslist.org/login/home')#ACCT PAGE REFRESH
print('POST SUCCESSFUL!')
