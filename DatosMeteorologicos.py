from typing import Tuple
import math

class DatosMeteorologicos:
    def __init__(self, nombre_archivo: str):
      
#Inicializamos la instacia de esa clase

        self.nombre_archivo = nombre_archivo

    def procesar_datos(self) -> Tuple[float, float, float, float, str]:

#Metemos o procesamos los datos de ese archivo y nos devuelve los mismos datos

        suma_temperatura= 0
        suma_humedad =0
        suma_presion =0
        suma_velocidad_viento_x = 0
        suma_velocidad_viento_y= 0
        total_registros = 0
        direccion_viento_frecuencia= {}

        with open(self.nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.startswith('Temperatura:'):
                    suma_temperatura+= float(linea.split(':')[1].strip())
                elif linea.startswith('Humedad:'):
                    suma_humedad +=float(linea.split(':')[1].strip())
                elif linea.startswith('Presión:'):
                    suma_presion += float(linea.split(':')[1].strip())
                elif linea.startswith('Viento:'):
                    viento_info = linea.split(':')[1].strip().split(',')
                    velocidad_viento = float(viento_info[0].strip())
                    direccion_viento = viento_info[1].strip()

                    suma_velocidad_viento_x +=(
                        velocidad_viento * math.cos(self.abreviacion_a_radianes(direccion_viento))
                    )
                    suma_velocidad_viento_y+= (
                        velocidad_viento * math.sin(self.abreviacion_a_radianes(direccion_viento))
                    )


                    direccion_viento_frecuencia[direccion_viento]= (
                    direccion_viento_frecuencia.get(direccion_viento, 0) + 1
                    )


                total_registros+= 1

        promedio_temperatura = suma_temperatura /total_registros
        promedio_humedad =suma_humedad/ total_registros
        promedio_presion=suma_presion /total_registros
        promedio_velocidad_viento = (
        math.sqrt(suma_velocidad_viento_x ** 2 + suma_velocidad_viento_y ** 2) / total_registros
        )
        direccion_viento_prominente = max(
        direccion_viento_frecuencia, key=direccion_viento_frecuencia.get)

        return (
            promedio_temperatura,
            promedio_humedad,
            promedio_presion,
            promedio_velocidad_viento,
            direccion_viento_prominente
        )

    def abreviacion_a_radianes(self, abreviacion: str) -> float:

#Se pone la dirección del viento a radianes

        abreviaciones_grados = {
            "N": 0,
            "NNE": 22.5,
            "NE": 45,
            "ENE": 67.5,
            "E": 90,
            "ESE": 112.5,
            "SE": 135,
            "SSE": 157.5,
            "S": 180,
            "SSW": 202.5,
            "SW": 225,
            "WSW": 247.5,
            "W": 270,
            "WNW": 292.5,
            "NW": 315,
            "NNW": 337.5,
        }
        return math.radians(abreviaciones_grados.get(abreviacion, 0))

if __name__== "__main__":
    ARCHIVO_TEXTO= 'datos.txt'
    datos_meteorologicos =DatosMeteorologicos(ARCHIVO_TEXTO)
    estadisticas= datos_meteorologicos.procesar_datos()
    print('Estadísticas meteorológicas:')
    print('Temperatura promedio:', estadisticas[0])
    print('Humedad promedio:', estadisticas[1])
    print('Presión promedio:', estadisticas[2])
    print('Velocidad promedio del viento:', estadisticas[3])
    print('Dirección predominante del viento:', estadisticas[4])
