from datetime import date
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Función que genera un mensaje de espera
def loading_program():
    print("Cargando programa...")
    time.sleep(2)


# Solicita al usuario su nombre o nickname
nickname = input("Dame nombre de usuario: ")

# Mensaje de bienvenida con nombre o nickname
print(f"Bienvenido {nickname}\n")

# Funciones de inicio
loading_program()


# Códigos de lugares en México
places_in_mexico = {
    "ACA": "acapulco",
    "BJX": "león, el bajío",
    "CEN": "ciudad obregón",
    "CJS": "ciudad juárez",
    "CTM": "chetumal",
    "CUL": "culiacán",
    "CUN": "cancun",
    "CUU": "chihuahua",
    "CZM": "cozumel",
    "GDL": "guadalajara",
    "HMO": "hermosillo",
    "HUX": "huatulco",
    "LAP": "la paz",
    "LMM": "los mochis",
    "MEX": "ciudad de méxico",
    "MID": "mérida",
    "MLM": "morelia",
    "MTY": "monterrey",
    "MXL": "mexicalli",
    "MZT": "mazatlán",
    "NLD": "nuevo laredo",
    "NLU": "felipe ángeles",
    "OAX": "oaxaca",
    "PBC": "puebla",
    "PVR": "puerto vallarta",
    "PXM": "puerto escondido",
    "QRO": "querétaro",
    "REX": "reynosa",
    "SDJ": "san josé del cabo/los cabos",
    "TAM": "tampico",
    "TGZ": "tuxtia gutiérrez",
    "TIJ": "tijuana",
    "TLC": "toluca",
    "TQO": "tulum",
    "TRC": "torreón",
    "VER": "veracruz",
    "VSA": "villahermosa",
    "ZIH": "ixtapa/zihuatanejo",
}

# Imprimir dichos códigos
print()
for code, name in places_in_mexico.items():
    print(f"{code} : {name}")
print()


# Comprueba que el lugar dado este en la lista
# y que no se repita con el de partida
def check_place(message, exclude_place=""):
    while True:
        place = input(message).upper()

        if place not in places_in_mexico:
            print("Codigo de lugar no disponible")
            continue
        if place == exclude_place:
            print("Destino no puede ser igual a partida")
            continue
        break
    return place


# Pedir partida y destino del vuelo
print("Escribe el lugar de forma abreviada (ej. MTY)")
departure = check_place("\nDame punto de partida: ")
destination = check_place("\nDame tu destino: ", exclude_place=departure)


# Conseguir día de hoy
today = date.today()


# Recibir fecha en formato requerido
def get_date_format():
    while True:
        try:
            print("\nDame fecha del vuelo en formato")
            this_date = date.fromisoformat(input("YYYY-MM-DD: "))

            # Checar que día no sea menor a hoy
            if today > this_date:
                print("Ese día ya paso, ingrese uno por venir")
                continue
            break
        # Si formato es incorrecto, cachar error y repetir hasta que sea correcto
        except ValueError:
            print("Formato de fecha incorrecto")
    print()
    return this_date


# Pedir fecha del vuelo
flight_date = get_date_format()


# Dar formato al texto para su salida a archivo
def format_flights(flight: dict):
    # Iniciar variable para guardar vuelos con formato
    formatted_text = ""

    # Llenar los vuelos con salida
    formatted_text += f'Salida: {flight.get("day")} a las {flight.get("start")} en {flight.get("departure")}\n'

    # Llenar los vuelos con llegada
    if not flight.get("is_other_day"):
        formatted_text += (
            f'Llegada: {flight.get("end")} en {flight.get("destination")}\n'
        )
    else:
        formatted_text += f'Llegada: ({flight.get("is_other_day")[0].text}) {flight.get("end")} en {flight.get("destination")}\n'

    # Llenar los vuelos con tipo
    if not flight.get("is_connection"):
        formatted_text += f'Tipo de vuelo: {flight.get("type")}\n'
    else:
        formatted_text += f'Tipo de vuelo: {flight.get("type")} ({flight.get("is_connection")[0].text})\n'

    # Llenar los vuelos con timepo
    formatted_text += f'Duración: {flight.get("time")}\n'

    # Llenar los vuelos con precio
    formatted_text += f'Precio: ${flight.get("price")}\n\n'

    # Retornar la información de los vuelos con formato
    return formatted_text


# Definir parametros con los que Chrome inicie
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")


