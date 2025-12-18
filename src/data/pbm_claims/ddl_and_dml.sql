CREATE TABLE `patient_records.pbm_claims`
(
  claim_id STRING OPTIONS(description="Unique ID for the claim transaction."),
  patient_id STRING OPTIONS(description="ID of the patient."),
  medication_name STRING OPTIONS(description="Drug name requested."),
  insurance_plan STRING OPTIONS(description="Insurance plan name."),
  approval_status STRING OPTIONS(description="Status: Approved, Rejected, Pending."),
  copay_amount FLOAT64 OPTIONS(description="Patient out-of-pocket cost."),
  rejection_reason STRING OPTIONS(description="Reason for rejection (if applicable)."),
  claim_date TIMESTAMP OPTIONS(description="Date of claim processing.")
);

-- Inserting Data: Mix of Approved and Rejected claims across different plans
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1001', 'pat-055', 'Atorvastatin', 'BlueCross Gold', 'Approved', 10.00, NULL, TIMESTAMP_MICROS(1762585448536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1002', 'pat-089', 'Lisinopril', 'Aetna Silver', 'Approved', 15.50, NULL, TIMESTAMP_MICROS(1762584968536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1003', 'pat-012', 'Gabapentin', 'UnitedHealth Basic', 'Rejected', 0.00, 'Prior Auth Required', TIMESTAMP_MICROS(1762584008536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1004', 'pat-055', 'Levothyroxine', 'BlueCross Gold', 'Approved', 10.00, NULL, TIMESTAMP_MICROS(1762584908536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1005', 'pat-101', 'Ibuprofen', 'Medicare Part D', 'Approved', 2.00, NULL, TIMESTAMP_MICROS(1762586168536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1006', 'pat-022', 'Albuterol', 'Aetna Silver', 'Rejected', 0.00, 'Not on Formulary', TIMESTAMP_MICROS(1762585988536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1007', 'pat-055', 'Metformin', 'BlueCross Gold', 'Approved', 5.00, NULL, TIMESTAMP_MICROS(1762587008536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1008', 'pat-099', 'Amoxicillin', 'UnitedHealth Basic', 'Approved', 25.00, NULL, TIMESTAMP_MICROS(1762585628536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1009', 'pat-055', 'Ozempic', 'BlueCross Gold', 'Rejected', 0.00, 'Step Therapy Required', TIMESTAMP_MICROS(1762584788536530));
INSERT INTO `patient_records.pbm_claims` (claim_id, patient_id, medication_name, insurance_plan, approval_status, copay_amount, rejection_reason, claim_date) VALUES ('CLM-1010', 'pat-034', 'Atorvastatin', 'Medicare Part D', 'Approved', 1.50, NULL, TIMESTAMP_MICROS(1762587368536530));
