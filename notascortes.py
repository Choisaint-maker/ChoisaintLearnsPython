

def notascortes():
    print(f'ingrese las notas de los cortes')
    print(f'nota del corte 1: ')
    corte1 = float(input('corte 1: '))
    print(f'nota del corte 2: ')    
    corte2 = float(input('corte 2: '))
    print(f'nota del corte 3: ')
    corte3 = float(input('corte 3: '))
    return corte1, corte2, corte3
corte1, corte2, corte3 = notascortes()

def acumulado(a, b, c):
    acumulado = (a * 0.3) + (b * 0.3) + (c * 0.4)
    acm1 = a * 0.3
    acm2 = b * 0.3
    acm3 = c * 0.4
    return acm1, acm2, acm3

def notafinal(corte1, corte2, corte3):
    nota_final = (corte1 * 0.3) + (corte2 * 0.3) + (corte3 * 0.4)
    return nota_final   

def mensaje(nota_final):
    if nota_final >= 3.0:
        return 'aprobado'
    else:
        return 'reprobado'
    
print(f'el resultado es: {mensaje(notafinal(corte1, corte2, corte3))}')
print(f'la nota final es: {notafinal(corte1, corte2, corte3)}')
print(f'el acumulado por cortes es: {acumulado(corte1, corte2, corte3)}')

