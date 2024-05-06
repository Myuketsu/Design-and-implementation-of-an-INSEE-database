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
    code VARCHAR(5) CONSTRAINT commune_key PRIMARY KEY,
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

-- D1
CREATE TABLE mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5),
    region_departement VARCHAR(5),
    groupe_age VARCHAR(5),
    nombre_de_maries INT
);

-- D2 – État matrimonial antérieur des époux selon le département et la région de mariage. Année 2021

CREATE TABLE etat_matrimonial_anterieur_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5),
    region_departement VARCHAR(5),
    sexe VARCHAR(5),
    etat_matrimonial VARCHAR(1),
    nombre_de_maries INT
);


-- D3
CREATE TABLE premier_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5),
    region_departement VARCHAR(5),
    groupe_age VARCHAR(5),
    nombre_de_maries INT
);

-- D4 Nationalité des époux selon le département et la région de domicile conjugal. Année 2021

CREATE TABLE nationalite_epoux (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5),
    region_departement VARCHAR(5),
    nationalite_combinee VARCHAR(7),
    nombre_de_maries INT
);

-- D5
CREATE TABLE pays_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(2),
    region_departement VARCHAR(5),
    pays_naissance VARCHAR(7),
    nombre_de_maries INT
);

-- D6 Répartition mensuelle des mariages selon le département et la région de mariage. Année 2021

CREATE TABLE repartition_mensuelle_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5),
    region_departement VARCHAR(5),
    mois_mariage VARCHAR(2),
    nombre_de_maries INT
);

CREATE TABLE statistiques_pop (
    code_commune VARCHAR(5) REFERENCES commune(code),
    superficie FLOAT,
    annee_debut VARCHAR(4),
    annee_fin VARCHAR(4) CONSTRAINT check_annee_fin_sup_annee_debut CHECK (annee_debut <= annee_fin),
    type_statistique VARCHAR(32),
    valeur FLOAT,

    PRIMARY KEY (code_commune, type_statistique, annee_debut, annee_fin)
);