from django.shortcuts import render
import urllib.request
import json
from django.http import HttpResponse
from http import HTTPStatus
from urllib.error import HTTPError
from django.shortcuts import render, redirect
import requests
import urllib3

#llamado de vistas
def home(request):
    return(request,'pokemonList.html')

def index(request):
   
    return render(request, "main/index.html")

def pokemonList(request):
   
    return render(request, "main/pokemonList.html")

def weightPokemon(request):
   
    return render(request, "main/weightPokemon.html")

def typeFly(request):
   
    return render(request, "main/typeFly.html")

def pokemonReverse(request):
   
    return render(request, "main/pokemonReverse.html")

#Variable api_url de PokémonApi
"""
Variable creada para llamar a la api de PokémonApi y ser guardada en un espacio en memoria.
Utilizando el urllib3.PoolManager() utiliza un motor mucho mas rapido para leer la informacion que se trae en la api
antes de convertirlo a Json, esta funcion se utiliza para obtener el contenido de la respuesta en formato de cadena.
"""
api_url = 'https://pokeapi.co/api/v2/pokemon/'
http = urllib3.PoolManager()
# Función para obtener datos de Pokémon desde la API
"""
En esta función se trae los datos completos de la variable api_url de PokémonApi,
donde su informacion se extrae en formato Jason. 
La misma puede ser llamada a diferentes funciones que la soliciten.
"""
def getPokeApi(identifier):
    try:
        url = f'{api_url}{identifier}'
        response = http.request('GET', url, headers={'User-Agent': 'pikachu'})
        return json.loads(response.data.decode('utf-8'))
    
    except urllib3.exceptions.HTTPError as e:
        if e.status == 404:
            return None
        

# Función para convertir altura y peso de Pokémon
"""
Función para convertir los datos traidos desde un diccionario, 
en decimales a metros, en el caso de altura. En el caso de peso, lo convierte a Kilogramos
"""
def convertHeightWeight(data):
    height_obt = round(float(data['height']) * 0.1, 2)
    weight_obt = round(float(data['weight']) * 0.1, 2)
    return  height_obt, weight_obt


# Función para procesar los datos de Pokémon
"""
Función para Procesar los datos solicitados en el enunciado, y mostrarlos en la vista.
Permite tomar como parametro el identificador que estamos llamando.
"""
def pokemonData(identifier):
    try:
        data = getPokeApi(identifier)

        if data:
            height, weight = convertHeightWeight(data)
            return {
                "number": str(data.get('id', '')),
                "name": str(data.get('name', '')).capitalize(),
                "type": ', '.join([t['type']['name'] for t in data.get('types', [])]),
                "height": f"{height}M",
                "weight": f"{weight}KG",
                "sprite": str(data.get('sprites', {}).get('front_default', '')),
            }
        else:
            data = {'Pokemon no encontrado'}
    except HTTPError as e:
        if e.code == 404:
            return render('main/error.html', status=404) 
        else:
            raise










#Función para mostrar la tarjeta con el pokémon!
# Al utilizar el .lower, me aseguro de que el usuario pueda ingresar mayúsculas y minúsculas, sin devolver errores
# también aseguro que no le permita colocar espacios para evitar errores
def index(request):
   
    data = {}
    
    if request.method == 'POST':

        
        pokemon_input = request.POST.get('pokemon', '').lower().replace(' ', '%20')

        try:
            if pokemon_input:
              
                data = pokemonData(pokemon_input)
            else:
                
                data = {'error_message': 'Por favor, ingrese un número de Pokémon o un nombre para buscar.'}
                
        except HTTPError as e:
            if e.code == 404:
                return render(request, 'main/error.html')

    return render(request, 'main/index.html', data)



#Método para mostrar la Lista de los pokemones, del 1 al 50
"""
Función para permitir una libreria con los primeros 50 Pokémon de la api, que llamamos desde
otras funciones. Se utiliza un bucle for para que recorra la lista y nos muestre en la vista cada tarjeta
con sus respectivos valores.

Se llaman los metodos de conversión de valores, y la solicitud de datos en la función pokemonData()
"""
def pokemonList(request):
    data = {}
    pokemon_list = []

    
    for pokemon_number in range(1, 51):
        pokemon_data = pokemonData(pokemon_number)

        if pokemon_data:
            pokemon_list.append(pokemon_data)
        else:
            return render(request, 'main/error.html' )

    data['pokemon_list'] = pokemon_list
    return render(request, 'main/pokemonList.html', data)




#Función para filtrar pokemones por peso
"""
En esta funcion, solicito por parametro el dato para poder traer datos de la api 
y poder filtrar los pokemones del peso solicitado, mas de 30 y menor de 80.
en el condicional if, se solicita 3 < peso < 8, porque ya la conversion me la hace en la función de convert.

"""
def weightPokemon(request):
    data = {}
    pokemon_list = []

    # Obtener detalles de los primeros 50 Pokémon
    for pokemon_number in range(1, 51):
        try:
            list_of_data = getPokeApi(pokemon_number)

            if list_of_data:
                height, weight = convertHeightWeight(list_of_data)

                if 3 < weight < 8:
                    pokemon_data = {
                        "number": str(list_of_data.get('id', '')),
                        "name": str(list_of_data.get('name', '')).capitalize(),
                        "type": ', '.join([t['type']['name'] for t in list_of_data.get('types', [])]),
                        "height": f"{height}M",
                        "weight": f"{weight}KG",
                        "sprite": str(list_of_data.get('sprites', {}).get('front_default', '')),
                    }

                    pokemon_list.append(pokemon_data)
        except HTTPError as e:
            if e.code == 404:
                return render(request, 'main/error.html')

    data['filterPokemonByWeight'] = pokemon_list
    return render(request, 'main/weightPokemon.html', data)




