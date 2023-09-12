Función this_flight <- format_flights (flight_day,hour_start,place_start,hour_end,place_end,flight_type,flight_time,flight_price,ends_other_day,is_connection)
	this_flight <- ''
	this_flight <- this_flight+'Salida: {flight_day} a las {hour_start} en {place_start}\n'
	Si !ends_other_day Entonces
		this_flight <- this_flight+'Llegada: {hour_end} en {place_end}\n'
	SiNo
		this_flight <- this_flight+'Llegada: ({ends_other_day[0].text}) {hour_end} en {place_end}\n'
	FinSi
	Si !is_connection Entonces
		this_flight <- this_flight+'Tipo de vuelo: {flight_type}\n'
	SiNo
		this_flight <- this_flight+'Tipo de vuelo: {flight_type} ({is_connection[0].text})\n'
	FinSi
	this_flight <- this_flight+'Duración: {flight_time}\n'
	this_flight <- this_flight+'Precio: ${flight_price}\n\n'
FinFunción

Función current_flights <- viva_flights
	flight_date_format <- flight_date.replace['-','']
	url <- 'https://www.vivaaerobus.com/es-mx/book/options?itineraryCode={departure}_{destination}_{flight_date_format}&passengers=A1'
	driver <- webdriver.Chrome[options=options]
	driver <- driver.get[url]
	driver <- driver.maximize_window[]
	// time.sleep(15)
	button <- driver.find_elements[By.XPATH,'button')
	Si button Entonces
		button <- button.click[]
	FinSi
	// time.sleep(5)
	flight_day <- driver.find_element[By.XPATH,'//day')
	flight_options <- driver.find_elements[By.XPATH,'//app-flight-option')
	current_flights <- ''
	Para flight<-flight_options Hasta . Hacer
		flight_price <- flight.find_elements[By.XPATH,'.//default-price')
		Si !flight_price Entonces
			// continue
		SiNo
			flight_price <- flight_price.text
		FinSi
		hour_start <- flight.find_element[By.XPATH,'.//hour_start')
		place_start <- flight.find_element[By.XPATH,'.//place_start')
		hour_end <- flight.find_element[By.XPATH,'.//hour_end')
		place_end <- flight.find_element[By.XPATH,'.//place_end')
		flight_time <- flight.find_element[By.XPATH,'.//flight_time')
		flight_type <- flight.find_element[By.XPATH,'.//flight_type')
		ends_other_day <- flight.find_elements[By.XPATH,'.//ends_other_day')
		is_connection <- flight.find_elements[By.XPATH,'.//is_connection')
		current_flights <- current_flights+format_flights(flight_day,hour_start,place_start,hour_end,place_end,flight_type,flight_time,flight_price,ends_other_day,is_connection)
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
	// from selenium import webdriver
	// from selenium.webdriver.common.by import By
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
	flights <- ''
	flights <- flights+viva_flights()
	user_options <- '********************************\n'
	user_options <- user_options+'Archivo creado el {today} por {nickname}\n'
	user_options <- user_options+'con punto de partida: {departure}\n'
	user_options <- user_options+'con lugar de destino: {destination}\n'
	user_options <- user_options+'con fecha de vuelo: {flight_date}\n'
	user_options <- user_options+'********************************\n\n'
	current_time <- time.strftime['%Y%m%d%H%M')
	Escribir user_options>'viva-{current_time}.txt'
	Escribir flights>'viva-{current_time}.txt'
	Escribir "Tu archivo esta listo: viva-{current_time}.txt"
FinAlgoritmo
