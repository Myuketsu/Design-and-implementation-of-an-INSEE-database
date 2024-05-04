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

CREATE TABLE Population (
    id SERIAL PRIMARY KEY,
    CODGEO VARCHAR(10),
    SUPERF FLOAT,
    P20_LOG FLOAT,
    P14_LOG FLOAT,
    P09_LOG FLOAT,
    D99_LOG INT,
    D90_LOG INT,
    D82_LOG INT,
    P20_LOGVAC FLOAT,
    P14_LOGVAC FLOAT,
    P09_LOGVAC FLOAT,
    D99_LOGVAC INT,
    D90_LOGVAC INT,
    D82_LOGVAC INT,
    DECE1420 INT,
    DECE0914 INT,
    DECE9909 INT,
    DECE9099 INT,
    DECE8290 INT,
    NAIS1420 INT,
    NAIS0914 INT,
    NAIS9909 INT,
    NAIS9099 INT,
    NAIS8290 INT,
    P20_POP FLOAT,
    P14_POP FLOAT,
    P09_POP FLOAT,
    D99_POP INT,
    D90_POP INT,
    D82_POP INT,
    P20_RP FLOAT,
    P14_RP FLOAT,
    P09_RP FLOAT,
    D99_RP INT,
    D90_RP INT,
    D82_RP INT,
    P20_RSECOCC FLOAT,
    P14_RSECOCC FLOAT,
    P09_RSECOCC FLOAT,
    D99_RSECOCC INT,
    D90_RSECOCC INT,
    D82_RSECOCC INT
);