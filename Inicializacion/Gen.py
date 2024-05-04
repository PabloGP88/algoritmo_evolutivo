import json
import random

with open("./Json/profesores.json") as file:
    profesores_data = json.load(file)
class Gen:
    def __init__(self,id_profesor,id_materia,g_materia,m_materia,pmt_materia,horario,pmt_profesor,n_horas):
        self.id_profesor = id_profesor
        self.id_materia = id_materia
        self.g_materia = g_materia
        self.m_materia = m_materia
        self.pmt_materia = pmt_materia
        self.horario = horario
        self.pmt_profesor = pmt_profesor
        self.n_horas = n_horas

    def Mutar(self):
        x = random.randint(0,1)

        if (x == 0):
            #Mutar profesor
            self.id_profesor = random.choice(list(profesores_data.keys()))
        else: 
            #Mutar hora

            horario_index = random.randint(0, len(self.horario) - 1)  
            horario_seleccionado = self.horario[horario_index]

            inicio = random.randint(7.0, 18.0)  
            duracion = random.randint(1.0, 3.0)  
            hora_inicio = inicio 
            hora_fin = inicio + duracion
            
            self.horario[horario_index] = [horario_seleccionado[0], hora_inicio, hora_fin]
        # else:
        #     #Mutar dia
        #     dias_disponibles = profesores_data[self.id_profesor]["dias"]

        #     horario_index = random.randint(0, len(self.horario) - 1)  
        #     horario_seleccionado = self.horario[horario_index]  
        #     dia_mutable = random.choice(dias_disponibles) 
        #     # Actualiza solo el día seleccionado manteniendo la hora de inicio y fin
        #     self.horario[horario_index][0] = dia_mutable
           


