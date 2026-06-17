import requests

url = "https://api.nasa.gov/planetary/apod"
parametros = {
    "api_key": "6oR79ncl0eWXAMsJe3iicRBTcC6quyULr0fARUGm",
    "count": 5
}

respuesta = requests.get(url, params=parametros)

print(respuesta.status_code)

if respuesta.status_code == 200:
    datos = respuesta.json()
    for imagen in datos:
        print(imagen.get("title", "sin título"))
        print(imagen.get("url", "sin url"))
        print(imagen.get("explanation", "sin explicación"))
else:
    print(respuesta.text)