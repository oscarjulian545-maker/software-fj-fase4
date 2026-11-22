"""Modelos orientados a objetos para la gestión de clientes, servicios y reservas de Software FJ."""  # Describe el módulo
from abc import ABC, abstractmethod  # Importa herramientas para definir clases y métodos abstractos
from typing import List, Optional  # Importa anotaciones de tipos para claridad en el código
from exceptions import (  # Importa las excepciones personalizadas del sistema
    ErrorCalculoFinanciero,
    ErrorReservaInvalida,
    ErrorServicioNoDisponible,
    ErrorValidacionEntidad,
)


class EntidadSistema(ABC):
    """Clase abstracta general que representa entidades identificables dentro del sistema."""  # Clase abstracta base

    def __init__(self, id_entidad: str) -> None:
        """Valida y asigna el identificador único de la entidad."""  # Documenta el inicializador
        if not id_entidad or not id_entidad.strip():  # Verifica que el ID no esté vacío ni solo con espacios
            raise ErrorValidacionEntidad(  # Lanza excepción personalizada si el ID falta
                "El identificador de la entidad es obligatorio.",
                detalle="id_entidad vacío o nulo en EntidadSistema",
            )
        self._id_entidad = id_entidad.strip()  # Guarda el ID normalizado en atributo protegido

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador de la entidad."""  # Documenta el getter
        return self._id_entidad  # Devuelve el valor del ID

    @abstractmethod
    def describir(self) -> str:
        """Método abstracto que cada entidad debe implementar para describirse."""  # Obliga a subclases a implementarlo


class Cliente(EntidadSistema):
    """Representa a un cliente con encapsulación de datos personales y validaciones estrictas."""  # Clase Cliente

    def __init__(self, id_entidad: str, nombre: str, correo: str, documento: str) -> None:
        """Inicializa y valida los atributos encapsulados de un cliente."""  # Documenta el constructor
        super().__init__(id_entidad)  # Valida y asigna id_entidad desde EntidadSistema
        self.__nombre = ""  # Inicializa atributo privado de nombre
        self.__correo = ""  # Inicializa atributo privado de correo
        self.__documento = ""  # Inicializa atributo privado de documento
        self.nombre = nombre  # Usa el setter para validar el nombre
        self.correo = correo  # Usa el setter para validar el correo
        self.documento = documento  # Usa el setter para validar el documento

    @property
    def nombre(self) -> str:
        """Obtiene el nombre del cliente."""  # Getter de nombre
        return self.__nombre  # Retorna el nombre privado

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida que el nombre tenga al menos 2 caracteres."""  # Setter de nombre
        if not valor or len(valor.strip()) < 2:  # Comprueba longitud mínima válida
            raise ErrorValidacionEntidad(  # Lanza excepción si el nombre es inválido
                "Nombre de cliente inválido.",
                detalle=f"Valor recibido: '{valor}'",
            )
        self.__nombre = valor.strip()  # Asigna el nombre limpio

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""  # Getter de correo
        return self.__correo  # Retorna el correo privado

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida que el correo contenga '@' y un dominio con '.'."""  # Setter de correo
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:  # Verifica formato básico de correo
            raise ErrorValidacionEntidad(  # Lanza excepción si el correo no es válido
                "Correo electrónico del cliente no válido.",
                detalle=f"Correo recibido: '{valor}'",
            )
        self.__correo = valor.strip().lower()  # Normaliza y guarda el correo

    @property
    def documento(self) -> str:
        """Obtiene el documento de identidad del cliente."""  # Getter de documento
        return self.__documento  # Retorna el documento privado

    @documento.setter
    def documento(self, valor: str) -> None:
        """Valida que el documento sea numérico y tenga al menos 5 dígitos."""  # Setter de documento
        limpio = valor.strip() if isinstance(valor, str) else ""  # Limpia cadenas y protege tipos no string
        if not limpio.isdigit() or len(limpio) < 5:  # Verifica dígitos y longitud mínima
            raise ErrorValidacionEntidad(  # Lanza excepción si el documento es inválido
                "Documento de identidad inválido.",
                detalle=f"Documento recibido: '{valor}'",
            )
        self.__documento = limpio  # Guarda el documento validado

    def describir(self) -> str:
        """Retorna una descripción resumida y segura del cliente."""  # Implementación polimórfica de describir
        return f"Cliente [{self._id_entidad}]: {self.__nombre} (Doc: {self.__documento}, Correo: {self.__correo})"


class Servicio(EntidadSistema, ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""  # Clase abstracta Servicio

    def __init__(self, id_entidad: str, nombre: str, tarifa_base: float, disponible: bool = True) -> None:
        """Inicializa los datos comunes de un servicio y valida su tarifa."""  # Constructor de Servicio
        super().__init__(id_entidad)  # Inicializa el ID de la entidad
        if not nombre or not nombre.strip():  # Verifica que el servicio tenga nombre
            raise ErrorValidacionEntidad(  # Lanza excepción si falta el nombre
                "El nombre del servicio es obligatorio.",
                detalle="nombre vacío en Servicio",
            )
        if tarifa_base <= 0:  # Verifica que la tarifa base sea positiva
            raise ErrorCalculoFinanciero(  # Lanza excepción si la tarifa es cero o negativa
                "La tarifa base del servicio debe ser mayor que cero.",
                detalle=f"tarifa_base={tarifa_base}",
            )
        self.nombre = nombre.strip()  # Guarda el nombre del servicio
        self.tarifa_base = float(tarifa_base)  # Guarda la tarifa base como flotante
        self.disponible = bool(disponible)  # Indica si el servicio está disponible

    def verificar_disponibilidad(self) -> None:
        """Comprueba si el servicio está disponible o lanza una excepción."""  # Valida disponibilidad
        if not self.disponible:  # Revisa si el servicio está inactivo/ocupado
            raise ErrorServicioNoDisponible(  # Lanza excepción de servicio no disponible
                f"El servicio '{self.nombre}' no está disponible en este momento.",
                detalle=f"id_servicio={self._id_entidad}, disponible={self.disponible}",
            )

    @abstractmethod
    def validar_parametros(self, duracion_horas: float, extra: Optional[int] = None) -> None:
        """Valida los parámetros específicos de cada tipo de servicio."""  # Método abstracto de validación

    def calcular_costo(
        self,
        duracion_horas: float,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.19,
        extra: Optional[int] = None,
    ) -> float:
        """Calcula el costo total soportando parámetros opcionales (descuento, impuesto y parámetro extra)."""  # Sobrecarga por parámetros opcionales
        self.validar_parametros(duracion_horas, extra=extra)  # Valida duración y parámetro extra según el servicio
        if not (0.0 <= descuento_pct < 1.0):  # Valida que el descuento esté en rango válido (0% a <100%)
            raise ErrorCalculoFinanciero(  # Lanza excepción si el porcentaje de descuento es inconsistente
                "El porcentaje de descuento debe estar entre 0.0 y menor que 1.0.",
                detalle=f"descuento_pct={descuento_pct}",
            )
        if impuesto_pct < 0.0:  # Valida que el impuesto no sea negativo
            raise ErrorCalculoFinanciero(  # Lanza excepción si el impuesto es negativo
                "El porcentaje de impuesto no puede ser negativo.",
                detalle=f"impuesto_pct={impuesto_pct}",
            )
        subtotal = self._calcular_subtotal(duracion_horas, extra=extra)  # Calcula subtotal específico de cada servicio
        if subtotal <= 0:  # Verifica que el subtotal resultante sea válido
            raise ErrorCalculoFinanciero(  # Lanza excepción si el cálculo produce un valor no positivo
                "El subtotal calculado es inconsistente.",
                detalle=f"subtotal={subtotal}",
            )
        con_descuento = subtotal * (1.0 - descuento_pct)  # Aplica descuento opcional
        total = con_descuento * (1.0 + impuesto_pct)  # Aplica impuesto opcional
        return round(total, 2)  # Redondea el total a dos decimales

    @abstractmethod
    def _calcular_subtotal(self, duracion_horas: float, extra: Optional[int] = None) -> float:
        """Calcula el subtotal antes de descuentos e impuestos según el tipo de servicio."""  # Método abstracto interno


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o desarrollo."""  # Subclase 1 de Servicio

    def __init__(self, id_entidad: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True) -> None:
        """Inicializa la sala y valida su capacidad máxima."""  # Constructor de ReservaSala
        super().__init__(id_entidad, nombre, tarifa_base, disponible)  # Llama al constructor de Servicio
        if capacidad <= 0:  # Verifica que la sala tenga capacidad positiva
            raise ErrorValidacionEntidad(  # Lanza excepción si la capacidad es inválida
                "La capacidad de la sala debe ser mayor a cero.",
                detalle=f"capacidad={capacidad}",
            )
        self.capacidad = capacidad  # Guarda capacidad de personas de la sala

    def validar_parametros(self, duracion_horas: float, extra: Optional[int] = None) -> None:
        """Valida duración en horas y número de asistentes (extra)."""  # Sobrescribe validación de parámetros
        if duracion_horas <= 0 or duracion_horas > 12:  # Restringe duración de sala entre >0 y <=12 horas
            raise ErrorValidacionEntidad(  # Lanza excepción si la duración está fuera de rango
                "La reserva de sala debe tener una duración mayor a 0 y máximo 12 horas.",
                detalle=f"duracion_horas={duracion_horas}",
            )
        if extra is not None and (extra <= 0 or extra > self.capacidad):  # Valida asistentes contra capacidad
            raise ErrorReservaInvalida(  # Lanza excepción si excede capacidad o es no positivo
                f"Número de asistentes inválido para la sala '{self.nombre}' (capacidad máx: {self.capacidad}).",
                detalle=f"asistentes={extra}",
            )

    def _calcular_subtotal(self, duracion_horas: float, extra: Optional[int] = None) -> float:
        """Calcula el costo de la sala multiplicando tarifa base por duración."""  # Sobrescribe cálculo base
        return self.tarifa_base * duracion_horas  # Retorna subtotal de sala

    def describir(self) -> str:
        """Describe el servicio de reserva de sala."""  # Sobrescribe describir
        estado = "Disponible" if self.disponible else "No disponible"  # Traduce estado booleano
        return f"Sala [{self._id_entidad}] '{self.nombre}' | Cap: {self.capacidad} | Tarifa/h: ${self.tarifa_base} | {estado}"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""  # Subclase 2 de Servicio

    def __init__(self, id_entidad: str, nombre: str, tarifa_base: float, stock: int, disponible: bool = True) -> None:
        """Inicializa el equipo y valida el stock disponible."""  # Constructor de AlquilerEquipo
        super().__init__(id_entidad, nombre, tarifa_base, disponible)  # Llama al constructor de Servicio
        if stock < 0:  # Verifica que el stock no sea negativo
            raise ErrorValidacionEntidad(  # Lanza excepción si el stock es negativo
                "El stock de equipos no puede ser negativo.",
                detalle=f"stock={stock}",
            )
        self.stock = stock  # Almacena cantidad de unidades en stock

    def validar_parametros(self, duracion_horas: float, extra: Optional[int] = None) -> None:
        """Valida duración y cantidad de equipos solicitados (extra)."""  # Sobrescribe validación de parámetros
        if duracion_horas <= 0 or duracion_horas > 72:  # Permite alquileres desde >0 hasta 72 horas
            raise ErrorValidacionEntidad(  # Lanza excepción si la duración es inválida
                "El alquiler de equipos debe durar entre más de 0 y 72 horas.",
                detalle=f"duracion_horas={duracion_horas}",
            )
        cantidad = 1 if extra is None else extra  # Asume 1 unidad si no se especifica cantidad extra
        if cantidad <= 0 or cantidad > self.stock:  # Comprueba que haya stock suficiente
            raise ErrorServicioNoDisponible(  # Lanza excepción si no hay unidades suficientes
                f"Stock insuficiente para '{self.nombre}' (solicitado: {cantidad}, disponible: {self.stock}).",
                detalle=f"stock={self.stock}, solicitado={cantidad}",
            )

    def _calcular_subtotal(self, duracion_horas: float, extra: Optional[int] = None) -> float:
        """Calcula el subtotal multiplicando tarifa base, duración y cantidad de equipos."""  # Sobrescribe cálculo base
        cantidad = 1 if extra is None else extra  # Obtiene cantidad de equipos
        return self.tarifa_base * duracion_horas * cantidad  # Retorna subtotal de alquiler

    def describir(self) -> str:
        """Describe el servicio de alquiler de equipos."""  # Sobrescribe describir
        estado = "Disponible" if self.disponible else "No disponible"  # Traduce estado booleano
        return f"Equipo [{self._id_entidad}] '{self.nombre}' | Stock: {self.stock} | Tarifa/h: ${self.tarifa_base} | {estado}"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías técnicas o de software."""  # Subclase 3 de Servicio

    def __init__(self, id_entidad: str, nombre: str, tarifa_base: float, especialista: str, disponible: bool = True) -> None:
        """Inicializa la asesoría y valida el nombre del especialista."""  # Constructor de AsesoriaEspecializada
        super().__init__(id_entidad, nombre, tarifa_base, disponible)  # Llama al constructor de Servicio
        if not especialista or not especialista.strip():  # Verifica que se indique especialista
            raise ErrorValidacionEntidad(  # Lanza excepción si falta el especialista
                "Debe asignarse un especialista a la asesoría.",
                detalle="especialista vacío",
            )
        self.especialista = especialista.strip()  # Guarda nombre del especialista

    def validar_parametros(self, duracion_horas: float, extra: Optional[int] = None) -> None:
        """Valida duración de la sesión de asesoría."""  # Sobrescribe validación de parámetros
        if duracion_horas < 0.5 or duracion_horas > 8:  # Exige bloques de asesoría entre 0.5 y 8 horas
            raise ErrorValidacionEntidad(  # Lanza excepción si la duración es inválida
                "La asesoría especializada debe durar entre 0.5 y 8 horas.",
                detalle=f"duracion_horas={duracion_horas}",
            )

    def _calcular_subtotal(self, duracion_horas: float, extra: Optional[int] = None) -> float:
        """Calcula el costo de la asesoría según duración en horas."""  # Sobrescribe cálculo base
        return self.tarifa_base * duracion_horas  # Retorna subtotal de asesoría

    def describir(self) -> str:
        """Describe el servicio de asesoría especializada."""  # Sobrescribe describir
        estado = "Disponible" if self.disponible else "No disponible"  # Traduce estado booleano
        return f"Asesoría [{self._id_entidad}] '{self.nombre}' | Esp: {self.especialista} | Tarifa/h: ${self.tarifa_base} | {estado}"


class Reserva(EntidadSistema):
    """Gestiona la relación entre un cliente, un servicio, su duración y su estado."""  # Clase Reserva

    def __init__(
        self,
        id_entidad: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: float,
        cantidad_o_asistentes: Optional[int] = None,
    ) -> None:
        """Crea una reserva en estado PENDIENTE tras validar entidades y servicio."""  # Constructor de Reserva
        super().__init__(id_entidad)  # Valida id_entidad de la reserva
        if not isinstance(cliente, Cliente):  # Verifica que el argumento sea instancia de Cliente
            raise ErrorValidacionEntidad("El objeto proporcionado no es un Cliente válido.")  # Lanza excepción si no lo es
        if not isinstance(servicio, Servicio):  # Verifica que el argumento sea instancia de Servicio
            raise ErrorValidacionEntidad("El objeto proporcionado no es un Servicio válido.")  # Lanza excepción si no lo es
        servicio.verificar_disponibilidad()  # Verifica que el servicio esté disponible al crear la reserva
        servicio.validar_parametros(duracion_horas, extra=cantidad_o_asistentes)  # Valida parámetros específicos
        self.cliente = cliente  # Asigna el cliente a la reserva
        self.servicio = servicio  # Asigna el servicio a la reserva
        self.duracion_horas = duracion_horas  # Asigna duración en horas
        self.cantidad_o_asistentes = cantidad_o_asistentes  # Guarda parámetro opcional extra
        self.estado = "PENDIENTE"  # Establece estado inicial de la reserva
        self.total_calculado: Optional[float] = None  # Inicializa el total calculado

    def confirmar(self) -> None:
        """Confirma la reserva si se encuentra en estado PENDIENTE."""  # Método confirmar
        if self.estado == "CANCELADA":  # Impide confirmar una reserva cancelada
            raise ErrorReservaInvalida(  # Lanza excepción por transición inválida
                f"No se puede confirmar la reserva '{self._id_entidad}' porque está cancelada.",
                detalle=f"estado_actual={self.estado}",
            )
        if self.estado == "CONFIRMADA":  # Evita confirmar dos veces
            raise ErrorReservaInvalida(  # Lanza excepción por operación redundante/no permitida
                f"La reserva '{self._id_entidad}' ya se encuentra confirmada.",
                detalle=f"estado_actual={self.estado}",
            )
        self.servicio.verificar_disponibilidad()  # Revisa disponibilidad antes de confirmar
        self.estado = "CONFIRMADA"  # Actualiza estado a CONFIRMADA

    def cancelar(self) -> None:
        """Cancela la reserva si no ha sido ya cancelada."""  # Método cancelar
        if self.estado == "CANCELADA":  # Verifica si ya está cancelada
            raise ErrorReservaInvalida(  # Lanza excepción si ya estaba cancelada
                f"La reserva '{self._id_entidad}' ya fue cancelada previamente.",
                detalle=f"estado_actual={self.estado}",
            )
        self.estado = "CANCELADA"  # Actualiza estado a CANCELADA

    def procesar(self, descuento_pct: float = 0.0, impuesto_pct: float = 0.19) -> float:
        """Procesa la reserva confirmada y calcula su costo total."""  # Método procesar
        if self.estado != "CONFIRMADA":  # Exige que la reserva esté confirmada para procesarse
            raise ErrorReservaInvalida(  # Lanza excepción si intenta procesar sin confirmar
                f"Solo se pueden procesar reservas en estado CONFIRMADA (estado actual: {self.estado}).",
                detalle=f"id_reserva={self._id_entidad}, estado={self.estado}",
            )
        self.servicio.verificar_disponibilidad()  # Verifica nuevamente disponibilidad del servicio
        self.total_calculado = self.servicio.calcular_costo(  # Calcula el costo aplicando descuentos e impuestos
            duracion_horas=self.duracion_horas,
            descuento_pct=descuento_pct,
            impuesto_pct=impuesto_pct,
            extra=self.cantidad_o_asistentes,
        )
        self.estado = "PROCESADA"  # Marca la reserva como procesada
        return self.total_calculado  # Retorna el monto final

    def describir(self) -> str:
        """Retorna una descripción completa de la reserva."""  # Sobrescribe describir
        monto_txt = f"${self.total_calculado}" if self.total_calculado is not None else "Pendiente de cálculo"  # Formatea total
        return (
            f"Reserva [{self._id_entidad}] | Estado: {self.estado} | "
            f"{self.cliente.describir()} | {self.servicio.describir()} | "
            f"Duración: {self.duracion_horas}h | Total: {monto_txt}"
        )


class GestorSoftwareFJ:
    """Administra colecciones en memoria (listas) de clientes, servicios y reservas sin base de datos."""  # Gestor en memoria

    def __init__(self) -> None:
        """Inicializa las listas internas de gestión."""  # Constructor del gestor
        self.clientes: List[Cliente] = []  # Lista interna de clientes
        self.servicios: List[Servicio] = []  # Lista interna de servicios
        self.reservas: List[Reserva] = []  # Lista interna de reservas

    def registrar_cliente(self, cliente: Cliente) -> None:
        """Agrega un cliente a la lista interna evitando IDs duplicados."""  # Registra cliente
        if any(c.id_entidad == cliente.id_entidad for c in self.clientes):  # Comprueba ID duplicado
            raise ErrorValidacionEntidad(  # Lanza excepción por ID repetido
                f"Ya existe un cliente registrado con el ID '{cliente.id_entidad}'.",
                detalle="ID de cliente duplicado en GestorSoftwareFJ",
            )
        self.clientes.append(cliente)  # Añade cliente a la lista

    def registrar_servicio(self, servicio: Servicio) -> None:
        """Agrega un servicio a la lista interna evitando IDs duplicados."""  # Registra servicio
        if any(s.id_entidad == servicio.id_entidad for s in self.servicios):  # Comprueba ID duplicado
            raise ErrorValidacionEntidad(  # Lanza excepción por ID repetido
                f"Ya existe un servicio registrado con el ID '{servicio.id_entidad}'.",
                detalle="ID de servicio duplicado en GestorSoftwareFJ",
            )
        self.servicios.append(servicio)  # Añade servicio a la lista

    def crear_reserva(self, reserva: Reserva) -> None:
        """Registra una reserva en la lista interna tras verificar cliente y servicio."""  # Registra reserva
        if reserva.cliente not in self.clientes:  # Verifica que el cliente pertenezca al sistema
            raise ErrorReservaInvalida(  # Lanza excepción si el cliente no está registrado
                f"El cliente '{reserva.cliente.id_entidad}' no está registrado en el sistema.",
                detalle="Cliente ausente en lista self.clientes",
            )
        if reserva.servicio not in self.servicios:  # Verifica que el servicio pertenezca al sistema
            raise ErrorReservaInvalida(  # Lanza excepción si el servicio no está registrado
                f"El servicio '{reserva.servicio.id_entidad}' no está registrado en el sistema.",
                detalle="Servicio ausente en lista self.servicios",
            )
        if any(r.id_entidad == reserva.id_entidad for r in self.reservas):  # Verifica ID duplicado de reserva
            raise ErrorReservaInvalida(  # Lanza excepción si el ID de reserva ya existe
                f"Ya existe una reserva con el ID '{reserva.id_entidad}'.",
                detalle="ID de reserva duplicado en GestorSoftwareFJ",
            )
        self.reservas.append(reserva)  # Añade la reserva a la lista