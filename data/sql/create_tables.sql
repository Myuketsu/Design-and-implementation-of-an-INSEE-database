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
    TYPMAR3 VARCHAR(5),
    REGDEP_MAR VARCHAR(5),
    GRAGE VARCHAR(5),
    NBMARIES INT
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
    TYPMAR3 VARCHAR(5),
    REGDEP_MAR VARCHAR(5),
    GRAGE VARCHAR(5),
    NBMARIES INT
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
    TYPMAR2 VARCHAR(2),
    REGDEP_DOMI VARCHAR(5),
    LNEPOUX VARCHAR(7),
    NBMAR INT
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
    codgeo VARCHAR(10),
    superf FLOAT,
    p20_log FLOAT,
    p14_log FLOAT,
    p09_log FLOAT,
    d99_log INT,
    d90_log INT,
    d82_log INT,
    p20_logvac FLOAT,
    p14_logvac FLOAT,
    p09_logvac FLOAT,
    d99_logvac INT,
    d90_logvac INT,
    d82_logvac INT,
    dece1420 INT,
    dece0914 INT,
    dece9909 INT,
    dece9099 INT,
    dece8290 INT,
    nais1420 INT,
    nais0914 INT,
    nais9909 INT,
    nais9099 INT,
    nais8290 INT,
    p20_pop FLOAT,
    p14_pop FLOAT,
    p09_pop FLOAT,
    d99_pop INT,
    d90_pop INT,
    d82_pop INT,
    p20_rp FLOAT,
    p14_rp FLOAT,
    p09_rp FLOAT,
    d99_rp INT,
    d90_rp INT,
    d82_rp INT,
    p20_rsecocc FLOAT,
    p14_rsecocc FLOAT,
    p09_rsecocc FLOAT,
    d99_rsecocc INT,
    d90_rsecocc INT,
    d82_rsecocc INT
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