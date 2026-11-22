"""Ejecución secuencial de al menos 10 simulaciones del sistema de Software FJ."""  # Documenta el módulo
from typing import Callable  # Importa Callable para tipar funciones de simulación
from exceptions import (  # Importa las excepciones personalizadas del sistema
    ErrorCalculoFinanciero,
    ErrorReservaInvalida,
    ErrorServicioNoDisponible,
    ErrorSoftwareFJ,
    ErrorValidacionEntidad,
)
from logger_config import configurar_logger  # Importa el configurador de logs
from models import (  # Importa las clases del modelo orientado a objetos
    AlquilerEquipo,
    AsesoriaEspecializada,
    Cliente,
    GestorSoftwareFJ,
    Reserva,
    ReservaSala,
)

logger = configurar_logger()  # Inicializa el logger del sistema


def ejecutar_simulacion(numero: int, titulo: str, accion: Callable[[], str]) -> None:
    """Ejecuta una simulación con try/except/else/finally y encadenamiento ante fallos inesperados."""  # Documenta el runner
    logger.info(f"--- Iniciando Simulación #{numero}: {titulo} ---")  # Registra el inicio de la simulación
    estado_final = "COMPLETADA"  # Estado inicial de control para el bloque finally
    try:
        resultado = accion()  # Ejecuta la lógica específica de la simulación
    except ErrorSoftwareFJ as exc:
        estado_final = "CONTROLADA_CON_ERROR"  # Marca que ocurrió un error controlado del dominio
        logger.error(  # Registra la excepción personalizada y su detalle en el archivo de logs
            f"Simulación #{numero} controlada por excepción [{type(exc).__name__}]: "
            f"{exc.mensaje} | Detalle: {exc.detalle}"
        )
    except Exception as exc:
        estado_final = "ERROR_ENCADENADO"  # Marca que se encadenó una excepción inesperada
        try:
            raise ErrorSoftwareFJ(  # Encadena la excepción original usando 'raise ... from exc'
                f"Fallo inesperado en simulación #{numero} durante '{titulo}'.",
                detalle=f"Causa original ({type(exc).__name__}): {exc}",
            ) from exc
        except ErrorSoftwareFJ as encadenada:
            logger.error(  # Registra el error encadenado en el archivo de logs
                f"Simulación #{numero} encadenada [{type(encadenada).__name__}]: "
                f"{encadenada.mensaje} | {encadenada.detalle} | Causa: {encadenada.__cause__}"
            )
    else:
        logger.info(f"Simulación #{numero} exitosa: {resultado}")  # Registra el resultado si no hubo excepciones
    finally:
        logger.info(f"Finalizando Simulación #{numero} | Estado: {estado_final}")  # Se ejecuta siempre al cerrar el bloque


