# -*- coding: utf-8 -*-

import requests, os, re
from time import sleep as slp
from bs4 import BeautifulSoup  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  

class Weather:
	url = 'https://www.google.com/search?q={0}+pogoda'
	cities = []
	cloudy = ""
	c = 0
	chance_rain = 0
	weather_link = None

	def selenium(url):
		print("Loading new weather info..")
		slp(2)
		chrome_options = Options()  
		chrome_options.add_argument("--headless")  
		driver = webdriver.Chrome(options=chrome_options)  
		driver.get(url)
		try:
			element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[2]/div/div[2]/div[1]')))
			slp(1)
			print(str(element))
			print(element.text)
			Weather.cloudy = element.text
		except Exception as e:
			element = ""
			print("Error finding an element, maybe try again!")
			print("Or just enter on this site: "+url)
		finally:
			driver.close()
			del chrome_options
			del driver
			del element

	def scrap():
		for i in Weather.cities:
			if i.strip() == "":
				continue
			city = i.replace(' ', '+')
			
			#PART I
			request = requests.get(Weather.url.format(city))
			html = str(request.content)[2:-1]
			soup = BeautifulSoup(html, 'html5lib')
			for link in soup.findAll('a', attrs={'href': re.compile("ttps://maps.google.com/maps")}):
				weather_link = link
			weather_link = str(weather_link)
			weather_link = weather_link[weather_link.index("href=")+6:weather_link.index(">M")-1]

			#PART II PROBLEM WITH SCRAP
			Weather.selenium(weather_link)
			print("")
			print("Miasto: "+i)
			print("Pogoda: "+Weather.cloudy)
			print("Szansa Opadów: "+ str(Weather.chance_rain))
			print("Stopni: "+str(Weather.c))
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

print(">>WEATHER<<")
print("")
Weather.load()
print("")
Weather.new_city(input("Write new city or leave blank to exit: "))