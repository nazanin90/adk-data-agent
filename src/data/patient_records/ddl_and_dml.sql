-- DDL
CREATE TABLE patient_records.patient_encounters (
  -- Patient Info
  patient_id STRING,
  patient_name STRING,
  patient_gender STRING,
  patient_birth_date DATE,
  patient_address STRING,

  -- Encounter Info
  encounter_id STRING,
  encounter_class STRING,
  encounter_period_start TIMESTAMP,
  encounter_period_end TIMESTAMP,

  -- Practitioner Info
  practitioner_id STRING,
  practitioner_name STRING,
  practitioner_role STRING,
  practitioner_specialty STRING,

  -- Event Type
  event_type STRING OPTIONS(description="The type of event (e.g., 'Condition', 'Observation', 'Medication', 'MedicationAdministration')."),

  -- Condition Fields (NULL if not a Condition event)
  condition_id STRING,
  condition_display_name STRING,
  condition_code STRING,

  -- Observation Fields (NULL if not an Observation event)
  observation_id STRING,
  observation_display_name STRING,
  observation_value STRING,
  observation_unit STRING,

  -- Procedure Fields (NULL if not a Procedure event)
  procedure_id STRING,
  procedure_display_name STRING,
  procedure_code STRING,

  -- Medication Request Fields (NULL if not a 'Medication' event)
  medication_request_id STRING,
  medication_display_name STRING,
  medication_dosage_instruction STRING,
  medication_request_timestamp TIMESTAMP OPTIONS(description="The exact date and time the medication was ordered/prescribed."),

  -- Medication Administration Fields (NULL if not a 'MedicationAdministration' event)
  medication_admin_status STRING OPTIONS(description="Status of the administration (e.g., 'Given', 'Held', 'Patient Refused')."),
  medication_admin_timestamp TIMESTAMP OPTIONS(description="The exact date and time the medication was administered or recorded as not given."),
  medication_admin_notes STRING OPTIONS(description="Any notes from the nurse (e.g., 'Patient refused due to nausea')."),
  medication_admin_linked_request_id STRING OPTIONS(description="The 'medication_request_id' this administration fulfills.")
);

-- End

-- DML

INSERT INTO patient_records.patient_encounters (
  patient_id, patient_name, patient_gender, patient_birth_date, patient_address,
  encounter_id, encounter_class, encounter_period_start, encounter_period_end,
  practitioner_id, practitioner_name, practitioner_role, practitioner_specialty,
  event_type,
  condition_id, condition_display_name, condition_code,
  observation_id, observation_display_name, observation_value, observation_unit,
  procedure_id, procedure_display_name, procedure_code,
  medication_request_id, medication_display_name, medication_dosage_instruction, medication_request_timestamp,
  medication_admin_status, medication_admin_timestamp, medication_admin_notes, medication_admin_linked_request_id
)

