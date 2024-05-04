from Cromosoma import Cromosoma
import random
import bisect

class Operadores:
# METODO DE SELECCION
    def seleccion_ruleta(self,poblacion, n):
        fitness = [cromosoma.GetTotalScore() for cromosoma in poblacion]
        suma_aptitudes = sum(fitness)
        probabilidades = [aptitud / suma_aptitudes for aptitud in fitness]
        
        # Crea la ruleta ponderada acumulando las probabilidades
        ruleta = []
        acumulador = 0
        for probabilidad in probabilidades:
            acumulador += probabilidad
            ruleta.append(acumulador)
        
        seleccionados = []
        for _ in range(n):
            r = random.random()
            # Encuentra el cromosoma correspondiente en la ruleta
            idx = bisect.bisect_right(ruleta, r)
            seleccionados.append(poblacion[idx])
        
        return seleccionados

    # OPERADOR GENETICO DE CRUCE
    def crossover(self, parent1, parent2, n):
        # Limitar n a un valor máximo igual a la longitud del cromosoma menos 1
        n = min(n, len(parent1.GetGenes()) - 1)
        # Seleccionar puntos de cruce aleatorios
        crossover_points = sorted(random.sample(range(len(parent1.GetGenes()) - 1), n))
        child1 = []
        child2 = []

        # Iterar sobre los puntos de cruce
        start = 0
        for point in crossover_points:
            # Agregar secciones de parent1 a child1 y parent2 a child2
            child1 += parent1.GetGenes()[start:point+1]
            child2 += parent2.GetGenes()[start:point+1]
            # Actualizar el inicio de la siguiente sección
            start = point + 1

        # Agregar las secciones restantes
        child1 += parent2.GetGenes()[start:]
        child2 += parent1.GetGenes()[start:]

        return Cromosoma(child1), Cromosoma(child2)

    # OPERADOR GENETICO DE MUTACION
    def mutacion(self,parent1):

        x = random.randint(0,len(parent1.genes) - 1)
        child1 = parent1.genes[x]
        child1.Mutar()

        cromosoma = parent1
        cromosoma.genes[x] = child1

        return cromosoma
        
