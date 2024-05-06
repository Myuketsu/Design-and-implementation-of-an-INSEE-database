CREATE OR REPLACE PROCEDURE update_population()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Mise à jour des populations des départements
    UPDATE departement AS D
    SET pop = (
        SELECT SUM(S.valeur), C.code
        FROM commune C
        JOIN statistiques_pop S ON C.code = S.code_commune
        WHERE S.type_statistique = 'population' AND S.annee_debut = '2020'
        GROUP BY C.code
    );

    -- -- Mise à jour des populations des régions
    -- UPDATE region AS R
    -- SET pop = (
    --     SELECT SUM(D.pop)
    --     FROM departement AS D
    --     WHERE D.code_region = R.code
    -- );
END;
$$;