WITH DataPools AS (
  SELECT
   -- 1. Patients
   [STRUCT('p-001' AS id, 'James Smith' AS name, 'male' AS gender, DATE('1975-04-12') AS birth_date, '123 Main St' AS address),
    STRUCT('p-002' AS id, 'Mary Johnson' AS name, 'female' AS gender, DATE('1988-11-02') AS birth_date, '456 Oak Ave'),
    STRUCT('p-003' AS id, 'Robert Williams' AS name, 'male' AS gender, DATE('1952-07-30') AS birth_date, '789 Pine Ln'),
    STRUCT('p-004' AS id, 'Patricia Brown' AS name, 'female' AS gender, DATE('1991-01-15') AS birth_date, '101 Maple Dr'),
    STRUCT('p-005' AS id, 'John Jones' AS name, 'male' AS gender, DATE('1963-09-22') AS birth_date, '202 Cedar Pl'),
    STRUCT('p-006' AS id, 'Jennifer Garcia' AS name, 'female' AS gender, DATE('1982-03-14') AS birth_date, '303 Elm Blvd'),
    STRUCT('p-007' AS id, 'Michael Miller' AS name, 'male' AS gender, DATE('1995-08-20') AS birth_date, '404 Birch Ct'),
    STRUCT('p-008' AS id, 'Linda Davis' AS name, 'female' AS gender, DATE('1967-12-01') AS birth_date, '505 Spruce Way'),
    STRUCT('p-009' AS id, 'William Rodriguez' AS name, 'male' AS gender, DATE('1978-05-19') AS birth_date, '606 Aspen Pl'),
    STRUCT('p-010' AS id, 'Elizabeth Martinez' AS name, 'female' AS gender, DATE('2001-02-28') AS birth_date, '707 Walnut Cir'),
    STRUCT('p-011' AS id, 'David Hernandez' AS name, 'male' AS gender, DATE('1985-10-10') AS birth_date, '808 Cherry Ln'),
    STRUCT('p-012' AS id, 'Barbara Lopez' AS name, 'female' AS gender, DATE('1959-06-07') AS birth_date, '909 Poplar St'),
    STRUCT('p-013' AS id, 'Richard Gonzalez' AS name, 'male' AS gender, DATE('1999-04-30') AS birth_date, '111 Redwood Dr'),
    STRUCT('p-014' AS id, 'Susan Wilson' AS name, 'female' AS gender, DATE('1973-11-12') AS birth_date, '222 Sequoia Ave'),
    STRUCT('p-015' AS id, 'Joseph Anderson' AS name, 'male' AS gender, DATE('1980-01-05') AS birth_date, '333 Willow Rd'),
    STRUCT('p-016' AS id, 'Jessica Thomas' AS name, 'female' AS gender, DATE('1992-02-18') AS birth_date, '444 Birchview Dr'),
    STRUCT('p-017' AS id, 'Thomas Taylor' AS name, 'male' AS gender, DATE('1966-08-25') AS birth_date, '555 Pineneedle Rd'),
    STRUCT('p-018' AS id, 'Sarah Moore' AS name, 'female' AS gender, DATE('1987-12-30') AS birth_date, '666 Oakhill Ave'),
    STRUCT('p-019' AS id, 'Charles Jackson' AS name, 'male' AS gender, DATE('1971-05-09') AS birth_date, '777 Maplewood Ln'),
    STRUCT('p-020' AS id, 'Karen Martin' AS name, 'female' AS gender, DATE('1998-10-17') AS birth_date, '888 Cedar Crest')] AS patients,

   -- 2. Doctors
   [STRUCT('d-101' AS id, 'Dr. Emily Williams' AS name, 'Doctor' AS role, 'Cardiology' AS specialty),
    STRUCT('d-102' AS id, 'Dr. Michael Brown' AS name, 'Doctor' AS role, 'Orthopedics' AS specialty),
    STRUCT('d-103' AS id, 'Dr. David Wilson' AS name, 'Doctor' AS role, 'Neurology' AS specialty),
    STRUCT('d-104' AS id, 'Dr. Linda Harris' AS name, 'Doctor' AS role, 'Pediatrics' AS specialty),
    STRUCT('d-105' AS id, 'Dr. John Smith' AS name, 'Doctor' AS role, 'General Practice' AS specialty),
    STRUCT('d-106' AS id, 'Dr. Robert Garcia' AS name, 'Doctor' AS role, 'Oncology' AS specialty),
    STRUCT('d-107' AS id, 'Dr. Susan Clark' AS name, 'Doctor' AS role, 'Endocrinology' AS specialty),
    STRUCT('d-108' AS id, 'Dr. James Lee' AS name, 'Doctor' AS role, 'Pulmonology' AS specialty),
    STRUCT('d-109' AS id, 'Dr. Patricia Allen' AS name, 'Doctor' AS role, 'Gastroenterology' AS specialty),
    STRUCT('d-110' AS id, 'Dr. Christopher Young' AS name, 'Doctor' AS role, 'Psychiatry' AS specialty)] AS doctors,

   -- 3. Nurses
   [STRUCT('n-201' AS id, 'Sarah Jenkins' AS name, 'Nurse' AS role, 'RN' AS specialty),
    STRUCT('n-202' AS id, 'Paul Anderson' AS name, 'Nurse' AS role, 'LPN' AS specialty),
    STRUCT('n-203' AS id, 'Nancy Green' AS name, 'Nurse' AS role, 'RN' AS specialty),
    STRUCT('n-204' AS id, 'Mark Roberts' AS name, 'Nurse' AS role, 'NP' AS specialty),
    STRUCT('n-205' AS id, 'Laura Adams' AS name, 'Nurse' AS role, 'RN' AS specialty),
    STRUCT('n-206' AS id, 'Kevin Baker' AS name, 'Nurse' AS role, 'RN' AS specialty),
    STRUCT('n-207' AS id, 'Michelle Nelson' AS name, 'Nurse' AS role, 'LPN' AS specialty),
    STRUCT('n-208' AS id, 'Brian Carter' AS name, 'Nurse' AS role, 'RN' AS specialty),
    STRUCT('n-209' AS id, 'Helen Mitchell' AS name, 'Nurse' AS role, 'NP' AS specialty),
    STRUCT('n-210' AS id, 'George Roberts' AS name, 'Nurse' AS role, 'RN' AS specialty)] AS nurses,

   -- 4. Conditions
   [STRUCT('Hypertension' AS name, 'I10' AS code),
    STRUCT('Type 2 diabetes' AS name, 'E11' AS code),
    STRUCT('Acute bronchitis' AS name, 'J20.9' AS code),
    STRUCT('Anxiety' AS name, 'F41.1' AS code),
    STRUCT('Asthma' AS name, 'J45' AS code),
    STRUCT('Hyperlipidemia' AS name, 'E78.5' AS code),
    STRUCT('Major depressive disorder' AS name, 'F32.9' AS code),
    STRUCT('Gastroesophageal reflux disease' AS name, 'K21.9' AS code),
    STRUCT('Osteoarthritis' AS name, 'M19.9' AS code),
    STRUCT('COPD' AS name, 'J44.9' AS code),
    STRUCT('Migraine' AS name, 'G43.9' AS code),
    STRUCT('Pneumonia' AS name, 'J18.9' AS code)] AS conditions,

   -- 5. Procedures
   [STRUCT('Vaccination' AS name, '90471' AS code),
    STRUCT('Blood test' AS name, '85025' AS code),
    STRUCT('X-ray of chest' AS name, '71045' AS code),
    STRUCT('Electrocardiogram' AS name, '93000' AS code),
    STRUCT('Colonoscopy' AS name, '45378' AS code),
    STRUCT('Echocardiogram' AS name, '93306' AS code),
    STRUCT('Physical therapy eval' AS name, '97161' AS code),
    STRUCT('MRI of brain' AS name, '70551' AS code),
    STRUCT('CT scan of abdomen' AS name, '74176' AS code),
    STRUCT('Appendectomy' AS name, '44950' AS code)] AS procedures,

    -- 6. Observations
   [STRUCT('Body Temperature' AS name, 'C' AS unit),
    STRUCT('Heart rate' AS name, 'bpm' AS unit),
    STRUCT('Blood Pressure' AS name, 'mmHg' AS unit),
    STRUCT('Respiratory rate' AS name, 'breaths/min' AS unit),
    STRUCT('Oxygen saturation' AS name, '%' AS unit),
    STRUCT('Pain score' AS name, '0-10' AS unit),
    STRUCT('Blood Glucose' AS name, 'mg/dL' AS unit)] AS observations,

   -- 7. Medications
   [STRUCT('Lisinopril' AS name, '10 mg tablet, 1 tablet daily' AS dose),
    STRUCT('Metformin' AS name, '500 mg tablet, 1 tablet twice daily' AS dose),
    STRUCT('Atorvastatin' AS name, '20 mg tablet, 1 tablet at bedtime' AS dose),
    STRUCT('Amoxicillin' AS name, '500 mg capsule, 1 capsule 3 times daily' AS dose),
    STRUCT('Albuterol' AS name, '90 mcg inhaler, 2 puffs every 4 hours as needed' AS dose),
    STRUCT('Sertraline' AS name, '50 mg tablet, 1 tablet daily' AS dose),
    STRUCT('Omeprazole' AS name, '20 mg capsule, 1 capsule daily' AS dose),
    STRUCT('Ibuprofen' AS name, '400 mg tablet, as needed for pain' AS dose),
    STRUCT('Levothyroxine' AS name, '100 mcg tablet, 1 tablet daily' AS dose),
    STRUCT('Gabapentin' AS name, '300 mg capsule, 3 times daily' AS dose)] AS medications
),

