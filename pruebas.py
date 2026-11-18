"""
pruebas.py
Pruebas automáticas (unittest) del sistema Software FJ.
Ejecutar con:  python -m unittest pruebas -v
"""
import unittest

from entidades import Cliente
from excepciones import (
    CalculoInconsistenteError,
    ClienteInvalidoError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from reserva import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


class PruebasCliente(unittest.TestCase):
    """Valida la creación de clientes y sus reglas."""

    def test_cliente_valido(self):
        c = Cliente("Ana Pérez", "ANA@mail.com", "3101234567")
        self.assertEqual(c.correo, "ana@mail.com")  # el correo se guarda en minúscula

    def test_correo_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana Pérez", "ana-mail.com", "3101234567")

    def test_nombre_corto(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Al", "a@mail.com", "3101234567")

    def test_telefono_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana Pérez", "a@mail.com", "abc")


class PruebasServicios(unittest.TestCase):
    """Valida polimorfismo, sobrecarga y validaciones de servicios."""

    def test_costo_sala_con_recargo(self):
        sala = ReservaSala("Sala grande", 10000, 30)  # capacidad > 20 => +15 %
        self.assertAlmostEqual(sala.calcular_costo(2), 23000.0)

    def test_costo_total_con_impuesto_y_descuento(self):
        ase = AsesoriaEspecializada("Asesoría", 100000, "junior")
        # 100000 * 1 hora * (1-0.10) * (1+0.19) = 107100
        self.assertEqual(ase.costo_total(1, 0.19, 0.10), 107100.0)

    def test_costo_total_sin_extras(self):
        eq = AlquilerEquipo("Portátiles", 30000, 2)
        self.assertEqual(eq.costo_total(1), 63000.0)  # 30000*2*1*1.05

    def test_tarifa_negativa(self):
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("Sala", -5, 10)

    def test_nivel_inexistente(self):
        with self.assertRaises(ServicioInvalidoError):
            AsesoriaEspecializada("Ase", 50000, "maestro")

    def test_descuento_inconsistente(self):
        sala = ReservaSala("Sala", 10000, 10)
        with self.assertRaises(CalculoInconsistenteError):
            sala.costo_total(2, descuento=1.5)

    def test_polimorfismo_describir(self):
        servicios = [ReservaSala("S", 1000, 5), AlquilerEquipo("E", 1000, 1),
                     AsesoriaEspecializada("A", 1000, "senior")]
        for s in servicios:
            self.assertIn(s.nombre, s.describir())


class PruebasReserva(unittest.TestCase):
    """Valida el ciclo de vida de una reserva y las excepciones."""

    def setUp(self):
        self.cliente = Cliente("Luis Mora", "luis@mail.com", "3207654321")
        self.sala = ReservaSala("Sala", 10000, 10)

    def test_reserva_exitosa(self):
        r = Reserva(self.cliente, self.sala, 2)
        r.procesar()
        self.assertEqual(r.estado, Reserva.CONFIRMADA)

    def test_parametros_faltantes(self):
        with self.assertRaises(ReservaInvalidaError):
            Reserva(None, self.sala, 2)

    def test_duracion_invalida_encadena_causa(self):
        r = Reserva(self.cliente, self.sala, 99)
        with self.assertRaises(ReservaInvalidaError) as ctx:
            r.procesar()
        # El encadenamiento debe conservar la causa original
        self.assertIsInstance(ctx.exception.__cause__, ServicioInvalidoError)
        self.assertEqual(r.estado, Reserva.FALLIDA)

    def test_servicio_no_disponible(self):
        self.sala.disponible = False
        r = Reserva(self.cliente, self.sala, 2)
        with self.assertRaises(ServicioNoDisponibleError):
            r.procesar()

    def test_doble_cancelacion(self):
        r = Reserva(self.cliente, self.sala, 2)
        r.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            r.cancelar()

    def test_jerarquia_de_excepciones(self):
        # Todas las excepciones propias deben heredar de SoftwareFJError
        self.assertTrue(issubclass(ReservaInvalidaError, SoftwareFJError))


if __name__ == "__main__":
    unittest.main()
