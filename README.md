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

Los diferentes esquemas de HIVE están especificados en el directorio del repositorio src/etl

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

  El código de este coordinador está disponible en el repositorio en la dirección src/oozie/workflow/landing/coordinator.xml

* **Preparación de datos** Este coordinador se encarga de planificar la ejecución del workflow de preparación de datos. Usa una planificación basada en la disponibilidad de datos, en este caso espera que exista un fichero en un determinado directorio que tiene una especificación temporal. 
Este directorio debe tener el formato YYYY-MM-DD, donde esta fecha es el día que debe ser ejecutado. Dentro de esta carpeta debe estar almacenado un fichero con el nombre SUCCESS, una vez se encuentre el fichero se puede ejecutar el proceso. Este fichero es encargado de generarlo la acción número 3 del workflow de carga de ficheros.

  El código de este coordinador está disponible en el repositorio en la dirección src/oozie/workflow/preparation/coordinator.xml

* **Generar KPI** Este coordinador se encarga de generar el KPI. Usa una planificación basada en la disponibilidad de datos, en este caso espera que exista un fichero en un determinado directorio que tiene una especificación temporal. 
Este directorio debe tener el formato YYYY-MM-DD, donde esta fecha es el día que debe ser ejecutado. Dentro de esta carpeta debe estar almacenado un fichero con el nombre SUCCESS, una vez se encuentre el fichero se puede ejecutar el proceso. Este fichero es encargado de generarlo la acción número 2 del workflow de preparación de datos.

  El código de este coordinador está disponible en el repositorio en la dirección src/oozie/workflow/kpi/coordinator.xml
  
El flujo de cargas de trabajo de procesamiento de datos generadas por los coordinadores y workflows anteriormente expuestos, será necesario encapsularlo. Este encapsulamiento de los coordinadores lo hemos logrado desarrollando un **Bundle** de oozie.

El código de este bundle está disponible en el repositorio en la dirección src/oozie/workflow/bundle/bundle.xml

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

## Framework HDFS

Una vez establecida la prueba de concepto, vamos a diseñar e implementar en Python y Spark nuestro componente de DataQuality, este componente tiene que satisfacer los siguientes requerimientos:

1. **Establecer y calcular métricas sobre un DataSet.** Las métricas se ejecutarán para un dataset y un periodo. Este periodo estará asociado a la granularidad de procesamiento del dataset dentro del pipeline de la ETL. Los resultados de estas métricas estarán disponibles a nivel de lo que denominaremos interfaz. Está interfaz estará identificada por un dataset y periodo. Se podrán además añadir datasets adicionales, por ejemplo, para comprobar la integridad de los datos referenciales. Se consideran los siguientes aspectos de negocio:
    * Las métricas se ejecutarán para un interfaz. Actualmente estamos procesando la ETL con granularidad o frecuencia diaria, pero podríamos querer ejecutar otros datasets con frecuencias diferentes
    * Las métricas pueden ser a diferentes niveles:
      * Columna
      * Fichero
      * Referenciales
    * Las métricas deben ser agnósticas del dataset o periodo. Recibirán un DataFrame de Spark
2. **Establecer y calcular tests en función de las métricas y el DataSet.** Los tests se ejecutarán para una serie de métricas asociadas a dataset y un periodo. Los tests usarán las métricas descritas anteriormente y en caso de tener umbrales, estos deberán ser parametrizables a nivel de dataset. Se consideran los siguientes aspectos de negocio:
    * Los tests se ejecutarán para una interfaz
    * Los tests no usaran los datasets directamente. Solamente métricas
3. **Calcular las métricas y test sobre un DataSet de forma asíncrona y síncrona.** Se podrán ejecutar las metricas y tests de forma independiente al pipeline o dependiente del pipeline
4. **Detener la ejecución del pipeline en función de los resultados del test.** En base a los resultados del test, se podrá decidir si se continua o no con la ejecución del pipeline. No todos los tests detendrán la ejecución, con lo cual este parámetro ha de ser parametrizable por configuración
5. **Disponer de los resultados de las métricas y resultados.** Los resultados de las métricas y los tests han de estar disponibles para su consulta. Almacenar e identificar los registros que cumplen determinada métrica y han producido que le pipeline no continúe
6. **Reusabilidad y extensibilidad del componente DataQuality.** El componente deber ser reutilizable y extensible a otros proyectos que usen tecnologías BigData y HDFS

En el punto actual del desarrollo, hemos desarrollado e implementado los puntos 1, 2 y 3 de los requerimientos.
A continuación, describiremos el diseño de clases necesarias para cubrir los requerimientos expuestos.

* **Interface.** Clase que encapsula las granularidades y datasets sobre los que queremos aplicar las métricas y tests. Esta clase esta compuesta por las siguientes propiedades: 
  * Granuralidades
  * Tablas
  
*	**Granularity.** Clase abstracta que encapsula la granularidad de un data set. En esta versión se ha diseñado e implementado la siguiente granularidad:
  * GranularityTemporal. Granularidades temporal, por ejemplo, los datos vienen a diario, con lo cual nos indicará el día, mes y año

* **Table.** Clase que encapsula un DataSet, contiene tanto los datos como el esquema. Está compuesta por las siguientes propiedades:
  * DataFrame. Los datos del dataset, son cargados mediante un DataFrame de Spark
  * Colums. Esquema con las definiciones de las columnas del dataset
  * Metrics. Metricas de la interfaz
  * Tests. Tests de la interfaz
  * Granularity. Granuralidad del dataset

* **Column.** Clase que encapsula la definición de una columna del DataSet. Está compuesta por las siguientes propiedades:
  * Name. Nombre de la columna
  * Map_Type. Tipo de dato que usa la columna
  * Metrics. Métricas asociadas a la columna
  
* **Metric.** Clase abstracta que encapsula el concepto de métrica. Usaremos el patrón decorador para evaluar y devolver los resultados de las métricas. Tendremos dos tipos de metricas:
  * MetricFile. Metrica referente al dataset entero
  * MetricColumn. Metrica referente a una columna del dataset

* **MetricExpression.** Clase abstracta que encapsula una métrica en particular. En esta versión hemos implementado las siguientes métricas:
  * MetricExpressionNullValue. Metrica que evalúa si una columna tiene un valor nulo
  
* **MetricResult.** Clase abstracta que encapsula el resultado de una métrica. Está compuesto por las siguientes clases:
  * MetricResultAgg. Representada el resultado de una métrica de tipo agregación
  * MetricResultValidation. Representa el resultado de una métrica de tipo validación. Contiene las siguientes propiedades:
    * OK. Numero de columnas que satisfacen la métrica 
    * NOK. Numero de columnas que no satisfacen la métrica

* **MetricService.** Clase que encapsula un servicio encargado de evaluar las métricas de una interfaz. Presenta el siguiente método:
  * evaluate_metrics. Método que evalúa las métricas de una interfaz que recibe por parámetro
  
* **Test.** Clase que encapsula el concepto de test. Se encarga de evaluar un test en función de su métrica, está compuesto por las siguientes propiedades:
  * Threshold. Umbral del test que nos indica sí o no cumple la condición 
  * Metric. Metrica sobre la que se aplica el test
  * Operation. Operacion que se aplica entre el test y la métrica
  * Representation. Representación del resultado de la métrica
  * Result. Valor booleano que indica si se cumple o no el test
  
* **TestService.** Clase que encapsular un servicio encargado de evaluar los tests de una interfaz. Presenta el siguiente método:
  * assert_tests. Método que evalúa los tests de una interfaz que recibe por parámetro
    
El código de este framework está disponible en el repositorio en la dirección src/main/ 