-- 2. Encounters (High Volume)
Encounters AS (
  SELECT
    p.id AS patient_id, p.name AS patient_name, p.gender AS patient_gender, p.birth_date AS patient_birth_date, p.address AS patient_address,
    GENERATE_UUID() AS encounter_id,
    (ARRAY['ambulatory', 'inpatient', 'emergency'])[OFFSET(CAST(RAND() * 2 AS INT64))] AS encounter_class,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL CAST(1 + RAND() * 365*3 AS INT64) DAY) AS encounter_start,
    pools.doctors[OFFSET(CAST(RAND() * (ARRAY_LENGTH(pools.doctors) - 1) AS INT64))] AS doctor,
    pools.nurses[OFFSET(CAST(RAND() * (ARRAY_LENGTH(pools.nurses) - 1) AS INT64))] AS nurse
  FROM DataPools AS pools, UNNEST(pools.patients) AS p
  CROSS JOIN UNNEST(GENERATE_ARRAY(1, 100 + CAST(RAND() * 100 AS INT64))) AS encounter_num
),

BaseEvents AS (
  SELECT *, TIMESTAMP_ADD(encounter_start, INTERVAL CAST(1 + RAND() * 72 AS INT64) HOUR) AS encounter_end FROM Encounters
),

-- 4a. Conditions
ConditionEvents AS (
  SELECT
    b.patient_id, b.patient_name, b.patient_gender, b.patient_birth_date, b.patient_address,
    b.encounter_id, b.encounter_class, b.encounter_start AS encounter_period_start, b.encounter_end AS encounter_period_end,
    b.doctor.id AS practitioner_id, b.doctor.name AS practitioner_name, b.doctor.role AS practitioner_role, b.doctor.specialty AS practitioner_specialty,
    'Condition' AS event_type,
    GENERATE_UUID() AS condition_id, c.name AS condition_display_name, c.code AS condition_code,
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS TIMESTAMP),
    CAST(NULL AS STRING), CAST(NULL AS TIMESTAMP), CAST(NULL AS STRING), CAST(NULL AS STRING)
  FROM BaseEvents AS b
  CROSS JOIN DataPools AS pools
  CROSS JOIN UNNEST(GENERATE_ARRAY(1, 1 + CAST(RAND() * 2 AS INT64))) AS event_num
  LEFT JOIN UNNEST([pools.conditions[OFFSET(CAST(RAND() * (ARRAY_LENGTH(pools.conditions) - 1) AS INT64))]]) AS c
),