#Función para filtrar por tipo Grass
"""
Función para poder filtar los Pokémon tipo Grass. Lo cual llamo al metodo para traer los datos convertidos
y luego solicito que si hay tipo Grass en la lista de 50 primeros, me devuelva los siguientes valores y me los 
muestre en pantalla.
"""
def typeGrass(request, pokemon_type):
    data = {'filtered_pokemon_list': []}

    # Obtener detalles de los primeros 50 Pokémon
    for pokemon_number in range(1, 51):
        try:
            list_data = getPokeApi(pokemon_number)

            if list_data and 'types' in list_data:
                types = [t['type']['name'] for t in list_data.get('types', [])]
                
                if 'grass' in types:
                    height, weight = convertHeightWeight(list_data)
                    pokemon_data = {
                        "number": str(list_data.get('id', '')),
                        "name": str(list_data.get('name', '')).capitalize(),
                        "type": ', '.join(types),
                        "height": f"{height}M",
                        "weight": f"{weight}KG",
                        "sprite": str(list_data.get('sprites', {}).get('front_default', '')),
                    }
                    
                    data['filtered_pokemon_list'].append(pokemon_data)
        except requests.RequestException as e:
            if isinstance(e, requests.HTTPError) and e.response.status_code == 404:
                return render(request, 'main/error.html')
            else:
                raise

    return render(request, 'main/typeGrass.html', data)



#Funcion para filtrar por tipo vuelo y mas de 10 
"""
Funcion para obtener los pokemones de tipo Flying y que sean mayor a 10,
dentro de los primeros 50 de la lista.
en la funcion aparece si son > 1, porque el 10 lo utilizo antes para convertirlo a altura.
En la funcion se recorre la lista y encuentra los mayores a 10, luego los convierte.
Esta funcion tambien es usada por el parametro request, donde obtenemos la solicitud.
Al obtener todos los datos, es renderizado a la vista correspondiente
"""
def typeFly(request):
    data = {'fly_pokemon_10': []}

    # Obtener detalles de los primeros 50 Pokémon
    for pokemon_number in range(1, 51):
        try:
            list_of_data = getPokeApi(pokemon_number)

            if list_of_data and 'types' in list_of_data:
                types = [t['type']['name'] for t in list_of_data.get('types', [])]
                height = float(list_of_data.get('height', 0)) * 0.1

                if 'flying' in types and height > 1:
                    height_obt, weight_obt = convertHeightWeight(list_of_data)
                    weight_redond = round(weight_obt, 2)

                    pokemon_data = {
                        "number": str(list_of_data.get('id', '')),
                        "name": str(list_of_data.get('name', '')).capitalize(),
                        "type": ', '.join(types),
                        "height": f"{round(height_obt, 2)}M",
                        "weight": f"{weight_redond}KG",
                        "sprite": str(list_of_data.get('sprites', {}).get('front_default', '')),
                    }

                    data['fly_pokemon_10'].append(pokemon_data)
        except requests.RequestException as e:
            if isinstance(e, requests.HTTPError) and e.response.status_code == 404:
                return render(request, 'main/error.html')
            else:
                raise

    print('fly_pokemon_10:', data['fly_pokemon_10'])
    return render(request, 'main/typeFly.html', data)

#Función para mostrar los Pokémon con sus respectivos nombres de derecha a izquierda
"""
Esta función me permite buscar los primeros 50 Pokémon y procesar en reversa sus respectivos nombres.
En el parametro obtengo la url de la api.

Solo es utilizado en el name.
"""
def reverse(api_url):
    pokemon_list = []

    for pokemon_number in range(1,51):
        try:
           
           pokeapi = getPokeApi(pokemon_number)

           if pokeapi:
           

            pokeid = pokeapi.get('id', 0)
            pokename = pokeapi.get('name','')
            pokeimage = pokeapi.get('sprites', {}).get('front_default', '')
            poketype = ', '.join([t['type']['name'] for t in pokeapi.get('types', [])])
            pokeheight, pokeweight = convertHeightWeight(pokeapi)


            invert_name = pokename[::-1]

            pokemon_list.append({'name':invert_name, 
                                 'sprite': pokeimage,
                                 'type': poketype,
                                 'height': pokeheight,
                                 'weight': pokeweight,
                                 'number': pokeid
                                 
                                 })
          
        except HTTPError as e:
            print(f'Error al obtener los datos del nombre del Pokémon')
    return pokemon_list

"""
En esta función llamo a la función anterior (reverse), la cual me ejecuta lo que solicito.
Su resultado me renderiza a la vista de la pagina correspondiente, 
mostrando sus nombres en relacion inversa.
"""
def pokemonReverse(request):

    inv = reverse(api_url)

    return render(request, 'main/pokemonReverse.html', {
        'inv': inv
    })


