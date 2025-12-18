CREATE TABLE `patient_records.medication_inventory`
(
  pharmacy_id STRING OPTIONS(description="Unique ID for the pharmacy location."),
  pharmacy_name STRING OPTIONS(description="Name of the pharmacy chain (e.g., CVS, Walgreens)."),
  zip_code STRING OPTIONS(description="5-digit zip code of the pharmacy."),
  medication_name STRING OPTIONS(description="Name of the medication (matches clinical records)."),
  stock_level INT64 OPTIONS(description="Current number of units in stock."),
  last_updated TIMESTAMP OPTIONS(description="When this stock level was last checked.")
);


INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Atorvastatin', 65, TIMESTAMP_MICROS(1762585448536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Lisinopril', 92, TIMESTAMP_MICROS(1762584968536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Gabapentin', 36, TIMESTAMP_MICROS(1762584008536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Levothyroxine', 21, TIMESTAMP_MICROS(1762584908536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Ibuprofen', 6, TIMESTAMP_MICROS(1762586168536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Albuterol', 0, TIMESTAMP_MICROS(1762585988536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Atorvastatin', 61, TIMESTAMP_MICROS(1762587008536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Amoxicillin', 0, TIMESTAMP_MICROS(1762585628536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Ibuprofen', 0, TIMESTAMP_MICROS(1762584788536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Atorvastatin', 4, TIMESTAMP_MICROS(1762587368536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Sertraline', 69, TIMESTAMP_MICROS(1762586228536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Omeprazole', 93, TIMESTAMP_MICROS(1762587128536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Metformin', 34, TIMESTAMP_MICROS(1762585028536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Metformin', 26, TIMESTAMP_MICROS(1762586408536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Omeprazole', 27, TIMESTAMP_MICROS(1762586108536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Omeprazole', 77, TIMESTAMP_MICROS(1762586948536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Omeprazole', 79, TIMESTAMP_MICROS(1762585268536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Sertraline', 0, TIMESTAMP_MICROS(1762584668536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Ibuprofen', 67, TIMESTAMP_MICROS(1762585208536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Metformin', 0, TIMESTAMP_MICROS(1762585748536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Ibuprofen', 41, TIMESTAMP_MICROS(1762584788536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Sertraline', 54, TIMESTAMP_MICROS(1762585808536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Lisinopril', 21, TIMESTAMP_MICROS(1762586708536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Amoxicillin', 64, TIMESTAMP_MICROS(1762586888536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Amoxicillin', 23, TIMESTAMP_MICROS(1762586288536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Gabapentin', 3, TIMESTAMP_MICROS(1762584908536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Lisinopril', 60, TIMESTAMP_MICROS(1762584608536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Metformin', 91, TIMESTAMP_MICROS(1762585388536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Lisinopril', 65, TIMESTAMP_MICROS(1762584968536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Gabapentin', 0, TIMESTAMP_MICROS(1762584068536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Albuterol', 16, TIMESTAMP_MICROS(1762584368536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Atorvastatin', 0, TIMESTAMP_MICROS(1762585388536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Albuterol', 21, TIMESTAMP_MICROS(1762586408536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Sertraline', 38, TIMESTAMP_MICROS(1762585808536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Levothyroxine', 93, TIMESTAMP_MICROS(1762584068536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Levothyroxine', 0, TIMESTAMP_MICROS(1762585868536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Atorvastatin', 37, TIMESTAMP_MICROS(1762584488536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Gabapentin', 36, TIMESTAMP_MICROS(1762586408536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Levothyroxine', 90, TIMESTAMP_MICROS(1762586708536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Metformin', 3, TIMESTAMP_MICROS(1762586648536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Albuterol', 13, TIMESTAMP_MICROS(1762586768536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Levothyroxine', 26, TIMESTAMP_MICROS(1762586108536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Amoxicillin', 69, TIMESTAMP_MICROS(1762584548536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Albuterol', 92, TIMESTAMP_MICROS(1762586288536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Lisinopril', 36, TIMESTAMP_MICROS(1762584308536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-004', 'CVS Pharmacy', '10002', 'Gabapentin', 76, TIMESTAMP_MICROS(1762584968536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-002', 'Walgreens', '10001', 'Amoxicillin', 90, TIMESTAMP_MICROS(1762586948536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-003', 'Rite Aid', '10002', 'Omeprazole', 50, TIMESTAMP_MICROS(1762586228536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-001', 'CVS Pharmacy', '10001', 'Sertraline', 53, TIMESTAMP_MICROS(1762585688536530));
INSERT INTO `patient_records.medication_inventory` (pharmacy_id, pharmacy_name, zip_code, medication_name, stock_level, last_updated) VALUES ('ph-005', 'Local Health Mart', '10003', 'Ibuprofen', 0, TIMESTAMP_MICROS(1762584128536530));
