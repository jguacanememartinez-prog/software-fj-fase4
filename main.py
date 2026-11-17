"""
main.py
Programa principal de Software FJ: gestiona clientes, servicios y reservas en
listas internas (sin base de datos) y ejecuta 14 simulaciones, válidas e inválidas.
El programa NUNCA se detiene ante un error: cada operación está protegida.
"""
from entidades import Cliente
from excepciones import SoftwareFJError
from registro import ARCHIVO_LOG, log
from reserva import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


class GestorFJ:
    """Administra las listas internas de clientes, servicios y reservas."""

    def __init__(self):
        # Listas internas que reemplazan a una base de datos
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, nombre, correo, telefono):
        """Crea un cliente y lo guarda solo si pasa las validaciones."""
        cliente = Cliente(nombre, correo, telefono)  # puede lanzar ClienteInvalidoError
        self.clientes.append(cliente)
        return cliente

    def registrar_servicio(self, servicio):
        """Agrega un servicio ya creado a la lista."""
        self.servicios.append(servicio)
        return servicio

    def crear_reserva(self, cliente, servicio, duracion, impuesto=0.0, descuento=0.0):
        """Crea y procesa una reserva; siempre queda registrada en la lista."""
        reserva = Reserva(cliente, servicio, duracion)  # puede lanzar ReservaInvalidaError
        self.reservas.append(reserva)
        reserva.procesar(impuesto, descuento)
        return reserva


def simular(numero, titulo, operacion, resultados):
    """
    Ejecuta una operación protegida: captura TODO error, lo registra en el log
    y continúa con la siguiente simulación.
    """
    print(f"\n--- Simulación {numero}: {titulo}")
    log.info("INICIO simulación %s: %s", numero, titulo)
    try:
        resultado = operacion()
    except SoftwareFJError as error:
        # Error controlado del dominio: se registra con su causa si existe
        causa = f" | causa: {error.__cause__}" if error.__cause__ else ""
        log.error("Simulación %s falló (esperado): %s%s", numero, error, causa)
        print(f"   ERROR CONTROLADO -> {error}{causa}")
        resultados.append((numero, titulo, "Error controlado"))
    except Exception as error:  # noqa: BLE001 - red de seguridad final
        # Error inesperado: también se registra y el programa sigue
        log.exception("Simulación %s: error inesperado: %s", numero, error)
        print(f"   ERROR INESPERADO -> {error}")
        resultados.append((numero, titulo, "Error inesperado"))
    else:
        log.info("Simulación %s exitosa.", numero)
        print(f"   OK -> {resultado}")
        resultados.append((numero, titulo, "Exitosa"))
    finally:
        log.info("FIN simulación %s", numero)


def main():
    """Ejecuta las 14 simulaciones y muestra un resumen final."""
    log.info("===== INICIO DEL SISTEMA SOFTWARE FJ =====")
    gestor = GestorFJ()
    r = []  # resultados de las simulaciones

    # Datos base reutilizados por varias simulaciones
    base = {}

    # 1. Cliente válido
    def s1():
        base["ana"] = gestor.registrar_cliente("Ana Pérez", "ana.perez@mail.com", "3101234567")
        return base["ana"].describir()
    simular(1, "Registro válido de cliente", s1, r)

    # 2. Cliente con correo inválido
    simular(2, "Cliente con correo inválido",
            lambda: gestor.registrar_cliente("Luis Mora", "luis-mail.com", "3207654321"), r)

    # 3. Cliente con nombre vacío y teléfono inválido
    simular(3, "Cliente con nombre vacío",
            lambda: gestor.registrar_cliente("  ", "x@mail.com", "3207654321"), r)

    # 4. Segundo cliente válido
    def s4():
        base["luis"] = gestor.registrar_cliente("Luis Mora", "luis@mail.com", "3207654321")
        return base["luis"].describir()
    simular(4, "Segundo cliente válido", s4, r)

    # 5. Tres servicios válidos (uno por tipo)
    def s5():
        base["sala"] = gestor.registrar_servicio(ReservaSala("Sala Andes", 50000, 25))
        base["equipo"] = gestor.registrar_servicio(AlquilerEquipo("Portátiles Dell", 30000, 4))
        base["asesoria"] = gestor.registrar_servicio(
            AsesoriaEspecializada("Asesoría en Python", 80000, "senior"))
        return [s.describir() for s in gestor.servicios]
    simular(5, "Creación correcta de 3 servicios", s5, r)

    # 6. Servicio inválido: tarifa negativa
    simular(6, "Servicio con tarifa negativa",
            lambda: gestor.registrar_servicio(ReservaSala("Sala X", -100, 10)), r)

    # 7. Servicio inválido: nivel de asesoría inexistente
    simular(7, "Asesoría con nivel inexistente",
            lambda: gestor.registrar_servicio(AsesoriaEspecializada("Asesoría Y", 70000, "maestro")), r)

    # 8. Reserva exitosa con IVA y descuento (método sobrecargado)
    def s8():
        res = gestor.crear_reserva(base["ana"], base["sala"], 3, impuesto=0.19, descuento=0.10)
        return res.describir()
    simular(8, "Reserva exitosa de sala con IVA y descuento", s8, r)

    # 9. Reserva exitosa de equipo sin impuestos
    def s9():
        return gestor.crear_reserva(base["luis"], base["equipo"], 5).describir()
    simular(9, "Reserva exitosa de equipos (costo base)", s9, r)

    # 10. Duración inválida (encadenamiento de excepciones)
    simular(10, "Reserva con duración inválida (excepción encadenada)",
            lambda: gestor.crear_reserva(base["ana"], base["asesoria"], 20), r)

    # 11. Servicio no disponible
    def s11():
        base["equipo"].disponible = False
        return gestor.crear_reserva(base["luis"], base["equipo"], 2)
    simular(11, "Reserva de servicio no disponible", s11, r)

    # 12. Parámetros faltantes
    simular(12, "Reserva con cliente faltante (None)",
            lambda: gestor.crear_reserva(None, base["sala"], 2), r)

    # 13. Cálculo inconsistente (descuento del 150 %)
    simular(13, "Cálculo inconsistente (descuento > 100 %)",
            lambda: gestor.crear_reserva(base["ana"], base["sala"], 2, descuento=1.5), r)

    # 14. Cancelar y volver a cancelar (operación no permitida)
    def s14():
        reserva = gestor.reservas[0]
        reserva.cancelar()  # primera cancelación válida
        reserva.cancelar()  # segunda: no permitida
    simular(14, "Cancelación doble de una reserva", s14, r)

    # ---- Resumen final ----
    print("\n================ RESUMEN ================")
    for numero, titulo, estado in r:
        print(f"{numero:>2}. {titulo:<55} {estado}")
    print(f"\nClientes: {len(gestor.clientes)} | Servicios: {len(gestor.servicios)} "
          f"| Reservas: {len(gestor.reservas)}")
    print(f"Log completo en: {ARCHIVO_LOG}")
    log.info("===== FIN DEL SISTEMA: el programa terminó sin interrupciones =====")


if __name__ == "__main__":
    main()
