-- Hive SQL: Cele mai utilizate concepte în articole
INSERT OVERWRITE DIRECTORY '/date/machine_learning_hive/top_concepts'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
SELECT 
    concept_names, 
    COUNT(*)
FROM 
    ml_works
GROUP BY 
    concept_names
ORDER BY 
    COUNT(*) DESC
LIMIT 10;

