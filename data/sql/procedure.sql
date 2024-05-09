-- Tables population pour departement et region
CREATE TABLE IF NOT EXISTS departement_pop (
    code_departement VARCHAR(2) REFERENCES departement(code),
    annee VARCHAR(4),
    population FLOAT,

    PRIMARY KEY (code_departement, annee)
);

CREATE TABLE IF NOT EXISTS region_pop (
    code_region VARCHAR(2) REFERENCES region(code),
    annee VARCHAR(4),
    population FLOAT,

    PRIMARY KEY (code_region, annee)
);

-- View pour obtenir la population pour chaque département/région
CREATE OR REPLACE VIEW get_pop_departement AS
SELECT code_departement, annee_debut AS annee, SUM(S.valeur) AS population
    FROM commune C
    JOIN (
        SELECT code_commune, annee_debut, valeur 
        FROM statistiques_pop
        WHERE type_statistique = 'population'
    ) S ON C.code = S.code_commune
    GROUP BY C.code_departement, S.annee_debut;

CREATE OR REPLACE VIEW get_pop_region AS
SELECT code_region, annee, SUM(DP.population) AS population
    FROM departement D
    JOIN departement_pop DP ON D.code = DP.code_departement
    GROUP BY D.code_region, DP.annee;

-- Insertion des données dans les tables
INSERT INTO departement_pop (code_departement, annee, population)
    SELECT * FROM get_pop_departement;

INSERT INTO region_pop (code_region, annee, population)
    SELECT * FROM get_pop_region;

-- Définition de la procédure
CREATE OR REPLACE PROCEDURE update_population()
AS $$
BEGIN
    -- Mise à jour des populations des départements
    UPDATE departement_pop AS DP
    SET population = GDP.population
    FROM get_pop_departement GDP
    WHERE DP.code_departement = GDP.code_departement AND DP.annee = GDP.annee;

    -- -- Mise à jour des populations des régions
    UPDATE region_pop AS RP
    SET population = GRP.population
    FROM get_pop_region GRP
    WHERE RP.code_region = GRP.code_region AND RP.annee = GRP.annee;
END;
$$ LANGUAGE plpgsql;

-- CALL update_population();