-- 4b. Observations
ObservationEvents AS (
  SELECT
    b.patient_id, b.patient_name, b.patient_gender, b.patient_birth_date, b.patient_address,
    b.encounter_id, b.encounter_class, b.encounter_start AS encounter_period_start, b.encounter_end AS encounter_period_end,
    b.nurse.id AS practitioner_id, b.nurse.name AS practitioner_name, b.nurse.role AS practitioner_role, b.nurse.specialty AS practitioner_specialty,
    'Observation' AS event_type,
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    GENERATE_UUID() AS observation_id,
    o.name AS observation_display_name,
    CASE o.name
      WHEN 'Body Temperature' THEN FORMAT("%.1f", 36.5 + RAND() * 2)
      WHEN 'Heart rate' THEN CAST(CAST(60 + RAND() * 40 AS INT64) AS STRING)
      WHEN 'Blood Pressure' THEN CAST(CAST(110 + RAND() * 20 AS INT64) AS STRING) || '/' || CAST(CAST(70 + RAND() * 15 AS INT64) AS STRING)
      WHEN 'Respiratory rate' THEN CAST(CAST(12 + RAND() * 8 AS INT64) AS STRING)
      WHEN 'Oxygen saturation' THEN CAST(CAST(95 + RAND() * 5 AS INT64) AS STRING)
      WHEN 'Pain score' THEN CAST(CAST(RAND() * 10 AS INT64) AS STRING)
      WHEN 'Blood Glucose' THEN CAST(CAST(70 + RAND() * 130 AS INT64) AS STRING)
    END AS observation_value,
    o.unit AS observation_unit,
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS TIMESTAMP),
    CAST(NULL AS STRING), CAST(NULL AS TIMESTAMP), CAST(NULL AS STRING), CAST(NULL AS STRING)
  FROM BaseEvents AS b
  CROSS JOIN DataPools AS pools
  CROSS JOIN UNNEST(GENERATE_ARRAY(1, 2 + CAST(RAND() * 3 AS INT64))) AS event_num
  LEFT JOIN UNNEST([pools.observations[OFFSET(CAST(RAND() * (ARRAY_LENGTH(pools.observations) - 1) AS INT64))]]) AS o
),

-- 4c. Procedures
ProcedureEvents AS (
  SELECT
    b.patient_id, b.patient_name, b.patient_gender, b.patient_birth_date, b.patient_address,
    b.encounter_id, b.encounter_class, b.encounter_start AS encounter_period_start, b.encounter_end AS encounter_period_end,
    b.doctor.id AS practitioner_id, b.doctor.name AS practitioner_name, b.doctor.role AS practitioner_role, b.doctor.specialty AS practitioner_specialty,
    'Procedure' AS event_type,
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    GENERATE_UUID() AS procedure_id, p.name AS procedure_display_name, p.code AS procedure_code,
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS TIMESTAMP),
    CAST(NULL AS STRING), CAST(NULL AS TIMESTAMP), CAST(NULL AS STRING), CAST(NULL AS STRING)
  FROM BaseEvents AS b
  CROSS JOIN DataPools AS pools
  CROSS JOIN UNNEST(GENERATE_ARRAY(1, 1 + CAST(RAND() * 1 AS INT64))) AS event_num
  LEFT JOIN UNNEST([pools.procedures[OFFSET(CAST(RAND() * (ARRAY_LENGTH(pools.procedures) - 1) AS INT64))]]) AS p
  WHERE RAND() < 0.8
),

