import random
import numpy as np
from deap import algorithms, base, creator, tools, gp

# 1. Tabla de Verdad para el Segmento 'a' (BCD 0 al 9)
# Dígitos donde el segmento 'a' está encendido (1): 0, 2, 3, 5, 6, 7, 8, 9
# Dígitos donde está apagado (0): 1, 4
TRUTH_TABLE = [
    # (x3, x2, x1, x0) -> Target segmento 'a'
    ((False, False, False, False), True),   # 0
    ((False, False, False, True),  False),  # 1
    ((False, False, True,  False), True),   # 2
    ((False, False, True,  True),  True),   # 3
    ((False, True,  False, False), False),  # 4
    ((False, True,  False, True),  True),   # 5
    ((False, True,  True,  False), True),   # 6
    ((False, True,  True,  True),  True),   # 7
    ((True,  False, False, False), True),   # 8
    ((True,  False, False, True),  True)    # 9
]

# 2. Definición de Operadores Lógicos
def logic_and(a, b): return a and b
def logic_or(a, b):  return a or b
def logic_not(a):    return not a

# 3. Configurar Conjunto de Primitivas (PrimitiveSet)
pset = gp.PrimitiveSet("MAIN", 4)
pset.addPrimitive(logic_and, 2, name="AND")
pset.addPrimitive(logic_or, 2, name="OR")
pset.addPrimitive(logic_not, 1, name="NOT")
pset.renameArguments(ARG0='x3', ARG1='x2', ARG2='x1', ARG3='x0')

# 4. Definición de Fitness e Individuo
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

# 5. Función de Aptitud
def evaluate_circuit(individual):
    func = toolbox.compile(expr=individual)
    hits = 0
    for inputs, target in TRUTH_TABLE:
        try:
            res = func(*inputs)
            if bool(res) == target:
                hits += 1
        except Exception:
            return (0,)
    return (hits,)

toolbox.register("evaluate", evaluate_circuit)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

# Limitar crecimiento desmedido del árbol (Bloat control)
toolbox.decorate("mate", gp.staticLimit(key=len, max_value=20))
toolbox.decorate("mutate", gp.staticLimit(key=len, max_value=20))

# 6. Ejecución del Algoritmo Genético
def main():
    random.seed(42)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    print("--- Iniciando Evolución de Circuito Lógico ---")
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.1, ngen=40, 
                                   stats=stats, halloffame=hof, verbose=True)

    best = hof[0]
    print("\n==============================================")
    print("¡Mejor Circuito Lógico Encontrado!")
    print(f"Expresión: {best}")
    print(f"Aptitud (Aciertos): {best.fitness.values[0]} / 10")
    print("==============================================")

if __name__ == "__main__":
    main()
