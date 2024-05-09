-- WIP
CREATE OR REPLACE PROCEDURE update_population_if_all()
AS $$
BEGIN
    -- Mise à jour des populations des départements
    UPDATE departement_pop AS DP
    SET population = GDP.population
    FROM (

    )
    WHERE DP.code_departement = GDP.code_departement AND DP.annee = GDP.annee;

    -- -- Mise à jour des populations des régions
    UPDATE region_pop AS RP
    SET population = GRP.population
    FROM get_pop_region GRP
    WHERE RP.code_region = GRP.code_region AND RP.annee = GRP.annee;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION call_update_population_if_all()
RETURNS TRIGGER AS $$
BEGIN
    CALL update_population_if_all();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER population_update_departement_region
AFTER INSERT ON statistiques_pop
FOR EACH STATEMENT
EXECUTE PROCEDURE call_update_population_if_all();