-- On définit nos fonctions qui vont mettre à jour la population pour chaque département/région
-- La population d'un/d'une département/région est calculée que si l'ensemble des communes/département du/(de la) département/région est renseignée.
CREATE OR REPLACE FUNCTION calcul_pop_dep(annee_cible INT) 
    RETURNS TABLE (
        code_departement VARCHAR,
        annee INT,
		population FLOAT
) AS $$
BEGIN
    RETURN QUERY 
		SELECT C.code_departement, annee_cible AS annee, SUM(S.valeur) AS population
		FROM commune C
		JOIN (
			SELECT code_commune, valeur 
			FROM statistiques_pop
			WHERE type_statistique = 'population' AND annee_debut = annee_cible
		) S ON C.code = S.code_commune
		JOIN (
			SELECT TempC.code_departement, COUNT(*) AS commune_count -- Nombre total de commune pour chaque département
			FROM commune TempC
			GROUP BY TempC.code_departement
		) CD ON C.code_departement = CD.code_departement
		GROUP BY C.code_departement, commune_count
		HAVING COUNT(*) = commune_count;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION calcul_pop_reg(annee_cible INT) 
    RETURNS TABLE (
        code_region VARCHAR,
        annee INT,
		population FLOAT
) AS $$
BEGIN
    RETURN QUERY 
		SELECT D.code_region, annee_cible AS annee, SUM(DP.pop) AS population
		FROM departement D
		JOIN (
			SELECT TempDP.code_departement, TempDP.population AS pop
			FROM departement_pop TempDP
			WHERE TempDP.annee = annee_cible
		) DP ON D.code = DP.code_departement
		JOIN (
			SELECT TempD.code_region, COUNT(*) AS departement_count -- Nombre total de département pour chaque région
			FROM departement TempD
			GROUP BY TempD.code_region
		) DR ON D.code_region = DR.code_region
		GROUP BY D.code_region, departement_count
		HAVING COUNT(*) = departement_count;
END;
$$ LANGUAGE 'plpgsql';

-- Procédure pour insérer les données dans les tables 'departement_pop'/'region_pop'. Elle utilise les fonctions définies plutôt
CREATE OR REPLACE PROCEDURE insert_population_if_all(annee_cible INT)
AS $$
BEGIN
    -- Insertion des populations des départements
    INSERT INTO departement_pop (code_departement, annee, population)
        SELECT * FROM calcul_pop_dep(annee_cible)
        ON CONFLICT DO NOTHING;

    -- Insertion des populations des régions
    INSERT INTO region_pop (code_region, annee, population)
        SELECT * FROM calcul_pop_reg(annee_cible)
        ON CONFLICT DO NOTHING;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour appeler la procédure
CREATE OR REPLACE FUNCTION call_insert_population_if_all()
RETURNS TRIGGER AS $$
DECLARE
   row record;
BEGIN
    FOR row IN SELECT DISTINCT annee_debut AS annee FROM statistiques_pop LOOP
        CALL insert_population_if_all(row.annee);
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour détecter si une nouvelle année de recensement est ajoutée au niveau de la table 'statistiques_pop'
CREATE OR REPLACE TRIGGER population_insert_departement_region
AFTER INSERT ON statistiques_pop
FOR EACH STATEMENT
EXECUTE PROCEDURE call_insert_population_if_all();