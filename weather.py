# -*- coding: utf-8 -*-

import os
from selenium import webdriver  
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
		chrome_options = Options()  
		chrome_options.add_argument("--headless")  
		driver = webdriver.Chrome(options=chrome_options)  
		driver.get(url)
		try:
			cloudy = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wob_dc"]')))
			Weather.cloudy = cloudy.text

			c = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wob_tm"]')))
			Weather.c = c.text

			chance_rain = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wob_pp"]')))
			Weather.chance_rain = chance_rain.text

		except Exception as e:
			cloudy = ""
			c = 0
			chance_rain = 0
			print("Error finding an element, maybe try again!")
			print("Or just enter on this site: "+url)
		finally:
			driver.close()
			del chrome_options
			del driver
			del cloudy
			del c
			del chance_rain

	def scrap():
		for i in Weather.cities:
			if i.strip() == "":
				continue
			city = i.replace(' ', '+')

			Weather.selenium(Weather.url.format(i))
			print("")
			i = i.rstrip('\n')
			print("---"+i+"---")
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
		try:
			if len(city)>2 and city[0] != '.':
				with open('/home/redarrow129/cities.txt', 'a') as file:
					file.write(city+"\n")

			if city[0] == '.':
				with open('/home/redarrow129/cities.txt', 'r') as f:
					lines = f.readlines()
				with open('/home/redarrow129/cities.txt', 'w') as f:
					for line in lines:
						if line.strip("\n") != city[1:]:
							f.write(line)
		except IndexError:
			exit(0)

		except:
			print("Unknown Error occured!")


print(">>WEATHER<<")
print("")
Weather.load()
print("")
Weather.new_city(input("Write new city or leave blank to exit (.'city' to del): "))