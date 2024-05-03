CREATE TABLE region (
    code VARCHAR(8) CONSTRAINT region_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,

    cheflieu VARCHAR(8) NOT NULL
);

CREATE TABLE departement (
    code VARCHAR(8) CONSTRAINT departement_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,

    cheflieu VARCHAR(8) NOT NULL,
    code_region VARCHAR(8) REFERENCES region(code)
);

CREATE TABLE commune (
    code VARCHAR(8) CONSTRAINT commune_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,

    code_departement VARCHAR(8) REFERENCES departement(code)
);

CREATE TABLE cheflieu (
    code_commune VARCHAR(8) CONSTRAINT chef_lieu_key PRIMARY KEY REFERENCES commune(code),
    code_departement VARCHAR(8) REFERENCES departement(code),
    code_region VARCHAR(8) REFERENCES region(code)
);