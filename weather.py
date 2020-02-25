import requests, os, re
from bs4 import BeautifulSoup

class Weather:
	url = 'https://www.google.com/search?q={0}+pogoda'
	cities = []

	def scrap():
		for i in Weather.cities:
			city = i.replace(' ', '+')
			cloudy = "Zachmurzenie"
			c = 0
			chance_rain = 0
			weather_link = ""
			
			#PART I
			request = requests.get(Weather.url.format(city))
			html = str(request.content)[2:-1]
			soup = BeautifulSoup(html, 'html5lib')
			soup.prettify()
			
			for link in soup.findAll('a', attrs={'href': re.compile("ttps://maps.google.com/maps")}):
				weather_link = link
			weather_link = str(weather_link)
			weather_link = weather_link[weather_link.index("href=")+6:weather_link.index(">M")-1]

			#PART II PROBLEM WITH SCRAP
			request = requests.get(weather_link)
			html = str(request.content)[2:-1]
			soup = BeautifulSoup(html, 'html5lib')
			soup.prettify()
			
			cloudy = soup.find("div", {"jstcache" : "171"})

			print(soup)
			
			print("")
			print("Miasto: "+i)
			print("Pogoda: "+str(cloudy))
			print("Szansa Opadów: "+ str(chance_rain))
			print("Stopni: "+str(c))
			print("")

	
	def load():
		if os.path.exists('/home/redarrow129/cities.txt') == False:
			file = open('/home/redarrow129/cities.txt', 'w')
			file.write('')
			file.close()
			print('Created file in user\'s directory "cities.txt"')
		with open('/home/redarrow129/cities.txt', 'r') as file:
			for line in file.readlines():
				if line == "" or line == " " or line == r"\n":
					continue
				Weather.cities.append(line)
		Weather.scrap()


	def new_city(city):
		if len(city)>2:
			with open('/home/redarrow129/cities.txt', 'a') as file:
				file.write(city+"\n")
		else:
			exit(0)


print(">>WHEATER<<")
print("")
Weather.load()
print("")
Weather.new_city(input("Write new city or leave blank to exit: "))