from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .servicios import ErrorDeEntrada, analizar_texto, convertir_numero


class ConversionNumericaTests(SimpleTestCase):
    def test_decimal_a_todas_las_bases(self):
        r = convertir_numero("255", 10)
        self.assertEqual(r.decimal, 255)
        self.assertEqual(r.binario, "11111111")
        self.assertEqual(r.octal, "377")
        self.assertEqual(r.hexadecimal, "FF")
        self.assertEqual((r.bits_significativos, r.bytes_necesarios), (8, 1))

    def test_hexadecimal_completa_binario_a_16_bits(self):
        r = convertir_numero("1ff", 16)
        self.assertEqual(r.decimal, 511)
        self.assertEqual(r.binario, "0000000111111111")
        self.assertEqual((r.bits_significativos, r.bytes_necesarios), (9, 2))

    def test_valor_maximo_y_cero(self):
        maximo = convertir_numero("65535", 10)
        self.assertEqual(maximo.binario, "1" * 16)
        self.assertEqual(maximo.hexadecimal, "FFFF")
        cero = convertir_numero("0", 10)
        self.assertEqual((cero.binario, cero.bits_significativos, cero.bytes_necesarios),
                         ("00000000", 1, 1))

    def test_octal_y_binario_de_origen(self):
        self.assertEqual(convertir_numero("777", 8).decimal, 511)
        self.assertEqual(convertir_numero("101", 2).decimal, 5)

    def test_digitos_invalidos_para_la_base(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "Dígitos inválidos para la base 2"):
            convertir_numero("1021", 2)
        with self.assertRaises(ErrorDeEntrada):
            convertir_numero("89", 8)

    def test_valor_fuera_de_rango(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "fuera del rango"):
            convertir_numero("65536", 10)

    def test_entrada_vacia_y_negativa(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "Debe ingresar un número"):
            convertir_numero("   ", 10)
        with self.assertRaisesMessage(ErrorDeEntrada, "negativos"):
            convertir_numero("-5", 10)


class AnalisisUtf8Tests(SimpleTestCase):
    def test_caracter_enie(self):
        (fila,) = analizar_texto("ñ")
        self.assertEqual(fila.decimal, 241)
        self.assertEqual(fila.unicode, "U+00F1")
        self.assertEqual(fila.hexadecimal, "F1")
        self.assertEqual(fila.bytes_utf8, "C3 B1")

    def test_limite_de_20_caracteres(self):
        self.assertEqual(len(analizar_texto("a" * 20)), 20)
        with self.assertRaises(ErrorDeEntrada):
            analizar_texto("a" * 21)


class VistaTests(TestCase):
    def test_formulario_numerico_muestra_resultado(self):
        resp = self.client.post(reverse("index"),
                                {"accion": "numero", "num-numero": "ff", "num-base": "16"})
        self.assertContains(resp, "11111111")

    def test_formulario_numerico_muestra_error(self):
        resp = self.client.post(reverse("index"),
                                {"accion": "numero", "num-numero": "", "num-base": "10"})
        self.assertContains(resp, "Debe ingresar un número")

    def test_formulario_texto_con_enie(self):
        resp = self.client.post(reverse("index"), {"accion": "texto", "txt-texto": "ñ"})
        self.assertContains(resp, "U+00F1")
        self.assertContains(resp, "C3 B1")
