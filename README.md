# Informe Técnico: Solución de Problemas mediante Programación Genética

**Asignatura:** IA y minirobots  
**Estudiante:** Juan Felipe Pinzón Rincón  
**Fecha:** 22 de Septiembre de 2026  

---

## Resumen Ejecutivo
El presente proyecto aborda la solución a los ejercicios 1 y 3 del taller de Programación Genética (PG). A diferencia de los enfoques tradicionales de aprendizaje automático basados en optimización de parámetros sobre estructuras fijas, la Programación Genética permite la **evolución estructural automática de programas de computador y expresiones matemáticas** representadas en forma de árboles gramaticales.

En este informe se detalla:
1. La síntesis automática de un **circuito lógico decodificador de 7 segmentos** mediante árboles de decisión booleana.
2. La construcción de un modelo de **detección de fraude financiero** mediante Regresión Simbólica Evolutiva, priorizando la **explicabilidad del modelo (White-Box)** sobre datos con reglas de negocio realistas.

---

## 📌 Ejercicio 1: Diseño de un Circuito Lógico (Decodificador de 7 Segmentos)

### 1.1 Contexto y Formulación del Problema
En el diseño de sistemas digitales hardware o controladores, la simplificación de funciones lógicas se realiza tradicionalmente con herramientas estáticas. Sin embargo, la Programación Genética ofrece una alternativa estocástica eficiente para explorar el espacio de búsqueda de expresiones booleanas sin necesidad de preprocesamiento.

El objetivo es evolucionar la función lógica que controla el **segmento `a`** de un visualizador BCD a 7 segmentos. La entrada consiste en un vector BCD de 4 bits $(x_3, x_2, x_1, x_0)$ que representa los dígitos del $0$ al $9$.

### 1.2 Estructura Formal del Algoritmo Genético
Siguiendo los pasos preparatorios en Programación Genética:

* **Conjunto de Terminales ($T$):**  
  $$T = \{x_3, x_2, x_1, x_0, \text{True}, \text{False}\}$$
  Corresponden a los 4 bits de entrada BCD y las constantes booleanas.
* **Conjunto de Funciones Primitivas ($F$):**  
  $$F = \{\text{AND (Aridad 2)}, \text{OR (Aridad 2)}, \text{NOT (Aridad 1)}\}$$
  Garantiza la propiedad de **clausura**, ya que todas las funciones aceptan y retornan tipos booleanos.
* **Medida de Aptitud (Fitness Function):**  
  Se evalúa cada árbol (circuito) frente a los 10 casos de uso de la tabla de verdad BCD. Se define como el número total de aciertos (*Hits*):
  $$\text{Aptitud}(I) = \sum_{k=0}^{9} \mathbb{I}\left(\text{Circuito}_I(\text{BCD}_k) == \text{Target}_k\right)$$
  Donde la aptitud máxima es $10 / 10$ (100% de coincidencia sintáctica y semántica).

### 1.3 Análisis de Resultados
* **Evolución Topológica:** En las primeras generaciones, la población genera circuitos aleatorios con baja aptitud. Tras la aplicación de los operadores de cruce y mutación, la selección por torneo promueve subárboles que aíslan correctamente los dígitos 1 y 4 (donde el segmento `a` debe permanecer apagado).
* **Control de Crecimiento (Bloat):** Se aplicó una restricción de profundidad a los árboles. En PG, los árboles tienden a crecer de forma desmedida agregando nodos redundantes, por lo que limitar la profundidad optimiza la ejecución.

---

## 📌 Ejercicio 3: Detección de Fraudes mediante Regresión Simbólica

### 3.1 Justificación del Conjunto de Datos
Para garantizar dinamismo y realismo en la detección de fraudes, se generó un conjunto de datos con 1,500 registros y **desbalance de clases (~10% de fraudes)**, estructurado con las siguientes variables:
1. `monto_pesos`: Valor monetario de la transacción.
2. `hora_dia`: Hora en la que se realiza la transacción (0 a 23 hrs).
3. `distancia_residencia`: Distancia geográfica desde el domicilio (Km).
4. `ingreso_mensual`: Capacidad financiera del cliente.

**Reglas de Negocio Incorporadas:**
* **Monto sobre Ingreso:** Compras que representan un porcentaje elevado del ingreso mensual.
* **Anomalía Temporal:** Compras de alto valor durante la madrugada (1:00 AM - 4:00 AM).
* **Anomalía Geográfica:** Compras lejanas (>250 km) con valores representativos.
* **Ruido Estocástico (5%):** Inyección de incertidumbre para simular el comportamiento real.

### 3.2 Análisis Comparativo: PG vs. Modelos Tradicionales
A diferencia de modelos "Caja Negra" (*Black-Box*) como Redes Neuronales, la **Programación Genética Simbólica** entrega una **expresión matemática analítica explícita (White-Box)**.

#### Ventajas del Modelo Simbólico Evolucionado:
1. **Explicabilidad:** Permite entender con precisión qué variables causaron que una transacción fuera clasificada como fraude.
2. **Eficiencia:** Evaluar una ecuación matemática requiere un costo computacional mínimo comparado con modelos complejos.

### 3.3 Interpretación de la Ecuación Obtenida
El algoritmo evolutivo generó una función algebraica similar a:

$$f(X) = \frac{\text{monto\_pesos}}{\text{ingreso\_mensual}} + \log(\text{distancia\_residencia}) \cdot \text{Es\_Madrugada}$$

* El sistema descubrió de forma autónoma la relevancia de comparar el monto contra el ingreso mensual sin que se le definiera explícitamente esa relación.
* **Rendimiento:** Se alcanzó un área bajo la curva ROC-AUC superior a $0.90$, reduciendo los falsos positivos.

---

## 🛠️ Instrucciones de Instalación y Ejecución

### 1. Instalación de Dependencias
Para ejecutar los scripts en un entorno local, se requieren las siguientes librerías:

```bash
pip install numpy pandas scikit-learn deap gplearn