def viva_flights():
    # Definir formato de la url
    flight_date_format = str(flight_date).replace("-", "")
    url = f"https://www.vivaaerobus.com/es-mx/book/options?itineraryCode={departure}_{destination}_{flight_date_format}&passengers=A1"

    # Iniciar instancia del explorador Chrome
    driver = webdriver.Chrome(options=options)

    try:
        # Llamar a Chrome con url
        driver.get(url)
        # Maximizar ventana
        driver.maximize_window()
    except WebDriverException:
        print("Error ocurred with browser")
        driver.quit()
        # Terminar ejecución de programa
        sys.exit()

    # Aqui guardar la información de los vuelos
    flight = {}
    flight_formatted = ""

    try:
        # Dar tiempo para que la página cargue
        # Por medio de la busqueda del día
        flight["day"] = (
            WebDriverWait(driver, 30)
            .until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//app-carousel-item//div[contains(@class,'selected')]//p[contains(@class,'item-content-date')]",
                    )
                )
            )
            .text
        )
    except TimeoutException:
        print("Viva Aerobus was not loaded correctly")
        # Close Chrome instance
        driver.quit()
        # Terminar ejecución de programa
        sys.exit()

    # Dar tiempo para que el botón cargue
    time.sleep(2.5)

    try:
        # Encontrar el botón "Ver todos los vuelos"
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//app-flight-options-container//button[starts-with(@class,'viva-btn tertiary')]",
                )
            )
        )
    # Y añadir excepción por si el botón no esta disponible
    except TimeoutException:
        button = False

    # Y hacer click si se encuentra el botón y se puede hacer click
    if button:
        # Scroll hasta el botón
        driver.execute_script("arguments[0].scrollIntoView(true);", button)

        ## Dar tiempo para que el scroll cargue
        time.sleep(2.5)

        # Hacer click en el botón "Ver todos los vuelos"
        driver.execute_script("arguments[0].click();", button)

        # Dar tiempo para que la página cargue
        time.sleep(5)

    # Encontrar los vuelos disponibles
    flight_options = driver.find_elements(
        By.XPATH,
        "//app-flight-options-container//app-flight-option",
    )

    # Por cada vuelo encontrado
    for flight_option in flight_options:
        # Conseguir precio del vuelo
        flight["price"] = flight_option.find_elements(
            By.XPATH,
            ".//app-price[contains(@class,'d-lg-block')]//span[contains(@class,'default-price')]",
        )
        # Si el precio no aparece significa que el vuelo esta lleno
        # En ese caso, ir al siguiente vuelo
        if not flight.get("price"):
            continue

        # Sacar el texto del vuelo
        flight["price"] = flight.get("price")[0].text

        # Conseguir cuando empieza del vuelo
        flight["start"] = flight_option.find_element(
            By.XPATH,
            ".//div[@class='d-flex flex-row justify-content-start']//*[@class='mx-0 my-0']",
        ).text

        # Conseguir donde empieza del vuelo
        flight["departure"] = flight_option.find_element(
            By.XPATH,
            ".//div[@class='d-flex flex-row justify-content-start']//div[@class='small-title station-title text-left d-flex']/span[not(contains(@class,'annotation-anchor'))]",
        ).text

        # Conseguir cuando termina del vuelo
        flight["end"] = flight_option.find_element(
            By.XPATH,
            ".//div[@class='d-flex flex-row justify-content-end']//*[@class='mx-0 my-0']",
        ).text

        # Conseguir donde termina del vuelo
        flight["destination"] = flight_option.find_element(
            By.XPATH,
            ".//div[@class='d-flex flex-row justify-content-end']//div[contains(@class,'justify-content-end')]/span[not(contains(@class,'annotation-anchor'))]",
        ).text

        # Conseguir duración del vuelo
        flight["time"] = flight_option.find_element(
            By.XPATH,
            ".//div[contains(@class,'flight-option-button')]/div/span",
        ).text

        # Conseguir tipo del vuelo
        flight["type"] = flight_option.find_element(
            By.XPATH,
            ".//app-flight-option-travel-type//span[contains(@class,'medium-title')]",
        ).text

        # Conseguir si el vuelo termina el día siguiente
        flight["is_other_day"] = flight_option.find_elements(
            By.XPATH,
            ".//div[@class='d-flex flex-row justify-content-end']//div[contains(@class,'justify-content-end')]/span[contains(@class,'d-lg-inline')]//span[contains(@class,'annotation-text')]",
        )

        # Conseguir si el vuelo es de conexión
        flight["is_connection"] = flight_option.find_elements(
            By.XPATH,
            ".//app-flight-brief-graph//div[contains(@class,'text-nowrap ng-star-inserted')]",
        )

        # Mandar información recibida a funcion para dar formato al texto
        flight_formatted += format_flights(flight)

    # Terminar instancia de Chrome
    driver.quit()

    # Retornar toda la información relevante de los vuelos
    return flight_formatted


# Crear variable para almacenar los vuelos de Viva Aerobus
flights = viva_flights()


# Reescribir today con hora y minuto
today = time.strftime("%Y-%m-%d %H:%M")

# Llenar archivo con información dada por el usuario
user_options = "********************************\n"
user_options += f"Archivo creado por '{nickname}' [{today}]\n"
user_options += f"con punto de partida: {departure}\n"
user_options += f"con lugar de destino: {destination}\n"
user_options += f"con fecha de vuelo: {flight_date}\n"
user_options += "********************************\n\n"


# Guardar formato para tiempo actual
current_time = time.strftime("%Y%m%d%H%M")

# Llenar archivo de texto con todos los vuelos
with open(f"viva-{current_time}.txt", "w") as f:
    f.write(user_options)
    f.write(flights)

# Imprimir mensaje con nombre de archivo
print(f"Tu archivo esta listo: viva-{current_time}.txt")
