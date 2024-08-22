# Viva-Scrapper

_Viva-Scrapper_ consta de un programa cuyo objetivo es **extraer información de internet sobre los vuelos en la página oficial de Viva Aerobus** para regresarlá al usuario de manera clara y ordenada dentro de un archivo de texto. Cualquiera puede usar _Viva-Scrapper_ y obtener la facilidad, rapidez y apoyo que esta herramienta busca dar.

Uno de los problemas que surgen al buscar información en internet es la extracción de dicha información, ya que copiar y pegar literalmente lo que aparece en pantalla resulta impráctico, sin mencionar que la información se copia en desorden y se pierde lo que se quería decir. Este programa obtendrá la información importante de los vuelos y le añadirá de vuelta su significado para que no se pierda lo que se transmitía en la pantalla.

Para un buen funcionamiento del programa, se **requerirá** que el usuario conozca e ingrese:

- de donde parte
- a donde quiere ir
- la fecha en la que planea hacerlo

Esto debido a que el programa requiere esa información para poder funcionar.

_Viva-Scrapper_ imprimirá una lista de los lugares que maneja Viva Aerobus para que puedan ser ingresados por el usuario. Para evitar errores, se hará uso de ciclos que le indiquen al usuario cuando ha ingresado un lugar o fecha erróneos o en un formato diferente al esperado, ya que las urls de Viva Aerobus dependen de que la información este bien escrita.

Cuando la información ingresada este correcta, _Viva-Scrapper_ iniciará un con la página de Viva Aerobus abierta, se cargarán todos los vuelos disponibles y el programa comenzará a obtener la información de cada vuelo. _Viva-Scrapper_ también usará condicionales para dejar afuera información que no sea útil, por ejemplo, no se mostrarán vuelos que estén marcados como llenos.

Una vez que se haya obtenido la información de la página de Viva Aerobus, _Viva-Scrapper_ se encargará de descomponer la información obtenida en variables que recibirán cada dato importante del vuelo y se le regresará al usuario la información de manera sencilla pero con lo necesario para que cada vuelo se siga entendiendo haciendo uso de este formato:

```
Salida: {día} a las {hora} en {partida}
Llegada: {hora} en {destino}
Tipo de vuelo: {tipo}
Duración: {duración}
Precio: ${precio}
```

Por último, cuando la información haya sido formateada, se cerrara la ventana de Chrome y el programa guardará lo relevante de los vuelos en un archivo de texto. Este archivo contendrá las opciones que uso el usuario para crearlo, en caso de que deseé revisitarlo tiempo después, y el nombre del archivo estará estructurado usando desde el año hasta el segundo en el que el archivo se creo de tal manera que un archivo no se escriba encima de otro por error.

### ¿Como puedo usarlo?

[USAGE.md](./USAGE.md)
