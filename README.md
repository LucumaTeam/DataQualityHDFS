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
* **week:** week from 1 to 19. Weeks 14 and 19 should not be used because they contain errors.
* **minutes:** total minutes.

## DataWarehouse

El almacén de datos usado por el proceso ETL, está basado en HDFS y usa como infraestructura de almacenamiento HIVE. Este almacén está compuesto por las siguientes BBDD:

* **Landing:** Esta base de datos se usa para almacenar los datos provenientes de los ficheros csv cargados sin ningún tipo de procesamiento, de esta manera podremos tener historificados los ficheros provenientes de la fuente. Contiene una tabla compuesta por todas las columnas de dataset sin procesar. Está particionada por la hora a la que se insertó en HDFS.
* **Preparation:** Usamos esta base de datos para almacenar los datos procesados. Se cargan los datos que provienen de la base de datos landing y se validan para cumplir las reglas de negocio. Contiene una tabla compuesta por todas las columnas de dataset tipados. Está particionada por las columnas temporales slot y week. 
* **KPI:** Base de datos que usamos para almacenar los diferentes KPI's. Los datos se generan a partir de la base de datos preparation. En un principio está compuesta por el KPI descrito en el apartado anterior.

Los diferentes esquemas de HIVE están especificados en el directorio del repositorio src/data

## Orquestación

La orquestación de las tareas necesarias para construir la ETL usa como tecnología oozie. El proceso de ETL está compuesto por los siguientes workflows:

* **Carga Fichero:** Workflow que usamos para cargar los ficheros csv procedentes de una fuente externa a nuestro sistema HDFS. Está compuesto por las siguientes acciones:

  1. **file_load_landing.** Acción que mueve el fichero desde el directorio de entrada a nuestro sistema de HDFS. La ruta de HDFS va coincidir con una partición la BBDD Landing de Hive.
  2. **hive_remake_landing.** Una vez el fichero está en directorio de la BBDD landing HIVE es necesario rehacer la tabla para que detecte la última partición creada.
  3. **dataset_fileload.** Genera un fichero SUCCESS en el directorio de HDFS que usan los datasets de Oozie. Este fichero lo usarán  los coodinadores asociados a estos procesos para que puedan ejecutar las tareas. Esta ruta tiene el formato HDFS/fileload/YYYY-MM-DD.

  El código de este worflow está disponible en el repositorio en la dirección src/oozie/workflow/fileload/workflow.xml

* **Preparación datos:** Workflow usado para cargar los datos almacenados en landing, validarlos, darles formato y almacenarlos en la base de datos preparation de HIVE. está compuesto por las siguientes acciones:

  1. **spark-node** Acción que selecciona los últimos datos cargados en la tabla landing. Esta desarrollado usando Spark, realiza las siguientes acciones:
  
  * Validar los datos, solo va cargar aquellos datos que cumplan la especificación de la tabla tv_audience de la BBDD Preparation.
  * Persistir los datos, determinará que registros son nuevos para introducir y cuales son actualizaciones de datos ya existentes 
    
  2. **dataset_preparation** Genera un fichero SUCCESS en el directorio de HDFS que usan los datasets de Oozie. Este fichero lo usarán  los coodinadores asociados a estos procesos para que puedan ejecutar las tareas. Esta ruta tiene el formato HDFS/preparation/YYYY-MM-DD.
  
  El código de este worflow está disponible en el repositorio en la dirección src/oozie/workflow/preparation/workflow.xml

* **Generación KPI:** Workflow usado para generar los diferentes KPI's y almacenarlos en la base de datos KPI de HIVE. Por el momento el único KPI desarrollado es definido el apartado KPI de este documento. Esta desarrollado usando Spark 

El código de este worflow está disponible en el repositorio en la dirección src/oozie/workflow/kpi/workflow.xml

Todos los workflows anteriormente expuestos será necesario planificarlos y ejecutarlos en función de diferentes eventos. Para lograr esto, será necesario el desarrollo de coordinadores que implementen está funcionalidad. Para nuestra ETL hemos desarrollado los siguientes coordinadores:

* **Carga de fichero** Este coordinador se encarga de planificar la ejecución del workflow carga de fichero. Usa una planificación temporal, en concreto esta planificado para lanzarse una vez al día, ya que se espera que el fichero venga diariamente a una determinada hora.

  El código de este worflow está disponible en el repositorio en la dirección src/oozie/workflow/landing/coordinator.xml

* **Preparación de datos** Este coordinador se encarga de planificar la ejecución del workflow de preparación de datos. Usa una planificación basada en la disponibilidad de datos, en este caso espera que exista un fichero en un determinado directorio que tiene una especificación temporal. 
Este directorio debe tener el formato YYYY-MM-DD, donde esta fecha es el día que debe ser ejecutado. Dentro de esta carpeta debe estar almacenado un fichero con el nombre SUCCESS, una vez se encuentre el fichero se puede ejecutar el proceso. Este fichero es encargado de generarlo la acción número 3 del workflow de carga de ficheros.

  El código de este worflow está disponible en el repositorio en la dirección src/oozie/workflow/preparation/coordinator.xml

* **Generar KPI** Este coordinador se encarga de generar el KPI. Usa una planificación basada en la disponibilidad de datos, en este caso espera que exista un fichero en un determinado directorio que tiene una especificación temporal. 
Este directorio debe tener el formato YYYY-MM-DD, donde esta fecha es el día que debe ser ejecutado. Dentro de esta carpeta debe estar almacenado un fichero con el nombre SUCCESS, una vez se encuentre el fichero se puede ejecutar el proceso. Este fichero es encargado de generarlo la acción número 2 del workflow de preparación de datos.

  El código de este worflow está disponible en el repositorio en la dirección src/oozie/workflow/kpi/coordinator.xml

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
