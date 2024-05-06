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

-- ALTER TABLE etat_matrimonial_anterieur_mariage

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE etat_matrimonial_anterieur_mariage
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);

-- ALTER TABLE nationalite_epoux

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE nationalite_epoux
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);

-- ALTER TABLE repartition_mensuelle_mariage

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE repartition_mensuelle_mariage
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);



-- Table mariage

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE mariage
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);

-- Table premier mariage

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE premier_mariage
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);

-- Table pays mariage

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE pays_mariage
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);

-- Table etat_matrimonial_anterieur_mariage

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE etat_matrimonial_anterieur_mariage
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);

-- Table nationalite_epoux

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE nationalite_epoux
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);

-- Table repartition_mensuelle_mariage

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE repartition_mensuelle_mariage
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);