import time
import pandas as pd
import matplotlib.pyplot as plt
from AStar_Algorithm import AStar_Algorithm

algorithm = AStar_Algorithm()

start_time = time.time()  # Captura el tiempo inicial
algorithm.A_Star()  # Ejecuta el algoritmo
end_time = time.time()  # Captura el tiempo final

execution_time = end_time - start_time  # Calcula el tiempo de ejecución

def print_execution_time(execution_time):
  if execution_time >= 3600:
      hours = int(execution_time // 3600)
      minutes = int((execution_time % 3600) // 60)
      seconds = execution_time % 60
      print(f"El tiempo de ejecución del algoritmo es: {hours} horas, {minutes} minutos y {seconds:.6f} segundos")
  elif execution_time >= 60:
      minutes = int(execution_time // 60)
      seconds = execution_time % 60
      print(f"El tiempo de ejecución del algoritmo es: {minutes} minutos y {seconds:.6f} segundos")
  else:
      print(f"El tiempo de ejecución del algoritmo es: {execution_time:.6f} segundos")

def display_graph():
  # Para guardar los resutados
  execution_time = 0
  results = []

  for i in range(30):
      algorithm = AStar_Algorithm()

      start_time = time.time()  # Captura el tiempo inicial
      algorithm.A_Star(False)  # Ejecuta el algoritmo
      end_time = time.time()  # Captura el tiempo final

      execution_time = end_time - start_time  # Calcula el tiempo de ejecución

      # Almacenar los resultados en una lista de diccionarios
      results.append({
          'execution_time': execution_time,
      })

  # Convertir la lista de resultados a un DataFrame de pandas
  df = pd.DataFrame(results)

  # Generar un gráfico de tiempo de ejecución
  plt.figure(figsize=(10, 5))
  plt.plot(df.index, df['execution_time'], marker='o', linestyle='-', color='b')
  plt.title('Tiempo de Ejecución del Algoritmo A*')
  plt.xlabel('Número de ejecuciones')
  plt.ylabel('Tiempo de Ejecución (segundos)')
  plt.grid(True)
  plt.show()

print_execution_time(execution_time)
print("--------------------------------")
# display_graph()
