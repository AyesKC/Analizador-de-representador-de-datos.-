"""Lógica pura (sin Django) de conversión numérica y análisis de caracteres."""

from dataclasses import dataclass

VALOR_MAXIMO = 65535
BASES_VALIDAS = (2, 8, 10, 16)
DIGITOS = "0123456789ABCDEF"


class ErrorDeEntrada(ValueError):
    """Error de validación con un mensaje claro para el usuario."""


@dataclass(frozen=True)
class ResultadoNumero:
    decimal: int
    binario: str          # completado al siguiente múltiplo de 8 bits
    octal: str
    hexadecimal: str
    bits_significativos: int
    bytes_necesarios: int


@dataclass(frozen=True)
class FilaCaracter:
    caracter: str
    decimal: int
    unicode: str          # U+XXXX
    hexadecimal: str
    bytes_utf8: str       # p. ej. "C3 B1"


def validar_numero(texto: str, base: int) -> int:
    """Valida el texto en la base dada y devuelve su valor entero."""
    if base not in BASES_VALIDAS:
        raise ErrorDeEntrada("La base seleccionada no es válida. Elija 2, 8, 10 o 16.")

    texto = (texto or "").strip()
    if not texto:
        raise ErrorDeEntrada("Debe ingresar un número.")

    if texto.startswith("-"):
        raise ErrorDeEntrada("No se permiten valores negativos.")

    permitidos = set(DIGITOS[:base])
    invalidos = sorted({c for c in texto.upper() if c not in permitidos})
    if invalidos:
        raise ErrorDeEntrada(
            f"Dígitos inválidos para la base {base}: {', '.join(invalidos)}."
        )

    valor = int(texto, base)
    if not 0 <= valor <= VALOR_MAXIMO:
        raise ErrorDeEntrada(
            f"El valor {valor} está fuera del rango permitido (0 a {VALOR_MAXIMO})."
        )
    return valor


def bits_significativos(valor: int) -> int:
    return max(valor.bit_length(), 1)  # el 0 necesita 1 bit


def bytes_necesarios(valor: int) -> int:
    return (bits_significativos(valor) + 7) // 8


def binario_completado(valor: int) -> str:
    """Binario rellenado a múltiplo de 8 bits (8, 16, 24, ...)."""
    ancho = bytes_necesarios(valor) * 8
    return format(valor, f"0{ancho}b")


def convertir_numero(texto: str, base: int) -> ResultadoNumero:
    valor = validar_numero(texto, base)
    return ResultadoNumero(
        decimal=valor,
        binario=binario_completado(valor),
        octal=format(valor, "o"),
        hexadecimal=format(valor, "X"),
        bits_significativos=bits_significativos(valor),
        bytes_necesarios=bytes_necesarios(valor),
    )


def analizar_texto(texto: str) -> list[FilaCaracter]:
    if texto is None or texto == "":
        raise ErrorDeEntrada("Debe ingresar un texto.")
    if len(texto) > 20:
        raise ErrorDeEntrada("El texto no puede superar los 20 caracteres.")

    filas = []
    for c in texto:
        cp = ord(c)
        filas.append(
            FilaCaracter(
                caracter=c,
                decimal=cp,
                unicode=f"U+{cp:04X}",
                hexadecimal=f"{cp:X}",
                bytes_utf8=" ".join(f"{b:02X}" for b in c.encode("utf-8")),
            )
        )
    return filas
