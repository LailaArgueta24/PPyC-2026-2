INITIAL_NUMBER = 33
STOP_NUMBER = 126
BASE = STOP_NUMBER - INITIAL_NUMBER + 1
FIXED_LENGTH = 26


def generate_password(posicion, total_procesos=1):
    """
    Genera cadenas de longitud fija (26) usando ASCII [33..126].

    - posicion: indice del proceso (0 <= posicion < total_procesos).
    - total_procesos: cantidad total de procesos.

    El reparto se hace tomando indices globales i tales que:
    i % total_procesos == posicion
    """
    if total_procesos <= 0:
        raise ValueError("total_procesos debe ser mayor a 0")
    if posicion < 0 or posicion >= total_procesos:
        raise ValueError("posicion debe estar en el rango [0, total_procesos)")

    total_combinaciones = BASE ** FIXED_LENGTH

    # Cada proceso recorre su particion: posicion, posicion + total_procesos, ...
    for indice in range(posicion, total_combinaciones, total_procesos):
        valor = indice
        chars = [INITIAL_NUMBER] * FIXED_LENGTH

        # Conversion a base BASE usando division entera y residuo.
        for i in range(FIXED_LENGTH - 1, -1, -1):
            valor, residuo = divmod(valor, BASE)
            chars[i] = INITIAL_NUMBER + residuo

        yield "".join(map(chr, chars))


if __name__ == "__main__":
    # Ejemplo: proceso 0 de 4, cadenas de tamano fijo 26.
    for symbol in generate_password(posicion=0, total_procesos=4):
        print(symbol)
