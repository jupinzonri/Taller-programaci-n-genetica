import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from gplearn.genetic import SymbolicClassifier

# 1. Generación de Dataset Sintético Realista
np.random.seed(42)
n_samples = 1500

monto = np.random.uniform(10000, 8000000, n_samples)
hora = np.random.randint(0, 24, n_samples)
distancia = np.random.uniform(0.1, 500, n_samples)
ingreso = np.random.uniform(1500000, 20000000, n_samples)

df = pd.DataFrame({
    'monto_pesos': monto,
    'hora_dia': hora,
    'distancia_residencia': distancia,
    'ingreso_mensual': ingreso
})

# Aplicación de reglas de negocio
monto_relativo = df['monto_pesos'] / df['ingreso_mensual']
es_madrugada = ((df['hora_dia'] >= 1) & (df['hora_dia'] <= 4)).astype(int)
es_lejano = (df['distancia_residencia'] > 250).astype(int)

score_riesgo = (
    (monto_relativo > 0.40).astype(int) * 0.45 +
    (es_madrugada & (df['monto_pesos'] > 1000000)).astype(int) * 0.35 +
    (es_lejano & (df['monto_pesos'] > 1500000)).astype(int) * 0.30
)

ruido = np.random.normal(0, 0.08, n_samples)
df['fraude'] = ((score_riesgo + ruido) > 0.40).astype(int)
df.to_csv('transacciones_fraude_realista.csv', index=False)

# 2. Entrenar Programación Genética Simbólica
X = df[['monto_pesos', 'hora_dia', 'distancia_residencia', 'ingreso_mensual']]
y = df['fraude']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

clf = SymbolicClassifier(
    population_size=1000,
    generations=20,
    tournament_size=20,
    stopping_criteria=0.01,
    function_set=('add', 'sub', 'mul', 'div', 'sqrt', 'log', 'abs'),
    p_crossover=0.7,
    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    verbose=1,
    parsimony_coefficient=0.005,
    random_state=42
)

print("--- Entrenando Modelo Simbólico de Fraude con PG ---")
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]

print("\n==============================================")
print(f"Expresión Simbólica Evolucionada: {clf._program}")
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
print("==============================================")
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred))
