Función formatted_text <- format_flights (flight)
	formatted_text <- ''
	formatted_text <- formatted_text+'Salida: {flight.get(day)} a las {flight.get(start)} en {flight.get(departure)}\n'
	Si !ends_other_day Entonces
		formatted_text <- formatted_text+'Llegada: {flight.get(end)} en {flight.get(destination)}\n'
	SiNo
		formatted_text <- formatted_text+'Llegada: ({flight.get(is_other_day)[0].text}) {flight.get(end)} en {flight.get(destination)}\n'
	FinSi
	Si !is_connection Entonces
		formatted_text <- formatted_text+'Tipo de vuelo: {flight.get(type)}\n'
	SiNo
		formatted_text <- formatted_text+'Tipo de vuelo: {flight.get(type)} ({flight.get(is_connection)[0].text})\n'
	FinSi
	formatted_text <- formatted_text+'Duración: {flight.get(time)}\n'
	formatted_text <- formatted_text+'Precio: ${flight.get(price)}\n\n'
FinFunción

Función current_flights <- viva_flights
	flight_date_format <- flight_date.replace['-','']
	url <- 'https://www.vivaaerobus.com/es-mx/book/options?itineraryCode={departure}_{destination}_{flight_date_format}&passengers=A1'
	driver <- webdriver.Chrome[options=options]
	driver <- driver.get[url]
	driver <- driver.maximize_window[]
	flight <- ()
	flight_formatted <- ''
	flight_day <- WebDriverWait.until[By.XPATH,'//day')
	// time.sleep(2.5)
	button <- WebDriverWait.until[By.XPATH,'button')
	Si button Entonces
		driver <- driver.execute_script['arguments[0].scrollIntoView(true);',button]
		// time.sleep(2.5)
		driver <- driver.execute_script['arguments[0].click();',button]
		// time.sleep(5)
	FinSi
	flight_options <- driver.find_elements[By.XPATH,'//app-flight-option')
	Para flight<-flight_options Hasta . Hacer
		flight_price <- flight.find_elements[By.XPATH,'.//default-price')
		Si !flight_price Entonces
			// continue
		FinSi
		flight_price <- flight_price.text
		flight_start <- flight.find_element[By.XPATH,'.//hour_start')
		flight_departure <- flight.find_element[By.XPATH,'.//place_start')
		flight_end <- flight.find_element[By.XPATH,'.//hour_end')
		flight_destination <- flight.find_element[By.XPATH,'.//place_end')
		flight_time <- flight.find_element[By.XPATH,'.//flight_time')
		flight_type <- flight.find_element[By.XPATH,'.//flight_type')
		flight_is_other_day <- flight.find_elements[By.XPATH,'.//ends_other_day')
		flight_is_connection <- flight.find_elements[By.XPATH,'.//is_connection')
		flight_formatted <- flight_formatted+format_flights(flight)
	FinPara
	driver <- driver.quit[]
FinFunción

Función this_date <- get_date_format
	Mientras True Hacer
		Escribir '\nDame fecha del vuelo en formato'
		this_date <- date.fromisoformat[input['YYYY-MM-DD: ')]
		Si today>this_date Entonces
			Escribir 'Ese día ya paso, ingrese uno por venir'
			// continue
		FinSi
		// break
	FinMientras
FinFunción

Función place <- check_place (message,exclude_place)
	Mientras True Hacer
		Leer place
		Si place_not_in__places_in_mexico Entonces
			Escribir 'Codigo de lugar no disponible'
			// continue
		FinSi
		Si place==exclude_place Entonces
			Escribir 'Destino no puede ser igual a partida'
			// continue
		FinSi
		// break
	FinMientras
FinFunción

Función loading_program
	Escribir 'Cargando programa...'
	// time.sleep(2)
FinFunción

Algoritmo main
	// from datetime import date
	// import time
	// import sys
	// from selenium import webdriver
	// from selenium.webdriver.common.by import By
	// from selenium.common.exceptions import TimeoutException
	// from selenium.common.exceptions import WebDriverException
	// from selenium.webdriver.support.ui import WebDriverWait
	// from selenium.webdriver.support import expected_conditions as EC
	Leer nickname
	Escribir 'Bienvenido', nickname
	loading_program()
	places_in_mexico <- ('code','place')
	Escribir ''
	Para code_name<-places_in_mexico.items[] Hasta 0 Con Paso . Hacer
		Escribir code, ':', name
	FinPara
	Escribir ''
	Escribir 'Escribe el lugar de forma abreviada (ej. MTY)'
	departure <- check_place('\nDame punto de partida: ')
	destination <- check_place('\nDame tu destino: ',exclude_place=departure)
	today <- date.today[]
	flight_date <- get_date_format()
	options <- webdriver.ChromeOptions[]
	options <- options.add_argument['--disable-blink-features=AutomationControlled')
	flights <- viva_flights()
	user_options <- '********************************\n'
	user_options <- user_options+'Archivo creado el {today} por {nickname}\n'
	user_options <- user_options+'con punto de partida: {departure}\n'
	user_options <- user_options+'con lugar de destino: {destination}\n'
	user_options <- user_options+'con fecha de vuelo: {flight_date}\n'
	user_options <- user_options+'********************************\n\n'
	current_time <- time.strftime['%Y%m%d%H%M')
	Escribir user_options>'viva-{current_time}.txt'
	Escribir flights>'viva-{current_time}.txt'
	Escribir 'Tu archivo esta listo: viva-{current_time}.txt'
FinAlgoritmo
