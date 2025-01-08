# Importă bibliotecile necesare
from google.cloud import bigquery
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Configurare client BigQuery
client = bigquery.Client(project="tehnologii-big-data-ad")  # Înlocuiește cu ID-ul proiectului tău

# Interogarea BigQuery pentru articole
query = """
SELECT
  id AS source,
  ref_work AS target
FROM
  `tehnologii-big-data-ad.openalex_work.machine_learning_works`,
  UNNEST(referenced_works) AS ref_work
WHERE
  ARRAY_LENGTH(referenced_works) > 300
"""

# Execută interogarea și încarcă datele într-un DataFrame Pandas
print("Executând interogarea BigQuery...")
query_job = client.query(query)
data = query_job.result().to_dataframe()
print(f"Interogarea a returnat {len(data)} rânduri.")

# Construirea grafului folosind NetworkX
print("Construind graful...")
G = nx.DiGraph()
edges = list(zip(data["source"], data["target"]))
G.add_edges_from(edges)
print(f"Graful a fost construit cu {G.number_of_nodes()} noduri și {G.number_of_edges()} muchii.")

# Verificare componente conectate
components = list(nx.weakly_connected_components(G))
print(f"Graful are {len(components)} componente conectate.")

# Lucrăm doar cu componenta cea mai mare
largest_component = max(components, key=len)
G = G.subgraph(largest_component).copy()
print(f"Componenta cea mai mare are {G.number_of_nodes()} noduri și {G.number_of_edges()} muchii.")

# Calculul centralităților
print("Calculând Degree Centrality...")
degree_centrality = nx.degree_centrality(G)

print("Calculând Betweenness Centrality...")
betweenness_centrality = nx.betweenness_centrality(G)

print("Calculând Closeness Centrality...")
closeness_centrality = nx.closeness_centrality(G)

print("Calculând Eigenvector Centrality...")
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)

# Funcție pentru afișarea topului articolelor după o anumită centralitate
def afiseaza_top_metrici(centralitate, nume_centralitate, top_n=5):
    top_articole = sorted(centralitate.items(), key=lambda item: item[1], reverse=True)[:top_n]
    print(f"\nTop {top_n} articole după {nume_centralitate}:")
    for idx, (nod, valoare) in enumerate(top_articole, start=1):
        print(f"{idx}. Nodul {nod} are {nume_centralitate} de {valoare:.4f}")

# Afișarea top 5 articole pentru fiecare centralitate
afiseaza_top_metrici(degree_centrality, "Degree Centrality")
afiseaza_top_metrici(betweenness_centrality, "Betweenness Centrality")
afiseaza_top_metrici(closeness_centrality, "Closeness Centrality")
afiseaza_top_metrici(eigenvector_centrality, "Eigenvector Centrality")

# Salvarea metricilor într-un fișier CSV
print("Salvând metricile în fișier CSV...")
df_metrics = pd.DataFrame({
    "Node": list(G.nodes),
    "Degree Centrality": [degree_centrality.get(node, 0) for node in G.nodes],
    "Betweenness Centrality": [betweenness_centrality.get(node, 0) for node in G.nodes],
    "Closeness Centrality": [closeness_centrality.get(node, 0) for node in G.nodes],
    "Eigenvector Centrality": [eigenvector_centrality.get(node, 0) for node in G.nodes]
})
df_metrics.to_csv("graph_metrics.csv", index=False)
print("Fișierul 'graph_metrics.csv' a fost salvat.")

# Selectarea unui subset de noduri pentru vizualizare
top_n = 300  # Creștem numărul de noduri pentru vizualizare
top_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:top_n]
subgraph = G.subgraph(top_nodes)
print(f"Subgraful pentru vizualizare conține {subgraph.number_of_nodes()} noduri și {subgraph.number_of_edges()} muchii.")

# Vizualizare statică a grafului
print("Generând vizualizarea statică...")
plt.figure(figsize=(15, 15))  # Dimensiune mai mare pentru claritate
pos = nx.spring_layout(subgraph, seed=42)  # Layout pentru graful subeșantionat

# Nodurile
node_sizes = [degree_centrality[node] * 2500 for node in subgraph.nodes]  # Dimensiuni mai mari
node_colors = [eigenvector_centrality[node] for node in subgraph.nodes]

nx.draw_networkx_nodes(
    subgraph,
    pos,
    node_size=node_sizes,
    node_color=node_colors,
    cmap=plt.cm.viridis,
    alpha=0.9
)

# Muchiile
nx.draw_networkx_edges(subgraph, pos, alpha=0.3, edge_color="gray")

# Etichete doar pentru nodurile cele mai importante
important_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:20]  # Mai multe etichete
nx.draw_networkx_labels(
    subgraph,
    pos,
    labels={node: node for node in important_nodes},
    font_size=8,
    font_color="white"
)

plt.title(f"Vizualizare statică a subgrafului (Top {top_n} noduri)", fontsize=16)
plt.axis("off")
plt.savefig("graph_visualization_large.png", format="png")
print("Vizualizarea statică extinsă a fost salvată în 'graph_visualization_large.png'.")
plt.show()
