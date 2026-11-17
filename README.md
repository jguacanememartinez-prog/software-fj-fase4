# Software FJ – Sistema de Gestión de Clientes, Servicios y Reservas

Proyecto de la **Fase 4 – Prácticas simuladas** del curso Programación (213023), UNAD, grupo 213023_611.

Aplicación en **Python 3** orientada a objetos, **sin base de datos**: toda la información vive en listas
de objetos y el único archivo que se escribe es el log de eventos y errores.

## Ejecución

```bash
python main.py
```

Requiere solo la biblioteca estándar de Python 3.8 o superior. El log se genera en `logs/software_fj.log`.

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (jerarquía desde `SoftwareFJError`) |
| `registro.py` | Configuración del archivo de logs |
| `entidades.py` | Clase abstracta `EntidadBase` y clase `Cliente` (validación y encapsulación) |
| `servicios.py` | Clase abstracta `Servicio` y `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar, procesar) |
| `main.py` | `GestorFJ` y 14 simulaciones válidas e inválidas |

## Conceptos aplicados

- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`, `@abstractmethod`).
- **Herencia y polimorfismo:** tres servicios sobrescriben `calcular_costo`, `validar_parametros` y `describir`.
- **Encapsulación:** atributos privados con `@property` y validación en los setters.
- **Sobrecarga:** `costo_total(duracion, impuesto=0.0, descuento=0.0)` admite varias formas de llamada.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/finally` y encadenamiento con `raise ... from ...`.
- **Logs:** cada evento y error queda registrado; el programa nunca se detiene.

## Códigos de error

| Código | Excepción |
|---|---|
| FJ-101 | `ClienteInvalidoError` |
| FJ-201 | `ServicioInvalidoError` |
| FJ-202 | `ServicioNoDisponibleError` |
| FJ-301 | `ReservaInvalidaError` |
| FJ-302 | `OperacionNoPermitidaError` |
| FJ-401 | `CalculoInconsistenteError` |

## Equipo y distribución del trabajo

| Integrante | Rama | Responsabilidad |
|---|---|---|
| Integrante 1 | `feature/excepciones-logs` | `excepciones.py`, `registro.py` |
| Integrante 2 | `feature/entidades-cliente` | `entidades.py` |
| Integrante 3 | `feature/servicios` | `servicios.py` |
| Integrante 4 | `feature/reserva` | `reserva.py` |
| Integrante 5 | `feature/simulaciones` | `main.py`, README |
