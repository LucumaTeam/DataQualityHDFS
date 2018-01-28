# DataQualityHDFS

Desarrollo de un componente Data Quality capaz de procesar datos almacenados en un Data Lake sobre HDFS

## DataSet

El dataset para realizar el analisis esta basado en la audiencias de televisión, está formado por los siguientes campos:
* **channel ID:** channel id from 1 to 217.
* **slot:** hour inside the week relative to the start of the view, from 1 to 24*7 = 168.
* **week:** week from 1 to 19. Weeks 14 and 19 should not be used because they contain errors.
* **genre ID:** it is the id of the genre, form 1 to 8. Genre/subgenre mapping is attached below.
* **subGenre ID:** it is the id of the subgenre, from 1 to 114. Genre/subgenre mapping is attached below.
* **user ID:** it is the id of the user.
* **program ID:** it is the id of the program. The same program can occur multiple times (e.g. a tv show).
* **event ID:** it is the id of the particular instance of a program. It is unique, but it can span multiple slots.
* **duration:** duration of the view.

## KPI

Una vez analizado el Data Set el siguiente paso es seleccionar un KPI para desarrollar metrica. El KPI es el número de minutos vistos de un programa en un canal por hora, tendra la siguientes columnas:

* **program ID:** it is the id of the program. The same program can occur multiple times (e.g. a tv show).
* **channel ID:** channel id from 1 to 217.
* **slot:** hour inside the week relative to the start of the view, from 1 to 24*7 = 168.
* **minutes:** total minutes.

## Métricas

Una vez establecido el KPI es necesario seleccionar unas métrica de referencia para evaluar el impacto en los indicador clave de rendimiento.

1. **Métrica:** Número de valores nulos en la columna program ID del Data Set.
2. **Test:** Verificar que los valores nulos > 15%.
3. **Impacto:** Estamos perdiendo información sobre el visionado de programas en un canal.

## Resultados

Una vez cargada la información del Data Set en una tabla de HIVE y obtenida los valores del KPI, con la metrica del paso anterior, los resultados son los siguientes:

1. **Métrica:** Número de valores nulos en la columna program ID del Data Set.
2. **Test:** Falso, ya que el numero de registros que cumplan la condición anterior es 0%.
3. **Impacto:** No se está perdiendo información de los programas.
