# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para la **Fase 4 (Componente práctico - Prácticas simuladas)** del curso **Programación (Código: 213023)** de la Universidad Nacional Abierta y a Distancia (**UNAD**) — Escuela de Ciencias Básicas, Tecnología e Ingeniería (**ECBTI**).

## Descripción General

El sistema modela una aplicación modular y estable en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)** para la empresa **Software FJ**, encargada de ofrecer servicios de reserva de salas, alquiler de equipos y asesorías especializadas.

Toda la gestión de información se realiza **en memoria mediante objetos y listas internas**, sin utilizar ningún motor de base de datos, empleando archivos únicamente para el registro continuo de eventos y errores (`logs/sistema_software_fj.log`).

---

## Estructura del Repositorio

```text
software-fj-fase4/
├── exceptions.py        # Jerarquía de excepciones personalizadas del dominio
├── models.py            # Clases abstractas, encapsulación, polimorfismo, sobrecarga y gestor en memoria
├── logger_config.py     # Configuración del sistema de logging en archivo y consola
├── simulaciones.py      # Ejecución secuencial de 12 simulaciones (válidas e inválidas)
├── logs/                # Carpeta generada automáticamente con el archivo de logs
├── .gitignore           # Exclusión de archivos temporales de Python
└── README.md            # Documentación general del proyecto
