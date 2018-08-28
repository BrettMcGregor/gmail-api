from bs4 import BeautifulSoup
import requests

with open('message2.html', 'r') as file:
    html = str(file.readlines())
# print(html)
# print(type(html))

# parse to find the click.email.woolworths link within the anchor element containing the text 'ACTIVATE NOW'
msg = BeautifulSoup(html, "html.parser")
attr = msg.find_all(attrs={"bgcolor": "#f47920"})

# if the offer does not contain the orange activate now button then look for the green one which is used sometimes
if not attr:
    attr = msg.find_all(attrs={"bgcolor": "#125434"})

link = attr[0].find("a")
# print(link)
# print()
# print(link.get_text())

print(link.attrs['href'])

activation_link = link.attrs['href']
# make a request to the link to activate the offer
r = requests.get(activation_link)
with open("activation_response.html",'w') as file:
    print(r, file=file)
