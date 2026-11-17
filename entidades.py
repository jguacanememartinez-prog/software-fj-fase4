"""
entidades.py
Clase abstracta EntidadBase y clase Cliente con validaciones y encapsulación.
"""
import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError
from registro import log


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    # Contador de clase para asignar identificadores únicos
    _contador = 0

    def __init__(self):
        # Incrementamos el contador compartido por todas las entidades
        EntidadBase._contador += 1
        # Atributo "privado" por convención: el id no debe modificarse
        self._id = EntidadBase._contador

    @property
    def id(self):
        """Solo lectura: el id nunca se modifica desde afuera."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe describirse a sí misma (polimorfismo)."""


class Cliente(EntidadBase):
    """Cliente de Software FJ con datos personales encapsulados y validados."""

    # Expresión regular sencilla para validar correos
    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

    def __init__(self, nombre, correo, telefono):
        super().__init__()
        # Los setters (propiedades) validan cada dato al asignarlo
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        log.info("Cliente creado: id=%s nombre=%s", self.id, self.nombre)

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Debe ser texto y tener al menos 3 caracteres útiles
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    # ---------- correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Debe ser texto y cumplir el patrón de correo
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__correo = valor.lower()

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Solo dígitos, entre 7 y 10 caracteres (números colombianos)
        texto = str(valor)
        if not texto.isdigit() or not 7 <= len(texto) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r}")
        self.__telefono = texto

    def describir(self):
        """Descripción legible del cliente."""
        return f"Cliente #{self.id}: {self.nombre} <{self.correo}> Tel. {self.telefono}"
