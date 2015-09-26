# Written by Shawn Xiang
# This script is used to schedule Behind the wheel appointment in all California DMV

# Based on https://gist.github.com/saikatbhadra/6629031 -> This script can be used to schedule office appointment

import mechanize
from bs4 import BeautifulSoup
from datetime import datetime
import time
import webbrowser

# ***CONFIGURATION: PLEASE CHANGE ALL THE FIELDS BELOW ACCORDINGLY***

YEAR = '2015' #Used to identify the string

TGT_DATE = 'October 1, 2015' #Example: 'September 30, 2015'
START_DATE = 'September 18, 2015' # Example: 'September 18, 2015'
OFFICE_ID = '111' # 3 digit number. Find it by inspect element of the web page to find the page id
NAME = 'JOHN SMITH' # Example: FIRSTNAME LASTNAME
DATE_OF_BIRTH = '12-21-1993' # Example: 12-21-1993
LICENCE_NUMBER = "Y1234567" # Example: Y1234567
TEL_NUMBER = "530-123-4567" # Example: 530-123-4567
TASK = 'DT' # DT: driving. Do not change unless you want to schedule motorcycle

# Please set it 120 secs or higher to be considerate for others
REFRESH_RATE_IN_SEC = 30 # Refresh rate in seconds

# Hour of the day, military time / 24hr e.g. 16 is 4pm
HOUR_START = 9
HOUR_END = 16

# ***End of Config***


form_url = 'https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do'

# Schedule function takes care of automatic scheduling based on the info entered and dates
def schedule(targetDate,name,officeId,telNumber,birthday,dlNumber,fromDate):
    tels = telNumber.split('-')
    births = birthday.split('-')
    names = name.split(' ')

    try:
        from_date = datetime.strptime(fromDate,'%B %d, %Y')
    except Exception:
        print("Your entered date is not parsable")
        from_date = datetime.today().strftime("%B %d, %Y")

    tgt_date = datetime.strptime(targetDate,'%B %d, %Y')

    # First enter all the information in the browser
    br = mechanize.Browser()

    # Catch server or other unexpected error
    try:
        br.open(form_url)
    except Exception:
        print("The website is down or unexpected error occurred while retrieving")
        return False

    br.select_form(name="ApptForm")
    br['officeId']=[officeId]
    br.find_control(name="requestedTask").value = ["DT"]
    br['firstName'] = names[0]
    br['lastName'] = names[1]
    br['telArea'] = tels[0]
    br['telPrefix'] = tels[1]
    br['telSuffix'] = tels[2]
    br['dlNumber'] = dlNumber
    br['birthMonth'] = births[0]
    br['birthDay'] = births[1]
    br['birthYear'] = births[2]

    result = br.submit()
    result_html =  br.response().read()
    soup = BeautifulSoup(result_html, "html.parser")
    results = soup.findAll('p',class_="alert")
    logString = ""

    # if from date is later than target date, swap them
    if (from_date > tgt_date):
        temp = from_date
        from_date = tgt_date
        tgt_date = temp

    #Loop through the elements in the response (html)

    for result in results:
        if (YEAR in result.get_text()):
            appt_text = result.get_text()

            appt_date = datetime.strptime(appt_text,'%A, %B %d, %Y at %I:%M %p')
            print ("Earliest time: %s that is %s days from now" %(appt_text, str((appt_date - datetime.today()).days)))
            
            #You can specify the time you want
            if appt_date <= tgt_date and appt_date>=from_date and appt_date.hour >=HOUR_START and appt_date.hour <=HOUR_END:
                print("We found the date: %s to be possible", appt_date)

                logString+= "\nCongratulations! You've found a date earlier than your target. Scheduling the appointment..."

                # The fifth form is always the submit. Check the corresponding HTML if this has been changed
                # Extract by ID or name is not possible as for now since cancel has the same name and id as submit
                br.select_form(nr=4)
                r = br.submit()

                # Confirming the date selected
                logString+= "\nConfirming the appointment..."

                if (checkForm(br)):
                    br.select_form(nr=4)
                    r = br.submit()
                    s = BeautifulSoup(br.response().read(), "html.parser")

                    logString += "\nThe final step is to actually schedule it...Use it when necessary.\n"

                    # Cancel previous appointment
                    if (checkForm(br)):
                        br.select_form(nr=4)
                        r = br.submit()
                        s = BeautifulSoup(br.response().read(), "html.parser")


                        print (logString)

                        #Open up a browser to check if it is register
                        #When there is a lag, you can always refresh it or register again to check if you have registered
                        webbrowser.open('https://www.dmv.ca.gov/foa/clear.do?goTo=viewCancel')

                        with open("record.txt", "a") as myfile:
                            myfile.write(logString)

                        #While loop ends
                        return True


                    else :
                        print("System Unavailable when trying to cancel previous schedule (3rd page). Don't worry, we will retry in %i seconds"%REFRESH_RATE_IN_SEC)
                        return False

                else:
                    print("System Unavailable when trying to confirm (2nd page). Don't worry, we will retry in %i seconds"%REFRESH_RATE_IN_SEC)
                    return False
            else:
                logString += "Sorry there is no appointment available between date %s and %s. Retrieved at %s "%(fromDate,targetDate,datetime.today().strftime("%X"))
                print (logString)
                with open("record.txt", "a") as myfile:
                    myfile.write(logString)
                return False
        elif ('System Unavailable' in result.get_text()):
                print("System is unavailable after submitted (1st page). Don't worry, we will retry in %i seconds"%REFRESH_RATE_IN_SEC)
                return False



def checkForm(rawParse):
    for frm in rawParse.forms():
         if str(frm.attrs["id"])=="ApptForm":
          return True

    return False

# while loop: retrieve every REFRESH_RATE_IN_SEC if it is false
while not schedule(TGT_DATE, NAME, OFFICE_ID, TEL_NUMBER, DATE_OF_BIRTH, LICENCE_NUMBER, START_DATE):
    print ("\n")
    time.sleep(REFRESH_RATE_IN_SEC)
