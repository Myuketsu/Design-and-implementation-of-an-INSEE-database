-- Update table mariage

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE mariage
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);


-- Update table premier_mariage

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE premier_mariage
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);

-- Update table pays_mariage

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE pays_mariage
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);

-- Update table population

UPDATE population
SET iddep = LEFT(departement_commune, 2),
    idcommune = RIGHT(departement_commune, 3);