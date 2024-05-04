import random
import json
import os
from inicializacion import CreatePopulation
from metodoSeleccion import Operadores

best_cromosoma = []

def programa_evolutivo(semestre,n_poblacion,n_epochs,mutation_percentage):
    # Obtener la ruta del directorio actual del script
    directorio_script = os.path.dirname(os.path.abspath(__file__))

    # OBTENER ARCHIVO DE CLASES
    if semestre == 1:
        ruta_json = os.path.join(directorio_script, '..', 'Json', 'clases_agos_dic.json')
        with open(ruta_json) as clases_json:
            clases = json.load(clases_json)
    elif semestre == 2:
        ruta_json = os.path.join(directorio_script, '..', 'Json', 'clases_feb_jun.json')
        with open(ruta_json) as clases_json:
            clases = json.load(clases_json)
    else:
        print("Semestre inválido. Por favor, seleccione 1 para Ago-Dic o 2 para Feb-Jun.")
        return

    # OBTENER ARCHIVO DE PROFESORES
    ruta_json = os.path.join(directorio_script, '..', 'Json', 'profesores.json')
    with open(ruta_json) as profesores_json:
        profesoresJson = json.load(profesores_json)

    # Funciones de costos y restricciones...

    # Funciones generales
    def setRestriccionLeve():
        incremento = random.uniform(1, 2)
        return incremento

    def setRestriccionFuerte():
        incremento = random.uniform(12.1, 15)
        return incremento

    profesoresLocal = {}
    def llenarProfesoresLocal(gen):
        idProfesor = gen.id_profesor
        horasMateria = gen.n_horas

        if idProfesor in profesoresLocal:
            profesoresLocal[idProfesor] += horasMateria
        else:
            profesoresLocal[idProfesor] = horasMateria

    # Funciones para restricciones
    def fuerteRevisarProfesores(gen):
        profesorGen = gen.id_profesor
        materiaGen = gen.id_materia
        existe = False
        for materia, valor in clases.items():
            if materia == materiaGen:
                profesorJson = valor['profesores']
                for profesor in profesorJson:
                    if profesorGen == profesor['nomina']:
                        existe = True
                        break
        if not existe:
            return setRestriccionFuerte()
        else:
            return 0
        
    def fuerteLeveRelacionModulo(gen):
        profesorGen = gen.id_profesor
        materiaGen = gen.id_materia
        moduloGen= gen.m_materia
        coincide = False
        for materia, valor in clases.items():
            if materia == materiaGen:
                profesorJson = valor['profesores']
                for profesor in profesorJson:
                    if profesorGen == profesor['nomina']:
                        for modulo in profesor['modulos']:
                            if moduloGen == modulo:
                                coincide = True
        if not coincide:
            return setRestriccionFuerte()
        else:
            return 0
        
    def fuerteNoColisionHorarios(cromosoma):
        for gen in cromosoma:
            for gen_check in cromosoma:
                if gen == gen_check: pass
                else:
                    for hora in gen.horario:
                        for hora_check in gen_check.horario:
                            if hora == hora_check: pass
                            else:
                                if hora[0] == hora_check[0] and hora[1] == hora_check[1]:
                                    return setRestriccionFuerte()
        return 0
        
    def fuerteFranjaNoClase(gen):
        for horario in gen.horario:
            # Si el horario está en la franja de no clase de 13 a 15, penalizar
            if horario[1] >= 13.0 and horario[1] < 15.0:
                return setRestriccionFuerte()
        # Si no, no penalizar
        return 0

    def fuerteMateriasHorasDiarias(cromosoma):
        # Como estamos evaluando materias en una semana, tenemos que considerar todo el cromosoma

        penalizacion = 0

        # Se creara un arreglo para no volver a comprobar materias que ya se han revisado
        bloques_revisados = []

        # Revisamos que exista en algun gen del cromosoma alguna materia que sea bloque
        for gen in cromosoma:

            # Checar si la materia del gen está en el json y NO es bloque
            if clases[gen.id_materia]['tipo'] == 0 and gen.id_materia not in bloques_revisados:

                # Se guarda la materia que se va a recorrer
                materia_seleccionada = gen.id_materia
                bloques_revisados.append(gen.id_materia)

                # Inicializamos una diccionario de los dias en los que se imparten clases
                dias_horario = {'lunes': [], 'martes': [], 'miercoles': [], 'jueves': [], 'viernes': []}

                # Recorrer cromosoma para encontrar la materia en cada gen
                for gen_check in cromosoma:

                    # Checar que la materia del gen sea la misma que se selecciono
                    if gen_check.id_materia == materia_seleccionada:

                        # Si lo es, poblar horarios de cada gen que tenga ese bloque
                        for horario in gen_check.horario:
                            dias_horario[horario[0]].append(horario[2])

                if sum(isinstance(i, list) for i in gen_check.horario) > 1:

                    # Revisar dias pares lunes-jueves
                    if (len(dias_horario['lunes']) >= 1 and len(dias_horario['jueves']) >= 1):
                        if (len(dias_horario['martes']) == 0 and len(dias_horario['viernes']) == 0):
                            pass
                        else:
                            #print('penalizacion por dias impares: ', dias_horario)
                            penalizacion += setRestriccionFuerte()
                    # Revisar dias pares martes-viernes
                    elif (len(dias_horario['martes']) >= 1 and len(dias_horario['viernes']) >= 1):
                        if (len(dias_horario['lunes']) == 0 and len(dias_horario['jueves']) == 0):
                            pass
                        else:
                            #print('penalizacion por dias impares: ', dias_horario)
                            penalizacion += setRestriccionFuerte()

                    # Se compara si hay más de 2 horas en un dia
                    for horas_fin in dias_horario.values():
                        if len(horas_fin) > 1:
                            #print('penalizacion por mas de 2 horas en un dia: ', dias_horario)
                            penalizacion += setRestriccionFuerte()
                            break

        # Regresar penalizaciones
        return penalizacion

    def leveRevisarMiercoles(gen):
        for horario in gen.horario:
            if horario[0] == 'miercoles':
                # Si se encuentra 'miércoles' en el horario, devolver un incremento aleatorio entre 1 y 2
                return setRestriccionLeve()
        # Si no se encuentra 'miércoles' en el horario, devolver 0
        return 0

    def leveRevisarSiete(gen):
        for materia, valor in clases.items():
            if materia == gen.id_materia:
                # En caso de que una materia del primero a quinto semestre empiece después de las 7 se penalizará
                if valor['semestre'] < 5:
                    for horario in gen.horario:
                        horas = horario[1]
                        if horas >= 19:
                            return setRestriccionLeve()
                        else:
                            return 0
                else:
                    return 0
            else:
                return 0

    def leveBloquesContinuos(cromosoma):
        # Como estamos evaluando bloques, tenemos que considerar todo el cromosoma

        penalizacion = 0

        # Se creara un arreglo para no volver a comprobar materias que ya se han revisado
        bloques_revisados = []

        # Revisamos que exista en algun gen del cromosoma alguna materia que sea bloque
        for gen in cromosoma:

        # Comparar si la materia es un bloque

            # Checar si la materia del gen está en el json y si es bloque
            if clases[gen.id_materia]['tipo'] == 1 and gen.id_materia not in bloques_revisados:

                # Booleano para revisar cuando se genera una penalizacion
                triggered = False

                # Se guarda la materia que se va a recorrer
                materia_seleccionada = gen.id_materia
                bloques_revisados.append(gen.id_materia)

                # Inicializamos una diccionario de los dias en los que se imparten clases
                dias_horario = {'lunes': [], 'martes': [], 'miercoles': [], 'jueves': [], 'viernes': []}

                # Recorrer cromosoma para encontrar la materia en cada gen
                for gen_check in cromosoma:

                    # Checar que la materia del gen sea la misma que se selecciono
                    if gen_check.id_materia == materia_seleccionada:

                        # Si lo es, poblar horarios de cada gen que tenga ese bloque
                        for horario in gen_check.horario:
                            dias_horario[horario[0]].append(horario[2])

                        # Se ordenan los valores de menor a mayor
                        dias_horario = {key: sorted(value) for key, value in dias_horario.items()}

                # Se compara si hay un espacio de más de 2 horas por bloque, 
                # lo que significaria que hay tiempo muerto enntre el bloque
                for horas_fin in dias_horario.values():

                    # Si se llega a penalizar debido a cierto bloque, cambiar de gen
                    if triggered: break

                    for hora in horas_fin[:-1]:
                        if len(horas_fin) > 1:
                            difference =  horas_fin[-1] - hora

                            # Si ese espacio existe, inmediatamente se penaliza al cromosoma
                            if difference > 2.0:

                                # Ir sumando las penalizaciones de bloques
                                penalizacion += setRestriccionLeve()
                                triggered = True
                                break

        # Regresar penalizaciones
        return penalizacion

    def fuerteRevisarPares(gen):
        penalizacion = 0
        for horario in gen.horario:
            hora_inicio = horario[1]
            if hora_inicio % 2 == 0:  # Si la hora de inicio es par
                penalizacion += setRestriccionFuerte()
        return penalizacion

    def leveCargaPlantaCatedra():
        if len(profesoresMaxUpLlenos) != 2:
            return setRestriccionLeve()
        else:
            return 0

    def fuerteCargaCompleta():
        for id_profesor, horas in profesoresLocal.items():
            detalles_profesor = profesoresJson.get(id_profesor)
            if detalles_profesor:
                max_up = detalles_profesor.get('max_up', 0) * 20
                if horas > max_up:
                    return setRestriccionFuerte()
                elif horas == max_up and detalles_profesor.get('planta', ''):
                    profesoresMaxUpLlenos.append(id_profesor)
                else:
                    return 0
          

    # Inicializacion de variables
    num_poblacion = n_poblacion
    poblacion = []
    poblacion_inicial = []
    profesoresMaxUpLlenos = []

    epochs = n_epochs
    time = 0

    crearPoblacion = CreatePopulation()
    operadores = Operadores()

    # Crear los poblacion inicial
    for i in range(num_poblacion):
        if semestre == 1:
            poblacion.append(crearPoblacion.GetCromosomaAgoDic())
        elif semestre == 2:
            poblacion.append(crearPoblacion.GetCromosomaFebJun())

    # Validación Inicial
    for cromosoma in poblacion:
        cromosoma.leves_score = 0
        cromosoma.graves_score = 0
        profesoresLocal = {}
        profesoresMaxUpLlenos = []
        for gen in cromosoma.GetGenes():
            # Checar restricciones y actualizar puntajes
            cromosoma.AddLevesScore(leveRevisarMiercoles(gen))
            cromosoma.AddLevesScore(leveRevisarSiete(gen))
            cromosoma.AddGravesScore(fuerteRevisarProfesores(gen))
            cromosoma.AddGravesScore(fuerteFranjaNoClase(gen))
            cromosoma.AddGravesScore(fuerteLeveRelacionModulo(gen))
            cromosoma.AddGravesScore(fuerteRevisarPares(gen))
            llenarProfesoresLocal(gen)

        cromosoma.AddGravesScore(fuerteMateriasHorasDiarias(cromosoma.GetGenes()))
        cromosoma.AddLevesScore(leveBloquesContinuos(cromosoma.GetGenes()))
        cromosoma.AddGravesScore(fuerteNoColisionHorarios(cromosoma.GetGenes()))
        cromosoma.AddGravesScore(fuerteCargaCompleta())

    poblacion_inicial = sorted(poblacion, key=lambda x: x.GetTotalScore())

    elite_size = 10  # Número de individuos de élite a mantener en cada generación
    mutation_rate = mutation_percentage

    print("Mejor puntaje poblacion inicial: " + str(poblacion_inicial[0].GetTotalScore()))

    # Evolucion
    best_score = float('inf')  # Variable para almacenar el mejor cromosoma

    while time < epochs:
        # Reiniciar variables para la nueva población
        poblacion_nueva = []
        num_nueva_poblacion = 0 
        # Selección y operadores genéticos
        for i in range(num_poblacion - elite_size):
            x = random.random()

            if x < mutation_rate:
                # Mutación
                parent = operadores.seleccion_ruleta(poblacion, 1)[0]
                child = operadores.mutacion(parent)
                poblacion_nueva.append(child)
                num_nueva_poblacion += 1
            else:
                # Cruce
                parents = operadores.seleccion_ruleta(poblacion, 2)
                n = random.randint(0, 9)
                child1, child2 = operadores.crossover(parents[0], parents[1], n)
                poblacion_nueva.append(child1)
                poblacion_nueva.append(child2)
                num_nueva_poblacion += 2

        # Evaluación de la nueva población
        for cromosoma in poblacion_nueva:
            cromosoma.leves_score = 0
            cromosoma.graves_score = 0
            profesoresLocal = {}
            profesoresMaxUpLlenos = []
            for gen in cromosoma.GetGenes():
                # Checar restricciones y actualizar puntajes
                cromosoma.AddLevesScore(leveRevisarMiercoles(gen))
                cromosoma.AddLevesScore(leveRevisarSiete(gen))
                cromosoma.AddGravesScore(fuerteRevisarProfesores(gen))
                cromosoma.AddGravesScore(fuerteFranjaNoClase(gen))
                cromosoma.AddGravesScore(fuerteLeveRelacionModulo(gen))
                cromosoma.AddGravesScore(fuerteRevisarPares(gen))
                llenarProfesoresLocal(gen)

            cromosoma.AddGravesScore(fuerteMateriasHorasDiarias(cromosoma.GetGenes()))
            cromosoma.AddLevesScore(leveBloquesContinuos(cromosoma.GetGenes()))
            cromosoma.AddGravesScore(fuerteNoColisionHorarios(cromosoma.GetGenes()))
            cromosoma.AddGravesScore(fuerteCargaCompleta())

        # Estrategia de reemplazo generacional
        poblacion_combinada = poblacion + poblacion_nueva
        poblacion_ordenada = sorted(poblacion_combinada, key=lambda x: x.GetTotalScore())
        poblacion = poblacion_ordenada[:num_poblacion]
        
        current_best_score = poblacion[0]

        if current_best_score.GetTotalScore() < best_score:
             # Guardar el mejor cromosoma
            best_score = current_best_score.GetTotalScore()
            best_cromosoma.append(current_best_score)
        
        print("Epoch: " + str(time))
        print("Mejor puntaje en poblacion actual: " + str(current_best_score.GetTotalScore()))
                
        time += 1

    # Llama a esta función después de tu bucle de evolución para realizar la verificación
    print("Puntaje final: ")
    print(best_score)

# Pedir al usuario

semestre = int(input("Seleccione el semestre (1 para Ago-Dic, 2 para Feb-Jun): "))
n_p = int(input("De cuantos elementos quiere la poblacion inicial: "))
n_e = int(input("Cuantos epochs quiere para la evolucion: "))
per_m = float(input("Con que porcentaje quiere realizar la mutacion (valor entr 0.0 y 1.0): "))

# Ejecutar el programa evolutivo para el semestre seleccionado
programa_evolutivo(semestre,n_p,n_e,per_m)
