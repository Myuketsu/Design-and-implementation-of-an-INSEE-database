CREATE TABLE region (
    code VARCHAR(8) CONSTRAINT region_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL
);

CREATE TABLE departement (
    code VARCHAR(8) CONSTRAINT departement_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,

    code_region VARCHAR(8) REFERENCES region(code)
);

CREATE TABLE commune (
    code VARCHAR(8) CONSTRAINT commune_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,

    code_departement VARCHAR(8) REFERENCES departement(code)
);

CREATE TABLE cheflieuRegion (
    code VARCHAR(8) CONSTRAINT chef_lieu_region_key PRIMARY KEY,

    code_region VARCHAR(8) REFERENCES region(code)
);

CREATE TABLE cheflieuDepartement (
    code VARCHAR(8) CONSTRAINT chef_lieu_departement_key PRIMARY KEY,

    code_departement VARCHAR(8) REFERENCES departement(code)
);

-- Pour les mariages, il faut voir comment faire en sorte que REGDEP_MAR et REGDEP_DOMI soient des clés étrangères qui réfèrent à la table departement et région
-- Il faudra donc séparer les VARCHAR
-- D1
CREATE TABLE mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5),
    region_departement VARCHAR(5),
    groupe_age VARCHAR(5),
    nombre_de_maries INT
);

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE mariage
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE mariage
SET idreg = LEFT(REGDEP_MAR, 2),
    iddep = RIGHT(REGDEP_MAR, 2);

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE mariage
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);


-- D3
CREATE TABLE premier_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5),
    region_departement VARCHAR(5),
    groupe_age VARCHAR(5),
    nombre_de_maries INT
);

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE premier_mariage
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE premier_mariage
SET idreg = LEFT(REGDEP_MAR, 2),
    iddep = RIGHT(REGDEP_MAR, 2);

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE premier_mariage
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);

-- D5
CREATE TABLE pays_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(2),
    region_departement VARCHAR(5),
    pays_naissance VARCHAR(7),
    nombre_de_maries INT
);

-- On ajoute les colonnes pour les clés étrangères dans la table mariage qu'on avait mis sur la photo
ALTER TABLE pays_mariage
ADD COLUMN idreg VARCHAR(8),
ADD COLUMN iddep VARCHAR(8);

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE pays_mariage
SET idreg = LEFT(REGDEP_DOMI, 2),
    iddep = RIGHT(REGDEP_DOMI, 2);

-- Et on ajoute les contraintes de clé étrangère
ALTER TABLE pays_mariage
ADD CONSTRAINT mariage_region_fk FOREIGN KEY (idreg) REFERENCES region(code),
ADD CONSTRAINT mariage_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code);

CREATE TABLE population (
    id SERIAL PRIMARY KEY,
    departement_commune VARCHAR(10),
    superficie FLOAT,
    nombre_logement_2020 FLOAT,
    nombre_logement_2014 FLOAT,
    nombre_logement_2009 FLOAT,
    nombre_logement_1999 INT,
    nombre_logement_1990 INT,
    nombre_logement_1982 INT,
    nombre_logements_vacants_2020 FLOAT,
    nombre_logements_vacants_2014 FLOAT,
    nombre_logements_vacants_2009 FLOAT,
    nombre_logements_vacants_1999 INT,
    nombre_logements_vacants_1990 INT,
    nombre_logements_vacants_1982 INT,
    nombre_deces_1420 INT,
    nombre_deces_0914 INT,
    nombre_deces_9909 INT,
    nombre_deces_9099 INT,
    nombre_deces_8290 INT,
    nombre_naissance_1420 INT,
    nombre_naissance_0914 INT,
    nombre_naissance_9909 INT,
    nombre_naissance_9099 INT,
    nombre_naissance_8290 INT,
    population_2020 FLOAT,
    population_2014 FLOAT,
    population_2009 FLOAT,
    population_2099 INT,
    population_2090 INT,
    population_2082 INT,
    residence_principale_2020 FLOAT,
    residence_principale_2014 FLOAT,
    residence_principale_2009 FLOAT,
    residence_principale_1999 INT,
    residence_principale_1990 INT,
    residence_principale_1982 INT,
    residence_secondaire_2020 FLOAT,
    residence_secondaire_2014 FLOAT,
    residence_secondaire_2009 FLOAT,
    residence_secondaire_1999 INT,
    residence_secondaire_1990 INT,
    residence_secondaire_1982 INT
);


-- On ajoute les colonnes pour les clés étrangères dans la table "population"
ALTER TABLE population
ADD COLUMN iddep VARCHAR(8),
ADD COLUMN idcommune VARCHAR(10);

UPDATE population
SET iddep = LEFT(codgeo, 2),
    idcommune = RIGHT(codgeo, 3);

ALTER TABLE population
ADD CONSTRAINT population_departement_fk FOREIGN KEY (iddep) REFERENCES departement(code),
ADD CONSTRAINT population_commune_fk FOREIGN KEY (idcommune) REFERENCES commune(code);