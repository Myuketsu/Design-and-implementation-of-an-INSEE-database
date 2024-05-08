-- Tables population pour departement et region
ALTER TABLE departement
ADD COLUMN IF NOT EXISTS population INT;

ALTER TABLE region
ADD COLUMN IF NOT EXISTS population INT;

-- DEFINITION DE LA PROCEDURE

CREATE OR REPLACE PROCEDURE update_population()
AS $$
BEGIN
    -- Mise à jour des populations des départements
    UPDATE departement AS D
    SET population = S.pop
    FROM (
        SELECT C.code_departement, SUM(S.valeur) AS pop
        FROM commune C
        JOIN (
            SELECT code_commune, valeur 
            FROM statistiques_pop
            WHERE type_statistique = 'population' AND annee_debut = '2020'
        ) S ON C.code = S.code_commune
        GROUP BY C.code_departement
    ) S
    WHERE D.code = S.code_departement;

    -- -- Mise à jour des populations des régions
    UPDATE region AS R
    SET population = S.pop
    FROM (
        SELECT D.code_region, SUM(S.valeur) AS pop
        FROM departement AS D
        JOIN commune C ON C.code_departement = D.code
        JOIN (
            SELECT code_commune, valeur 
            FROM statistiques_pop
            WHERE type_statistique = 'population' AND annee_debut = '2020'
        ) S ON C.code = S.code_commune
        GROUP BY D.code_region
    ) S
    WHERE R.code = S.code_region;
END;
$$ LANGUAGE plpgsql;

CALL update_population();