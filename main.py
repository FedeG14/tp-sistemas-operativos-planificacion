"""
Simulador de Planificación de Procesos - Sistemas Operativos
Opción 1: FCFS y SJF no expropiativo.

Ejecutar con:
    python main.py
No requiere instalar bibliotecas externas.
"""

from dataclasses import dataclass
from enum import Enum


class Estado(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    TERMINATED = "TERMINATED"


@dataclass
class PCB:
    """Process Control Block: información administrativa de un proceso."""
    pid: int
    nombre: str
    prioridad: int
    llegada: int
    rafaga: int
    estado: Estado = Estado.READY
    inicio: int = 0
    finalizacion: int = 0
    espera: int = 0
    retorno: int = 0


def crear_procesos():
    """Conjunto de procesos de prueba. Los tiempos son unidades simuladas."""
    return [
        PCB(1, "Proceso_A", 2, 0, 7),
        PCB(2, "Proceso_B", 1, 2, 4),
        PCB(3, "Proceso_C", 3, 4, 1),
        PCB(4, "Proceso_D", 2, 5, 4),
        PCB(5, "Proceso_E", 1, 6, 2),
    ]


def planificar(procesos, algoritmo):
    """
    Simula un algoritmo de planificación.
    FCFS: orden de llegada.
    SJF: menor ráfaga entre los procesos que ya llegaron.
    """
    pendientes = [PCB(p.pid, p.nombre, p.prioridad, p.llegada, p.rafaga)
                  for p in procesos]
    tiempo = 0
    gantt = []
    orden = []

    while pendientes:
        disponibles = [p for p in pendientes if p.llegada <= tiempo]

        if not disponibles:
            proxima_llegada = min(p.llegada for p in pendientes)
            gantt.append(("INACTIVO", tiempo, proxima_llegada))
            tiempo = proxima_llegada
            disponibles = [p for p in pendientes if p.llegada <= tiempo]

        if algoritmo == "FCFS":
            proceso = min(disponibles, key=lambda p: (p.llegada, p.pid))
        elif algoritmo == "SJF":
            proceso = min(disponibles, key=lambda p: (p.rafaga, p.llegada, p.pid))
        else:
            raise ValueError("Algoritmo no reconocido")

        proceso.estado = Estado.RUNNING
        proceso.inicio = tiempo
        proceso.espera = proceso.inicio - proceso.llegada
        tiempo += proceso.rafaga
        proceso.finalizacion = tiempo
        proceso.retorno = proceso.finalizacion - proceso.llegada
        proceso.estado = Estado.TERMINATED

        gantt.append((proceso.nombre, proceso.inicio, proceso.finalizacion))
        orden.append(proceso.nombre)
        pendientes.remove(proceso)

    return gantt, orden, sorted(
        [PCB(p.pid, p.nombre, p.prioridad, p.llegada, p.rafaga,
             Estado.TERMINATED, p.inicio, p.finalizacion, p.espera, p.retorno)
         for p in []],
        key=lambda p: p.pid
    ), tiempo


def ejecutar(algoritmo, procesos):
    """Versión que conserva y devuelve las métricas de cada PCB."""
    pendientes = [PCB(p.pid, p.nombre, p.prioridad, p.llegada, p.rafaga)
                  for p in procesos]
    terminados = []
    tiempo = 0
    gantt = []
    orden = []

    while pendientes:
        disponibles = [p for p in pendientes if p.llegada <= tiempo]

        if not disponibles:
            proxima_llegada = min(p.llegada for p in pendientes)
            gantt.append(("INACTIVO", tiempo, proxima_llegada))
            tiempo = proxima_llegada
            disponibles = [p for p in pendientes if p.llegada <= tiempo]

        if algoritmo == "FCFS":
            proceso = min(disponibles, key=lambda p: (p.llegada, p.pid))
        else:  # SJF no expropiativo
            proceso = min(disponibles, key=lambda p: (p.rafaga, p.llegada, p.pid))

        proceso.estado = Estado.RUNNING
        proceso.inicio = tiempo
        proceso.espera = tiempo - proceso.llegada
        tiempo += proceso.rafaga
        proceso.finalizacion = tiempo
        proceso.retorno = tiempo - proceso.llegada
        proceso.estado = Estado.TERMINATED

        gantt.append((proceso.nombre, proceso.inicio, proceso.finalizacion))
        orden.append(proceso.nombre)
        terminados.append(proceso)
        pendientes.remove(proceso)

    return gantt, orden, terminados


def imprimir_gantt(gantt):
    print("\nDiagrama de Gantt:")
    print(" | ".join(f"{nombre} [{inicio}-{fin}]"
                     for nombre, inicio, fin in gantt))


def imprimir_resultados(algoritmo, gantt, orden, procesos):
    promedio_espera = sum(p.espera for p in procesos) / len(procesos)
    promedio_retorno = sum(p.retorno for p in procesos) / len(procesos)

    print("\n" + "=" * 72)
    print(f"ALGORITMO: {algoritmo}")
    print("=" * 72)
    print(f"{'PID':<6}{'Proceso':<14}{'Llegada':>9}{'Ráfaga':>9}"
          f"{'Espera':>9}{'Retorno':>10}{'Estado':>14}")
    for p in sorted(procesos, key=lambda x: x.pid):
        print(f"{p.pid:<6}{p.nombre:<14}{p.llegada:>9}{p.rafaga:>9}"
              f"{p.espera:>9}{p.retorno:>10}{p.estado.value:>14}")

    imprimir_gantt(gantt)
    print("Orden de despacho:", " -> ".join(orden))
    print(f"Tiempo de espera promedio: {promedio_espera:.2f}")
    print(f"Tiempo de retorno promedio: {promedio_retorno:.2f}")


def main():
    procesos = crear_procesos()

    print("SIMULADOR DE PLANIFICACIÓN DE PROCESOS")
    print("Procesos de entrada:")
    print(f"{'PID':<6}{'Proceso':<14}{'Prioridad':>12}"
          f"{'Llegada':>10}{'Ráfaga':>10}")
    for p in procesos:
        print(f"{p.pid:<6}{p.nombre:<14}{p.prioridad:>12}"
              f"{p.llegada:>10}{p.rafaga:>10}")

    resultados = {}
    for algoritmo in ("FCFS", "SJF"):
        gantt, orden, terminados = ejecutar(algoritmo, procesos)
        imprimir_resultados(algoritmo, gantt, orden, terminados)
        resultados[algoritmo] = terminados

    print("\n" + "=" * 72)
    print("COMPARACIÓN FINAL")
    print("=" * 72)
    print(f"{'Algoritmo':<12}{'Espera promedio':>20}{'Retorno promedio':>22}")
    for algoritmo, procesos_finales in resultados.items():
        espera = sum(p.espera for p in procesos_finales) / len(procesos_finales)
        retorno = sum(p.retorno for p in procesos_finales) / len(procesos_finales)
        print(f"{algoritmo:<12}{espera:>20.2f}{retorno:>22.2f}")

    print("\nSimulación finalizada correctamente.")


if __name__ == "__main__":
    main()
