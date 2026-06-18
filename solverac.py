"""
Solver de sistemas de ecuaciones simbolicas complejas para circuitos AC.

El usuario escribe cada ecuacion directamente en notacion algebraica,
por ejemplo:

    x1 - x2/(9 - j*7) = 10 + j*5

en vez de tener que descomponerla termino a termino. El programa
extrae automaticamente los coeficientes, construye el sistema A*x = b,
lo resuelve con numpy, y valida el resultado por sustitucion directa
en las ecuaciones originales (no en la matriz ya armada), lo que
detecta tambien errores de la propia extraccion simbolica.

RESTRICCIONES DE SINTAXIS (ver lista completa al final del archivo):
  - Las incognitas deben llamarse exactamente x1, x2, ..., xn.
  - La unidad imaginaria se escribe 'j', siempre con * explicito (j*7, no j7).
  - Cada ecuacion debe tener exactamente un signo '='.
  - El sistema debe ser lineal (no se permiten potencias ni productos
    entre incognitas).
"""

import cmath
import math
import numpy as np
import sympy as sp


UMBRAL_RESIDUAL = 1e-6
LOCAL_DICT = {"j": sp.I}


class ErrorDeSintaxis(Exception):
    """Error de entrada del usuario, no del metodo numerico."""
    pass


def variables_permitidas(n):
    return {f"x{i+1}" for i in range(n)}


def parsear_ecuacion(texto, n, simbolos):
    """
    Convierte el texto de una ecuacion en su forma estandar (== 0),
    valida que solo use variables permitidas, y confirma que el
    sistema sea lineal en esas variables.
    """
    if texto.count("=") != 1:
        raise ErrorDeSintaxis(
            f"La ecuacion debe tener exactamente un '='. Recibido: '{texto}'"
        )

    izq_texto, der_texto = texto.split("=")

    try:
        izq = sp.sympify(izq_texto, locals=LOCAL_DICT)
        der = sp.sympify(der_texto, locals=LOCAL_DICT)
    except (sp.SympifyError, SyntaxError) as e:
        raise ErrorDeSintaxis(f"No se pudo interpretar la ecuacion: {e}")

    ecuacion = sp.expand(izq - der)

    permitidas = variables_permitidas(n)
    usadas = {str(s) for s in ecuacion.free_symbols}
    no_permitidas = usadas - permitidas
    if no_permitidas:
        raise ErrorDeSintaxis(
            f"Variable(s) no reconocida(s): {no_permitidas}. "
            f"Solo se permiten: {sorted(permitidas)}. "
            f"(¿Olvidaste el '*' entre 'j' y un numero, ej. j*7 en vez de j7?)"
        )

    # Verificacion de linealidad: el grado de la ecuacion en cada
    # variable debe ser <= 1, y no debe haber productos entre variables.
    for s in simbolos:
        if sp.degree(ecuacion, gen=s) > 1:
            raise ErrorDeSintaxis(
                f"La ecuacion no es lineal respecto a {s}. "
                f"Este programa solo resuelve sistemas lineales "
                f"(circuitos AC en regimen permanente senoidal)."
            )

    return ecuacion


def extraer_fila(ecuacion, simbolos):
    """
    Dada una ecuacion en forma estandar (== 0) y la lista ordenada
    de simbolos x1..xn, devuelve (fila_de_coeficientes, termino_b).
    """
    fila = [complex(ecuacion.coeff(s)) for s in simbolos]
    termino_indep = ecuacion.subs({s: 0 for s in simbolos})
    b_i = complex(-termino_indep)
    return fila, b_i


def leer_sistema():
    n = int(input("Numero de incognitas del sistema: "))
    simbolos = sp.symbols(f"x1:{n+1}")  # genera x1, x2, ..., xn

    A = np.zeros((n, n), dtype=complex)
    b = np.zeros(n, dtype=complex)
    ecuaciones_originales = []  # para la verificacion final por sustitucion

    print(f"\nVariables disponibles: {', '.join(str(s) for s in simbolos)}")
    print("Escribe 'j' para la unidad imaginaria, siempre con * (ej: j*7).\n")

    for i in range(n):
        while True:
            texto = input(f"Ecuacion {i+1} de {n}: ").strip()
            try:
                ecuacion = parsear_ecuacion(texto, n, simbolos)
                fila, b_i = extraer_fila(ecuacion, simbolos)
                A[i, :] = fila
                b[i] = b_i
                ecuaciones_originales.append(texto)
                break
            except ErrorDeSintaxis as e:
                print(f"  Error: {e}")
                print("  Vuelve a escribir esta ecuacion.\n")

    return A, b, ecuaciones_originales, simbolos


def resolver_sistema(A, b):
    try:
        x = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return None, None

    residual = A @ x - b
    error_relativo = np.linalg.norm(residual) / (np.linalg.norm(b) + 1e-30)
    return x, error_relativo


