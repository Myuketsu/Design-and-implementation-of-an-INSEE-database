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

-- Table population

ALTER TABLE population
ADD CONSTRAINT population_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code),
ADD CONSTRAINT population_commune_fk FOREIGN KEY (idcommune) REFERENCES commune(code);