-- 4d. Medication Base
MedicationRequestBase AS (
  SELECT
    b.*,
    GENERATE_UUID() AS medication_request_id,
    m.name AS medication_display_name,
    m.dose AS medication_dosage_instruction,
    TIMESTAMP_ADD(b.encounter_start, INTERVAL CAST(15 + RAND() * 120 AS INT64) MINUTE) AS medication_request_timestamp
  FROM BaseEvents AS b
  CROSS JOIN DataPools AS pools
  CROSS JOIN UNNEST(GENERATE_ARRAY(1, 1 + CAST(RAND() * 2 AS INT64))) AS event_num
  LEFT JOIN UNNEST([pools.medications[OFFSET(CAST(RAND() * (ARRAY_LENGTH(pools.medications) - 1) AS INT64))]]) AS m
  WHERE RAND() < 0.75
),

-- 4e. Unpivot Medication Events (INCREASED ANOMALY RATE)
MedicationEvents_Combined AS (
  SELECT
    mr.patient_id, mr.patient_name, mr.patient_gender, mr.patient_birth_date, mr.patient_address,
    mr.encounter_id, mr.encounter_class, mr.encounter_start AS encounter_period_start, mr.encounter_end AS encounter_period_end,
    CASE WHEN event_type = 'Medication' THEN mr.doctor.id WHEN event_type = 'MedicationAdministration' THEN mr.nurse.id END AS practitioner_id,
    CASE WHEN event_type = 'Medication' THEN mr.doctor.name WHEN event_type = 'MedicationAdministration' THEN mr.nurse.name END AS practitioner_name,
    CASE WHEN event_type = 'Medication' THEN mr.doctor.role WHEN event_type = 'MedicationAdministration' THEN mr.nurse.role END AS practitioner_role,
    CASE WHEN event_type = 'Medication' THEN mr.doctor.specialty WHEN event_type = 'MedicationAdministration' THEN mr.nurse.specialty END AS practitioner_specialty,
    event_type,
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING),
    CASE WHEN event_type = 'Medication' THEN mr.medication_request_id ELSE CAST(NULL AS STRING) END AS medication_request_id,
    CASE WHEN event_type = 'Medication' THEN mr.medication_display_name ELSE CAST(NULL AS STRING) END AS medication_display_name,
    CASE WHEN event_type = 'Medication' THEN mr.medication_dosage_instruction ELSE CAST(NULL AS STRING) END AS medication_dosage_instruction,
    CASE WHEN event_type = 'Medication' THEN mr.medication_request_timestamp ELSE CAST(NULL AS TIMESTAMP) END AS medication_request_timestamp,
    -- 56% Given, 14% Held, 30% Refused
    CASE WHEN event_type = 'MedicationAdministration' THEN (IF(RAND() < 0.3, 'Patient Refused', IF(RAND() < 0.8, 'Given', 'Held'))) ELSE CAST(NULL AS STRING) END AS medication_admin_status,
    CASE WHEN event_type = 'MedicationAdministration' THEN TIMESTAMP_ADD(mr.medication_request_timestamp, INTERVAL CAST(10 + RAND() * 240 AS INT64) MINUTE) ELSE CAST(NULL AS TIMESTAMP) END AS medication_admin_timestamp,
    CASE WHEN event_type = 'MedicationAdministration' THEN (IF(RAND() < 0.3, 'Patient refused due to nausea', IF(RAND() < 0.8, 'Patient tolerated well', 'Held due to vitals'))) ELSE CAST(NULL AS STRING) END AS medication_admin_notes,
    CASE WHEN event_type = 'MedicationAdministration' THEN mr.medication_request_id ELSE CAST(NULL AS STRING) END AS medication_admin_linked_request_id
  FROM MedicationRequestBase AS mr
  CROSS JOIN UNNEST(['Medication', 'MedicationAdministration']) AS event_type
  WHERE event_type = 'Medication' OR (event_type = 'MedicationAdministration' AND RAND() < 0.95)
)

SELECT * FROM ConditionEvents
UNION ALL SELECT * FROM ObservationEvents
UNION ALL SELECT * FROM ProcedureEvents
UNION ALL SELECT * FROM MedicationEvents_Combined;

-- End DML
