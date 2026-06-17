 #conversion de temperaturas
temp = float(input("Ingrese la temperatura en grados Celsius: "))
def temperatura(temp):
    fahrenheit = (temp * 9/5) + 32
    kelvin = temp + 273.15
    return fahrenheit, kelvin
fahrenheit, kelvin = temperatura(temp)
print(f"La temperatura en grados Fahrenheit es: {fahrenheit} °F")
print(f"La temperatura en grados Kelvin es: {kelvin} K")
print(f"La temperatura en grados Celsius es: {temp} °C")