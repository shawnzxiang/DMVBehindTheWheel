# DMVBehindTheWheel

I was tired of not finding a ideal DMV behind the wheel appointment and do all the manual work of typing my name, birth, office id, licence number, etc.

So I based off a blog post(source code https://gist.github.com/saikatbhadra/6629031) for booking a DMV office appointment, and I wrote the equivalent one for DMV behind the wheel.

I was very pleased that I succesfully booked my appointment several times when someone canceled it within my desirable date that moved my date two weeks earlier. Please also note this script finds whatever the earliest time falls into, it does not check later time on the second page. 

You will need to do the following:

1. Look up your office id in officeIdList

2. Write all your configuration in dmv.py

3. Run in python (I used pyCharm which downloads all the library with 2.7 compatible)

Anyway, this script can: 

1. Find the appointment (uncomment the rest of if loop if you do not want the script to book it for you)

2. Book the appointment for you in as many as four steps. (Web errors can occur at this time such as when someone booked it     before you in which case it will retry)

3. If there is no appointment available with the time specified, then it will retry again later. 

4. Redirect you to appointment page, you can confirm and make sure it is booked while the program is terminated

5. I used a simple PHP script on my site to send a text message.(see text.php) However, this requires a server setup for PHP. My email can never authenticate with python, so I just used a PHP script on my website instead. Anyway, this is kind of trivial since the program will terminate once your appointment is successful.  


Lastly, good luck with your DMV behind the wheel appointment :)
