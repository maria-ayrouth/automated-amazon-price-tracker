import requests

from bs4 import BeautifulSoup
import smtplib

EMAIL="your email"
PASSWORD="your password"

ACCEPT_LANG="en-US,en;q=0.9"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"

URL="https://www.amazon.com/COSORI-Electric-Reminder-Touchscreen-Certified/dp/B07GJBBGHG/ref=sr_1_2?crid=1UQAAOZXDCBB4&dchild=1&keywords=air+fryer&qid=1631459697&sr=8-2"

header={
    "Accept-Language":ACCEPT_LANG,
    "User-Agent":USER_AGENT
}
response=requests.get(url=URL,headers=header)
website=response.text

soup=BeautifulSoup(website,"html.parser")
#print(soup.prettify())


# <span class="a-size-mini olpMessageWrapper"> 4 options from<br>$75.78 </span>


price=soup.find(name="span",class_="a-size-mini olpMessageWrapper").getText()
price_as_float=float(price.split("$")[1])
print(price_as_float)

#<span id="productTitle" class="a-size-large product-title-word-break">
#COSORI Air&nbsp;Fryer&nbsp;Max&nbsp;XL(100 Recipes) Digital Hot Oven Cooker, One Touch Screen with 13 Cooking Functions, Preheat and Shake Reminder, 5.8 QT, Black

title=soup.find(name="span",id="productTitle").getText().strip()
print(title)

BUY_PRICE = 50

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.gmail.com")  as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL,
                            to_addrs=EMAIL,
                            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8"))

