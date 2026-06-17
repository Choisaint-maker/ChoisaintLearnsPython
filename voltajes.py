print(f'ingrese el valor de voltaje:')
V = float(input('voltaje: '))

if V < 0:
    print(f'el voltaje es negativo')
elif V == 0:
    print(f'el voltaje es cero')
elif V>0 and V<=5:
    print(f'logica baja')
elif V>5 and V<=12:
    print(f'logica alta')
else:
    print(f'fuera de rango')