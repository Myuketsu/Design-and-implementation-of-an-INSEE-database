-- Fonctions qui jettent des messages d'erreurs pour bloquer les commandes INSERT, UPDATE et DELETE sur les tables departement et region
CREATE OR REPLACE FUNCTION prevenir_modification_departement()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Les modifications sur la table "departement" sont interdites.';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION prevenir_modification_region()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Les modifications sur la table "region" sont interdites.';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Triggers pour la table departement
CREATE OR REPLACE TRIGGER bloquage_insert_departement
BEFORE INSERT ON departement
FOR EACH STATEMENT
EXECUTE FUNCTION prevenir_modification_departement();

CREATE OR REPLACE TRIGGER bloquage_update_departement
BEFORE UPDATE ON departement
FOR EACH STATEMENT
EXECUTE FUNCTION prevenir_modification_departement();

CREATE OR REPLACE TRIGGER bloquage_delete_departement
BEFORE DELETE ON departement
FOR EACH STATEMENT
EXECUTE FUNCTION prevenir_modification_departement();

-- Triggers pour la table region
CREATE OR REPLACE TRIGGER bloquage_insert_region
BEFORE INSERT ON region
FOR EACH STATEMENT
EXECUTE FUNCTION prevenir_modification_region();

CREATE OR REPLACE TRIGGER bloquage_update_region
BEFORE UPDATE ON region
FOR EACH STATEMENT
EXECUTE FUNCTION prevenir_modification_region();

CREATE OR REPLACE TRIGGER bloquage_delete_region
BEFORE DELETE ON region
FOR EACH STATEMENT
EXECUTE FUNCTION prevenir_modification_region();

-- Triggers pour pour mettre à jour la population d'un département et d'une région quand la population d'une commune est mise à jour.
CREATE OR REPLACE TRIGGER population_update_departement_region
AFTER UPDATE ON commune
FOR EACH STATEMENT
BEGIN
    CALL update_population();
END;