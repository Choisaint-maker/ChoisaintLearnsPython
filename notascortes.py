def menu():
    print('=' * 45)
    print(' PROGRAMA DE NOTAS DE CORTES')
    print('=' * 45)
    print('1. Calcular acumulado a primer corte')
    print('2. Calcular acumulado a segundo corte')
    print('3. Calcular totales y estado final')
    print('4. Calcular nota necesaria en el tercer corte')
    seleccion = int(input('Seleccione una opcion: '))
    return seleccion


def pedir_nota(etiqueta):
    return float(input(f'Nota del {etiqueta}: '))


def acumulado(a, b, c):
    acm1 = a * 0.3
    acm2 = b * 0.3
    acm3 = c * 0.4
    return acm1, acm2, acm3

def notafinal(corte1, corte2, corte3):
    return (corte1 * 0.3) + (corte2 * 0.3) + (corte3 * 0.4)


def mensaje(nota_final):
    return 'APROBADO' if nota_final >= 3.0 else 'REPROBADO'


def nota_necesaria(corte1, corte2, meta=3.0):
    # Despeje algebraico: corte3 = (meta - corte1*0.3 - corte2*0.3) / 0.4
    corte3 = (meta - corte1 * 0.3 - corte2 * 0.3) / 0.4
    return corte3


def mostrar_acumulados(acm1, acm2, acm3):
    print('-' * 45)
    print(f'  Acumulado corte 1: {acm1:.2f}')
    print(f'  Acumulado corte 2: {acm2:.2f}')
    print(f'  Acumulado corte 3: {acm3:.2f}')
    print('-' * 45)


def caso_primer_corte():
    print('\n--- Acumulado a primer corte ---')
    c1 = pedir_nota('corte 1')
    acm1 = c1 * 0.3
    print('-' * 45)
    print(f'  Acumulado corte 1: {acm1:.2f}')
    print(f'  (Aun faltan corte 2 y corte 3 para el total)')
    print('-' * 45)


def caso_segundo_corte():
    print('\n--- Acumulado a segundo corte ---')
    c1 = pedir_nota('corte 1')
    c2 = pedir_nota('corte 2')
    acm1, acm2, _ = acumulado(c1, c2, 0)
    print('-' * 45)
    print(f'  Acumulado corte 1: {acm1:.2f}')
    print(f'  Acumulado corte 2: {acm2:.2f}')
    print(f'  Subtotal parcial:  {acm1 + acm2:.2f}')
    print(f'  (Falta corte 3, peso 0.4, para el total)')
    print('-' * 45)


def caso_final():
    print('\n--- Calculo de estado final ---')
    c1 = pedir_nota('corte 1')
    c2 = pedir_nota('corte 2')
    c3 = pedir_nota('corte 3')

    nf = notafinal(c1, c2, c3)
    acm1, acm2, acm3 = acumulado(c1, c2, c3)

    mostrar_acumulados(acm1, acm2, acm3)
    print(f'  NOTA FINAL: {nf:.2f}')
    print(f'  ESTADO: {mensaje(nf)}')
    print('=' * 45)


def caso_nota_necesaria():
    print('\n--- Nota necesaria en el tercer corte ---')
    c1 = pedir_nota('corte 1')
    c2 = pedir_nota('corte 2')
    meta = float(input('Nota final que desea obtener (ej. 3.0): '))

    requerido = nota_necesaria(c1, c2, meta)
    acm1, acm2, _ = acumulado(c1, c2, 0)

    print('-' * 45)
    print(f'  Acumulado corte 1: {acm1:.2f}')
    print(f'  Acumulado corte 2: {acm2:.2f}')

    if requerido > 5.0:
        print(f'  Nota necesaria en corte 3: {requerido:.2f}')
        print('  RESULTADO: Matematicamente imposible.')
        print('  La escala maxima es 5.0, no se puede alcanzar la meta.')
    elif requerido <= 0:
        print(f'  Nota necesaria en corte 3: {requerido:.2f}')
        print('  RESULTADO: La meta ya esta garantizada (incluso con 0.0).')
    else:
        print(f'  Nota necesaria en corte 3: {requerido:.2f}')
        print(f'  RESULTADO: Es posible alcanzar la meta de {meta:.2f}')
    print('=' * 45)


def main():
    seleccion = menu()

    match seleccion:
        case 1:
            caso_primer_corte()
        case 2:
            caso_segundo_corte()
        case 3:
            caso_final()
        case 4:
            caso_nota_necesaria()
        case _:
            print('Opcion invalida. Seleccione 1, 2, 3 o 4.')
            main()  # Volver a mostrar el menu
        
    


if __name__ == '__main__':
    main()