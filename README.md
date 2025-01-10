![image](https://github.com/user-attachments/assets/23207f9d-67b5-4ab3-b72c-bcc669a13c57)# SNA_BigData

Description
This project leverages Big Data technologies to analyze citation networks in the field of Machine Learning. The primary goals of the project are:
•	Identifying significant academic papers using metrics such as centralities.
•	Analyzing relationships between papers and highlighting key connections.
•	Utilizing Big Data technologies (BigQuery, Hive) for efficient data processing
Project Structure
1. Main Folders
•	openalex-env/queries/: Contains SQL scripts used for data analysis and processing.
•	scripts/: Contains Python scripts for data extraction, graph construction, and machine learning models.
•	openalex-env/project/: Contains generated files, such as graph visualizations and analysis results.
2. Content
•	queries/:
o	create_ml_works_flat.sql: Creates a processed table in BigQuery for academic articles.
o	hive_top_10_most_cited.sql: Extracts the top 10 most-cited articles.
o	hive_top_concepts.sql: Identifies the most frequently used concepts in articles.
•	scripts/:
o	extract_and_load_to_bigquery.py: Extracts data from OpenAlex and loads it into BigQuery.
o	build_and_visualize_citation_network.py: Constructs and visualizes citation networks.
o	random_forest_citation_prediction.py: Implements a Random Forest model to predict citation counts.
o	total_articles_count.py: Counts the total number of available articles.
•	project/:
o	graph_visualization_large.png: Visualization of the citation network.
o	graph_metrics.csv: Metrics calculated for the network (degree, betweenness, closeness, eigenvector centrality).
o	feature_importances.csv: Feature importance for the Random Forest model.
How to Run the Project
1.	Set up the virtual environment:
conda create --name openalex-env python=3.9
conda activate openalex-env
pip install -r requirements.txt
2.	Run the scripts:
o	Data extraction: python scripts/extract_and_load_to_bigquery.py
o	Citation network construction and visualization: python scripts/build_and_visualize_citation_network.py
o	Citation prediction: python scripts/random_forest_citation_prediction.py
Technologies Used
•	Languages: Python, SQL.
•	Big Data: Google BigQuery, Apache Hive.
•	Machine Learning: Scikit-learn.
•	Visualization: NetworkX, Matplotlib.

![image](https://github.com/user-attachments/assets/5dcc95d1-dcb7-4f2e-89d0-d73f1892ee7f)
