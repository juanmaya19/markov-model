import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Definir los estados del SGR
estados = ['Solicitud Enviada (SE)', 'En Revisión (ER)', 'Aprobada (AP)', 'Desembolso (DE)', 'Seguimiento (SG)']

# Definir la matriz de transición
matriz_transicion = np.array([
    [0.2, 0.8, 0.0, 0.0, 0.0],  # Probabilidades de transición desde 'Solicitud Enviada (SE)'
    [0.3, 0.1, 0.6, 0.0, 0.0],  # Probabilidades de transición desde 'En Revisión (ER)'
    [0.0, 0.0, 0.1, 0.9, 0.0],  # Probabilidades de transición desde 'Aprobada (AP)'
    [0.0, 0.0, 0.0, 0.3, 0.7],  # Probabilidades de transición desde 'Desembolso (DE)'
    [0.0, 0.0, 0.0, 0.0, 1.0]   # Probabilidades de transición desde 'Seguimiento (SG)'
])

def validar_matriz_transicion(matriz):
    """Valida que la matriz de transición sea válida."""
    if not np.allclose(matriz.sum(axis=1), 1):
        raise ValueError("Las filas de la matriz de transición deben sumar 1.")

    if np.any(matriz < 0) or np.any(matriz > 1):
        raise ValueError("Los valores de la matriz de transición deben estar entre 0 y 1.")

def simular_proceso_markov(estados, matriz_transicion, estado_inicial, num_iteraciones):
    """Simula el proceso de Markov."""
    historial_estados = [estado_inicial]
    estado_actual = estado_inicial

    for _ in range(num_iteraciones - 1):
        estado_actual_index = estados.index(estado_actual)
        siguiente_estado = np.random.choice(estados, p=matriz_transicion[estado_actual_index])
        historial_estados.append(siguiente_estado)
        estado_actual = siguiente_estado

    return historial_estados

def analizar_resultados_multiple_simulacion(historiales_estados):
    """Analiza los resultados de múltiples simulaciones."""
    conteo_total_estados = Counter()

    for historial in historiales_estados:
        conteo_total_estados.update(historial)

    total_iteraciones = sum(conteo_total_estados.values())
    frecuencias = {estado: conteo / total_iteraciones for estado, conteo in conteo_total_estados.items()}
    tiempos_promedio = {estado: total_iteraciones / conteo for estado, conteo in conteo_total_estados.items()}

    return frecuencias, tiempos_promedio

def graficar_historial_multiple_simulacion(historiales_estados, estados, tiempos_promedio):
    """Grafica el historial de estados y el tiempo promedio por estado."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)  # Subplots para las dos gráficas

    # Graficar historial de estados
    for i, historial in enumerate(historiales_estados):
        indices_estados = [estados.index(estado) for estado in historial]
        ax1.plot(indices_estados, marker='o', linestyle='-', alpha=0.5, label=f'Simulación {i+1}')

    ax1.set_yticks(range(len(estados)))
    ax1.set_yticklabels(estados)
    ax1.set_xlabel('Iteraciones')
    ax1.set_ylabel('Estados')
    ax1.set_title('Historial de Estados del SGR en Múltiples Simulaciones')
    ax1.legend(loc='best')
    ax1.grid(True)

    # Graficar tiempo promedio por estado
    ax2.barh(list(tiempos_promedio.keys()), list(tiempos_promedio.values()), color='skyblue')
    ax2.set_xlabel('Tiempo Promedio')
    ax2.set_title('Tiempo Promedio en Cada Estado')
    ax2.grid(True)

    plt.tight_layout()  # Ajustar el diseño de la figura
    plt.show()

# Ejemplo de uso
num_iteraciones = 20  # Número de iteraciones por simulación
num_simulaciones = 4   # Número de simulaciones
estado_inicial = 'Solicitud Enviada (SE)'

# Validar la matriz de transición
validar_matriz_transicion(matriz_transicion)

# Simular múltiples procesos de Markov
historiales_estados = [simular_proceso_markov(estados, matriz_transicion, estado_inicial, num_iteraciones) for _ in range(num_simulaciones)]

# Analizar los resultados
frecuencias, tiempos_promedio = analizar_resultados_multiple_simulacion(historiales_estados)

# Mostrar resultados
print("\nFrecuencias de los estados (promedio en múltiples simulaciones):")
for estado, frecuencia in frecuencias.items():
    print(f"{estado}: {frecuencia:.2f}")

print("\nTiempo promedio en cada estado (promedio en múltiples simulaciones):")
for estado, tiempo in tiempos_promedio.items():
    print(f"{estado}: {tiempo:.2f}")

# Graficar el historial de estados y el tiempo promedio por estado
graficar_historial_multiple_simulacion(historiales_estados, estados, tiempos_promedio)
