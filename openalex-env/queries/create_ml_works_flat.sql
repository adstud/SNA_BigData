CREATE OR REPLACE TABLE `tehnologii-big-data-ad.openalex_work.ml_works_flat` AS
SELECT
  machine_learning_works.id AS id,
  machine_learning_works.title AS title,
  machine_learning_works.publication_year AS publication_year,
  machine_learning_works.cited_by_count AS cited_by_count,
  ARRAY_LENGTH(machine_learning_works.referenced_works) AS num_referinte,
  STRING_AGG(DISTINCT CONCAT(c.id, ':', c.display_name), '; ') AS concept_names
FROM
  `tehnologii-big-data-ad.openalex_work.machine_learning_works` AS machine_learning_works,
  UNNEST(machine_learning_works.concepts) AS c
GROUP BY
  machine_learning_works.id, machine_learning_works.title, machine_learning_works.publication_year, 
  machine_learning_works.cited_by_count, machine_learning_works.referenced_works;

