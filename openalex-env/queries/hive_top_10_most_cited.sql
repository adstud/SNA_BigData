-- Hive SQL: Extrage primele 10 articole cu cele mai multe citări
INSERT OVERWRITE DIRECTORY '/date/machine_learning_hive/top_10_most_cited'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
SELECT 
    id, 
    title, 
    cited_by_count
FROM 
    ml_works
ORDER BY 
    cited_by_count DESC
LIMIT 10;

