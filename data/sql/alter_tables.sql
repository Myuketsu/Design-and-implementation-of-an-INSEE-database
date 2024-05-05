-- ALTER TABLE mariage

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE mariage
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);

-- ALTER TABLE premier_mariage

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE premier_mariage
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);

-- ALTER TABLE pays_mariage

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE pays_mariage
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);

-- ALTER TABLE population

-- On ajoute les colonnes pour les clés étrangères dans la table "population"
ALTER TABLE population
ADD COLUMN iddep VARCHAR(8),
ADD COLUMN idcommune VARCHAR(10);