def correr_simulaciones() -> None:
    """Ejecuta 12 simulaciones completas (válidas e inválidas) manteniendo el sistema activo."""  # Función principal de pruebas
    gestor = GestorSoftwareFJ()  # Instancia el gestor en memoria sin base de datos
    clientes_creados = {}  # Diccionario auxiliar de apoyo en memoria para las pruebas
    servicios_creados = {}  # Diccionario auxiliar de servicios en memoria
    reservas_creadas = {}  # Diccionario auxiliar de reservas en memoria

    # Simulación 1: Registro válido de cliente con encapsulación y validación
    def sim_01() -> str:
        cliente = Cliente("CLI-01", "Laura Gómez", "laura.gomez@correo.com", "1110456789")  # Crea cliente válido
        gestor.registrar_cliente(cliente)  # Registra el cliente en la lista interna del gestor
        clientes_creados["CLI-01"] = cliente  # Guarda referencia para simulaciones posteriores
        return cliente.describir()  # Devuelve descripción del cliente registrado

    # Simulación 2: Registro inválido de cliente por correo incorrecto
    def sim_02() -> str:
        cliente_malo = Cliente("CLI-02", "Carlos Ruiz", "correo_sin_arroba", "1110987654")  # Falla validación de correo
        gestor.registrar_cliente(cliente_malo)  # No se ejecutará si falla antes
        return "No debería llegar aquí"

    # Simulación 3: Registro inválido de cliente por documento no numérico
    def sim_03() -> str:
        cliente_doc = Cliente("CLI-03", "Ana Torres", "ana.torres@correo.com", "ABC-123")  # Falla validación de documento
        gestor.registrar_cliente(cliente_doc)  # No se ejecuta si falla antes
        return "No debería llegar aquí"

    # Simulación 4: Creación válida de 3 servicios especializados (Sala, Equipo, Asesoría)
    def sim_04() -> str:
        sala = ReservaSala("SRV-SALA-1", "Sala Innovación", 45000.0, capacidad=12, disponible=True)  # Servicio 1: Sala
        equipo = AlquilerEquipo("SRV-EQ-1", "Laptop Desarrollador", 18000.0, stock=5, disponible=True)  # Servicio 2: Equipo
        asesoria = AsesoriaEspecializada(  # Servicio 3: Asesoría especializada
            "SRV-ASE-1", "Arquitectura de Software", 80000.0, especialista="Ing. Mateo Pérez", disponible=True
        )
        for srv in (sala, equipo, asesoria):  # Registra todos los servicios en el gestor
            gestor.registrar_servicio(srv)
            servicios_creados[srv.id_entidad] = srv
        return f"Registrados {len(gestor.servicios)} servicios especializados."

    # Simulación 5: Creación inválida de servicio por tarifa base negativa
    def sim_05() -> str:
        servicio_invalido = ReservaSala("SRV-SALA-2", "Sala Audit", -15000.0, capacidad=8)  # Tarifa inválida <= 0
        gestor.registrar_servicio(servicio_invalido)  # No se ejecuta si falla antes
        return "No debería llegar aquí"

    # Simulación 6: Reserva válida de sala, confirmación y procesamiento con descuento e impuesto
    def sim_06() -> str:
        cliente = clientes_creados["CLI-01"]  # Obtiene cliente registrado
        sala = servicios_creados["SRV-SALA-1"]  # Obtiene sala disponible
        reserva = Reserva("RES-01", cliente, sala, duracion_horas=3.0, cantidad_o_asistentes=8)  # Crea reserva válida
        gestor.crear_reserva(reserva)  # Añade reserva a la lista interna
        reserva.confirmar()  # Confirma la reserva
        total = reserva.procesar(descuento_pct=0.10, impuesto_pct=0.19)  # Procesa con 10% dto. e IVA 19%
        reservas_creadas["RES-01"] = reserva  # Guarda referencia
        return f"Reserva RES-01 procesada por ${total} | Estado: {reserva.estado}"

    # Simulación 7: Reserva inválida por exceder capacidad máxima de la sala
    def sim_07() -> str:
        cliente = clientes_creados["CLI-01"]  # Obtiene cliente
        sala = servicios_creados["SRV-SALA-1"]  # Sala con capacidad máxima de 12 personas
        reserva_exceso = Reserva("RES-02", cliente, sala, duracion_horas=2.0, cantidad_o_asistentes=20)  # 20 > 12
        gestor.crear_reserva(reserva_exceso)  # No se ejecuta por excepción previa
        return "No debería llegar aquí"

    # Simulación 8: Reserva fallida por servicio no disponible
    def sim_08() -> str:
        equipo_ocupado = AlquilerEquipo("SRV-EQ-2", "Proyector 4K", 25000.0, stock=2, disponible=False)  # No disponible
        gestor.registrar_servicio(equipo_ocupado)  # Registra el servicio no disponible
        reserva_no_disp = Reserva("RES-03", clientes_creados["CLI-01"], equipo_ocupado, duracion_horas=4.0, cantidad_o_asistentes=1)
        gestor.crear_reserva(reserva_no_disp)  # No se ejecuta porque verificar_disponibilidad falla
        return "No debería llegar aquí"

    # Simulación 9: Intento de procesar una reserva sin haberla confirmado primero
    def sim_09() -> str:
        asesoria = servicios_creados["SRV-ASE-1"]  # Obtiene asesoría disponible
        reserva_pendiente = Reserva("RES-04", clientes_creados["CLI-01"], asesoria, duracion_horas=2.0)  # Queda PENDIENTE
        gestor.crear_reserva(reserva_pendiente)  # Registra reserva pendiente
        reserva_pendiente.procesar()  # Debe fallar porque no está CONFIRMADA
        return "No debería llegar aquí"

    # Simulación 10: Cancelación válida de reserva y posterior intento inválido de confirmarla
    def sim_10() -> str:
        equipo = servicios_creados["SRV-EQ-1"]  # Obtiene servicio de alquiler de equipos
        reserva_cancel = Reserva("RES-05", clientes_creados["CLI-01"], equipo, duracion_horas=5.0, cantidad_o_asistentes=2)
        gestor.crear_reserva(reserva_cancel)  # Registra reserva
        reserva_cancel.cancelar()  # Cancela la reserva válidamente
        reserva_cancel.confirmar()  # Intento inválido de confirmar una reserva ya cancelada
        return "No debería llegar aquí"

    # Simulación 11: Cálculo inconsistente de descuento fuera de rango
    def sim_11() -> str:
        asesoria = servicios_creados["SRV-ASE-1"]  # Obtiene asesoría
        asesoria.calcular_costo(duracion_horas=2.0, descuento_pct=1.5)  # Descuento del 150% es inválido
        return "No debería llegar aquí"

    # Simulación 12: Encadenamiento de excepción ante error inesperado (ZeroDivisionError)
    def sim_12() -> str:
        _ = 100 / 0  # Provoca ZeroDivisionError para demostrar encadenamiento 'raise ... from exc'
        return "No debería llegar aquí"

    simulaciones = [  # Lista ordenada de las 12 simulaciones a ejecutar secuencialmente
        (1, "Registro válido de cliente", sim_01),
        (2, "Registro inválido de cliente por correo", sim_02),
        (3, "Registro inválido de cliente por documento", sim_03),
        (4, "Creación válida de sala, equipo y asesoría", sim_04),
        (5, "Creación inválida de servicio con tarifa negativa", sim_05),
        (6, "Reserva válida, confirmación y procesamiento con sobrecarga", sim_06),
        (7, "Reserva inválida por exceso de capacidad de sala", sim_07),
        (8, "Reserva fallida por servicio no disponible", sim_08),
        (9, "Procesamiento inválido de reserva en estado PENDIENTE", sim_09),
        (10, "Cancelación válida y reconfirmación inválida de reserva", sim_10),
        (11, "Cálculo financiero inconsistente por descuento inválido", sim_11),
        (12, "Encadenamiento de excepción ante error inesperado", sim_12),
    ]

    for num, titulo, fn in simulaciones:  # Ejecuta todas las simulaciones una tras otra sin detenerse
        ejecutar_simulacion(num, titulo, fn)

    logger.info(  # Resumen final en el log confirmando estado de colecciones sin base de datos
        f"Resumen final en memoria -> Clientes: {len(gestor.clientes)} | "
        f"Servicios: {len(gestor.servicios)} | Reservas: {len(gestor.reservas)}"
    )


if __name__ == "__main__":  # Permite ejecutar este archivo directamente desde terminal o IDE
    correr_simulaciones()  # Inicia la ejecución secuencial de las simulaciones