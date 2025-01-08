# Importă bibliotecile necesare
from google.cloud import bigquery
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Configurează clientul BigQuery
client = bigquery.Client(project="tehnologii-big-data-ad")

# Definește interogarea pentru a obține datele relevante
query = """
SELECT
  publication_year,
  ARRAY_LENGTH(referenced_works) AS num_referinte,
  ARRAY_LENGTH(authorships) AS num_autori,
  cited_by_count
FROM
  `tehnologii-big-data-ad.openalex_work.machine_learning_works`
WHERE
  ARRAY_LENGTH(referenced_works) > 400
"""

# Execută interogarea și încarcă datele într-un DataFrame Pandas
query_job = client.query(query)
data = query_job.result().to_dataframe()

# Verifică dacă există valori lipsă și elimină-le
data = data.dropna()

# Definirea caracteristicilor (X) și a țintei (y)
X = data[['publication_year', 'num_referinte', 'num_autori']]
y = data['cited_by_count']

# Împărțirea datelor în seturi de antrenament și testare
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Antrenează modelul Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prezicerea valorilor pentru setul de testare
y_pred = model.predict(X_test)

# Evaluarea performanței modelului
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Eroarea pătratică medie (MSE): {mse}')
print(f'Coeficientul de determinare (R^2): {r2}')

# Importanța caracteristicilor
feature_importances = pd.DataFrame({
    'Caracteristică': X.columns,
    'Importanță': model.feature_importances_
}).sort_values(by='Importanță', ascending=False)

print("\nImportanța caracteristicilor:")
print(feature_importances)

# Salvează rezultatele într-un fișier CSV
feature_importances.to_csv("feature_importances.csv", index=False)
print("\nImportanța caracteristicilor a fost salvată în 'feature_importances.csv'.")
