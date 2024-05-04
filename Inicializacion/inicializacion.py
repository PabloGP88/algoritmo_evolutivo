import json
import random
import math
from Gen import Gen
from Cromosoma import Cromosoma

class CreatePopulation:

    def generate_horario(profesor, tipo, n_horas, periodos):
        # Inicializa una lista vacía para almacenar el horario generado.
        horario = []

        # Calcula el número de horas por semana que se deben asignar.
        # Se divide el número total de horas entre la cantidad de periodos disponibles y días hábiles en una semana.
        horas_por_semana = math.ceil(n_horas / (len(periodos) * 5))

        # Obtiene los días disponibles del profesor del diccionario proporcionado.
        dias_disponibles = profesor["dias"]
        # Determina el número de días seleccionados para asignar clases, dependiendo del tipo de horario.
        if tipo == 0:
            num_dias_seleccionados = min(2, len(dias_disponibles))
            if "miercoles" in dias_disponibles:
                dias_disponibles.remove("miercoles")
        else:
            num_dias_seleccionados = min(5, len(dias_disponibles))

        # Selecciona aleatoriamente los días en los que se asignarán clases.

        if tipo == 0:
            x = random.randint(0,1)
            if (x == 0):
                dias_seleccionados = ["lunes","jueves"]
            else:
                dias_seleccionados = ["martes","viernes"]
        else:
            dias_seleccionados = random.sample(dias_disponibles, num_dias_seleccionados)

        # Inicializa el contador de horas asignadas.
        horas_asignadas = 0

        # Mientras haya horas por asignar y días disponibles para asignar clases:
        while horas_asignadas < horas_por_semana and dias_seleccionados:
            # Selecciona aleatoriamente un día de la lista de días seleccionados.
            dia = random.choice(dias_seleccionados)
            dias_seleccionados.remove(dia)

            # Calcula una hora de inicio aleatoria dentro del horario del profesor.
            # Se elige una hora impar entre el inicio del horario del profesor y las 17:00.
            hora_inicio = random.choice(
                range(int(profesor["horario"][0]), min(19, int(profesor["horario"][1]) - 1), 2)
            )

            # Calcula la hora de finalización de la clase.
            # La hora de finalización es la hora de inicio más dos horas, o la hora de cierre del horario del profesor, lo que ocurra primero.
            if (horas_por_semana > 10):
                

                if ((horas_asignadas + 3) > horas_por_semana):

                    if ((horas_asignadas + 2) > horas_por_semana):
                        hora_fin = min(hora_inicio + 1, profesor["horario"][1])
                    else:
                        hora_fin = min(hora_inicio + 2, profesor["horario"][1])
                else:
                    hora_fin = min(hora_inicio + 3, profesor["horario"][1])
            
            else:
                if ((horas_asignadas + 2) > horas_por_semana):
                    hora_fin = min(hora_inicio + 1, profesor["horario"][1])
                else:
                    hora_fin = min(hora_inicio + 2, profesor["horario"][1])

                # Agrega la clase al horario generado como una lista que contiene el día, la hora de inicio y la hora de finalización.
            horario.append([dia, float(hora_inicio), float(hora_fin)])
                # Actualiza el contador de horas asignadas.
            horas_asignadas += hora_fin - hora_inicio

        return horario

    def GetCromosomaFebJun(self):
        # Load the JSON data
        with open("./Json/clases_feb_jun.json") as file:
            data = json.load(file)

        with open("./Json/profesores.json") as file:
            profesores_data = json.load(file)

        # Generate Gens for each key in the JSON
        gens = []
        for materia, info in data.items():
            num_modulos = info["num_modulos"]

            # Randomly select a professor from the list of professors
            profesores = info["profesores"]
            profesor = random.choice(profesores)
            id_profesor = profesor["nomina"]
            profesor_data = profesores_data[id_profesor]

            for _ in range(num_modulos):
                id_materia = materia
                g_materia = random.randint(1, info["grupos_max"])

                # Randomly select a module from the professor's available modules
                m_materia = random.choice(profesor["modulos"])
                pmt_materia = info["periodos"]
                pmt_profesor = pmt_materia
                n_horas = profesor["horas"][profesor["modulos"].index(m_materia)]

                # Generate the 'horario' attribute
                horario = CreatePopulation.generate_horario(profesor_data, info["tipo"], n_horas, pmt_materia)

                gen = Gen(
                    id_profesor,
                    id_materia,
                    g_materia,
                    m_materia,
                    pmt_materia,
                    horario,
                    pmt_profesor,
                    n_horas,
                )
                gens.append(gen)

        cromosoma = Cromosoma(gens)
        cromosoma.leves_score = 0
        cromosoma.graves_score = 0
        
        return cromosoma

    def GetCromosomaAgoDic(self):
        # Load the JSON data
        with open("./Json/clases_agos_dic.json") as file:
            data = json.load(file)

        with open("./Json/profesores.json") as file:
            profesores_data = json.load(file)

        # Generate Gens for each key in the JSON
        gens = []
        for materia, info in data.items():
            num_modulos = info["num_modulos"]

            # Randomly select a professor from the list of professors
            profesores = info["profesores"]
            profesor = random.choice(profesores)
            id_profesor = profesor["nomina"]
            profesor_data = profesores_data[id_profesor]

            for _ in range(num_modulos):
                id_materia = materia
                g_materia = random.randint(1, info["grupos_max"])

                # Randomly select a module from the professor's available modules
                m_materia = random.choice(profesor["modulos"])
                pmt_materia = info["periodos"]
                pmt_profesor = pmt_materia
                n_horas = profesor["horas"][profesor["modulos"].index(m_materia)]

                # Generate the 'horario' attribute
                horario = CreatePopulation.generate_horario(profesor_data, info["tipo"], n_horas, pmt_materia)

                gen = Gen(
                    id_profesor,
                    id_materia,
                    g_materia,
                    m_materia,
                    pmt_materia,
                    horario,
                    pmt_profesor,
                    n_horas,
                )
                gens.append(gen)

        cromosoma = Cromosoma(gens)

        return cromosoma