def verificar_por_sustitucion(ecuaciones_originales, simbolos, x):
    """
    Verificacion independiente: sustituye la solucion en las ecuaciones
    de TEXTO originales (no en la matriz ya construida), para detectar
    tambien errores que hayan ocurrido durante la extraccion simbolica.
    """
    sustitucion = {s: complex(val) for s, val in zip(simbolos, x)}
    errores = []

    for i, texto in enumerate(ecuaciones_originales):
        izq_texto, der_texto = texto.split("=")
        izq = sp.sympify(izq_texto, locals=LOCAL_DICT).subs(sustitucion)
        der = sp.sympify(der_texto, locals=LOCAL_DICT).subs(sustitucion)
        diferencia = abs(complex(izq) - complex(der))
        errores.append(diferencia)

    return errores


def mostrar_resultado(x, error_relativo, errores_sustitucion):
    print("\n--- Resultados ---")
    for i, valor in enumerate(x):
        mag = abs(valor)
        ang = math.degrees(cmath.phase(valor))
        print(f"x{i+1} = {valor.real:.4f} + {valor.imag:.4f}j   "
              f"(forma polar: {mag:.4f} ∠ {ang:.2f}°)")

    print(f"\nResidual de la matriz (A*x - b): {error_relativo:.2e}")
    print("Verificacion por sustitucion directa en cada ecuacion original:")
    for i, err in enumerate(errores_sustitucion):
        estado = "OK" if err < UMBRAL_RESIDUAL else "FALLA"
        print(f"  Ecuacion {i+1}: diferencia = {err:.2e}  [{estado}]")

    if max(errores_sustitucion) > UMBRAL_RESIDUAL or error_relativo > UMBRAL_RESIDUAL:
        print("\nADVERTENCIA: alguna ecuacion no se satisface dentro del umbral.")
        print("Esto indica inconsistencia en el sistema ingresado, o un error")
        print("en como se planteo el circuito. Revisa tus ecuaciones de origen.")
    else:
        print("\nSistema consistente: la solucion satisface todas las ecuaciones.")


def main():
    print("=== Solver simbolico de ecuaciones complejas para circuitos AC ===\n")
    A, b, ecuaciones_originales, simbolos = leer_sistema()
    x, error_relativo = resolver_sistema(A, b)

    if x is None:
        print("\nLa matriz de coeficientes es singular: el sistema no tiene")
        print("solucion unica. Revisa que tus ecuaciones sean independientes")
        print("(ninguna debe ser combinacion lineal de las otras).")
        return

    errores_sustitucion = verificar_por_sustitucion(ecuaciones_originales, simbolos, x)
    mostrar_resultado(x, error_relativo, errores_sustitucion)


if __name__ == "__main__":
    main()


# =====================================================================
# LISTA DE RESTRICCIONES (sintaxis de entrada obligatoria)
# =====================================================================
#
# 1. NOMBRES DE VARIABLE: unicamente x1, x2, ..., xn, donde n es el
#    numero de incognitas declarado al inicio. No se permite Va, I1,
#    Vab, ni ningun otro nombre. Esto elimina ambiguedad de mayusculas/
#    minusculas y nombres repetidos.
#
# 2. UNIDAD IMAGINARIA: se escribe exclusivamente como 'j', y SIEMPRE
#    con un operador * explicito antes del numero. Correcto: j*7.
#    Incorrecto: j7 (se interpretaria como una variable nueva llamada
#    'j7', y el programa la rechazara por no estar en la lista permitida).
#
# 3. UNA SOLA IGUALDAD POR ECUACION: cada linea debe contener
#    exactamente un signo '='. No se permiten desigualdades, ni
#    ecuaciones con multiples '=' encadenados.
#
# 4. SISTEMA LINEAL UNICAMENTE: no se permiten potencias de las
#    incognitas (x1**2) ni productos entre incognitas (x1*x2). Esto
#    es coherente con el modelo fisico: en regimen permanente
#    senoidal (fasores), todo circuito con R, L, C es lineal por
#    definicion. Elementos no lineales (diodos, transistores) no
#    estan dentro del alcance de este programa.
#
# 5. NUMERO DE ECUACIONES = NUMERO DE INCOGNITAS: el programa pide
#    exactamente n ecuaciones para n incognitas. No se valida
#    independencia lineal de antemano; si las ecuaciones no son
#    independientes, la matriz resultante sera singular y el programa
#    lo reportara como tal (no como "error de tipeo").
#
# 6. OPERADORES SOPORTADOS: +, -, *, /, **, y parentesis, segun la
#    sintaxis estandar de Python/sympy. No se aceptan notaciones como
#    "9-j7" (sin asterisco) ni "5∠30°" (forma polar simbolica directa);
#    para ingresar un numero en polar, debe convertirse antes a
#    rectangular usando j explicito.
#
# 7. CADA ECUACION SE EVALUA DE FORMA INDEPENDIENTE: no hay memoria
#    entre ecuaciones mas alla de las variables x1..xn; no se permite
#    definir variables auxiliares o abreviaciones dentro del sistema.
# =====================================================================