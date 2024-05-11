-- Update table mariage

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE mariage
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);
ALTER TABLE mariage DROP COLUMN region_departement;

-- Update table premier_mariage

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE premier_mariage
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);
ALTER TABLE premier_mariage DROP COLUMN region_departement;

-- Update table pays_mariage

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE pays_mariage
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);
ALTER TABLE pays_mariage DROP COLUMN region_departement;

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE etat_matrimonial_anterieur_mariage
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);
ALTER TABLE etat_matrimonial_anterieur_mariage DROP COLUMN region_departement;

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE nationalite_epoux
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);
ALTER TABLE nationalite_epoux DROP COLUMN region_departement;

-- On coupe les REGDEP_MAR et REGDEP_DOMI pour avoir les codes région et département
UPDATE repartition_mensuelle_mariage
SET idreg = LEFT(region_departement, 2),
    iddep = RIGHT(region_departement, 2);
ALTER TABLE repartition_mensuelle_mariage DROP COLUMN region_departement;