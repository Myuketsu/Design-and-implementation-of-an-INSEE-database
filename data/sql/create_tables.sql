CREATE TABLE region (
    code VARCHAR(2) CONSTRAINT region_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL
);

CREATE TABLE departement (
    code VARCHAR(2) CONSTRAINT departement_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,

    code_region VARCHAR(2) REFERENCES region(code)
);

CREATE TABLE commune (
    code VARCHAR(5) CONSTRAINT commune_key PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    superficie FLOAT NOT NULL CONSTRAINT superficie_leq_0 CHECK(superficie > 0),

    code_departement VARCHAR(2) REFERENCES departement(code)
);

CREATE TABLE cheflieuRegion (
    code VARCHAR(5) CONSTRAINT chef_lieu_region_key PRIMARY KEY,

    code_region VARCHAR(2) REFERENCES region(code)
);

CREATE TABLE cheflieuDepartement (
    code VARCHAR(5) CONSTRAINT chef_lieu_departement_key PRIMARY KEY,

    code_departement VARCHAR(2) REFERENCES departement(code)
);

-- D1
CREATE TABLE mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5) NOT NULL,
    region_departement VARCHAR(4) NOT NULL,
    groupe_age VARCHAR(5) NOT NULL,
    nombre_de_maries INT NOT NULL CONSTRAINT nbr_mariage_lt_0 CHECK(nombre_de_maries >= 0)
);

-- D2 – État matrimonial antérieur des époux selon le département et la région de mariage. Année 2021
CREATE TABLE etat_matrimonial_anterieur_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5) NOT NULL,
    region_departement VARCHAR(4) NOT NULL,
    sexe VARCHAR(5) NOT NULL,
    etat_matrimonial VARCHAR(1) NOT NULL,
    nombre_de_maries INT NOT NULL CONSTRAINT nbr_mariage_lt_0 CHECK(nombre_de_maries >= 0)
);

-- D3
CREATE TABLE premier_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5) NOT NULL,
    region_departement VARCHAR(4) NOT NULL,
    groupe_age VARCHAR(5) NOT NULL,
    nombre_de_maries INT NOT NULL CONSTRAINT nbr_mariage_lt_0 CHECK(nombre_de_maries >= 0)
);

-- D4 Nationalité des époux selon le département et la région de domicile conjugal. Année 2021
CREATE TABLE nationalite_epoux (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5) NOT NULL,
    region_departement VARCHAR(4) NOT NULL,
    nationalite_combinee VARCHAR(7) NOT NULL,
    nombre_de_maries INT NOT NULL CONSTRAINT nbr_mariage_lt_0 CHECK(nombre_de_maries >= 0)
);

-- D5
CREATE TABLE pays_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(2) NOT NULL,
    region_departement VARCHAR(4) NOT NULL,
    pays_naissance VARCHAR(7) NOT NULL,
    nombre_de_maries INT NOT NULL CONSTRAINT nbr_mariage_lt_0 CHECK(nombre_de_maries >= 0)
);

-- D6 Répartition mensuelle des mariages selon le département et la région de mariage. Année 2021
CREATE TABLE repartition_mensuelle_mariage (
    id SERIAL PRIMARY KEY,
    type_de_mariage VARCHAR(5) NOT NULL,
    region_departement VARCHAR(4) NOT NULL,
    mois_mariage VARCHAR(2) NOT NULL CONSTRAINT check_mois CHECK(mois_mariage IN ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'AN')),
    nombre_de_maries INT NOT NULL CONSTRAINT nbr_mariage_lt_0 CHECK(nombre_de_maries >= 0)
);

CREATE TABLE statistiques_pop (
    code_commune VARCHAR(5) REFERENCES commune(code),
    annee_debut INT NOT NULL,
    annee_fin INT NOT NULL CONSTRAINT check_annee_fin_sup_annee_debut CHECK(annee_debut <= annee_fin),
    type_statistique VARCHAR(32) NOT NULL,
    valeur FLOAT NOT NULL,

    PRIMARY KEY (code_commune, type_statistique, annee_debut, annee_fin)
);