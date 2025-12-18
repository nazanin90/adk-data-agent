#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Source the .env file to get the PROJECT_ID
if [ -f .env ]; then
  source .env
fi

# Check if project ID is set
if [ -z "$PROJECT_ID" ]; then
  echo "Error: PROJECT_ID is not set in the .env file."
  exit 1
fi

USER_EMAIL=$(gcloud config get-value account)

echo "--- Enabling required Google Cloud services for project: $PROJECT_ID ---"

gcloud services enable geminidataanalytics.googleapis.com --project="$PROJECT_ID"
gcloud services enable cloudaicompanion.googleapis.com --project="$PROJECT_ID"
gcloud services enable bigquery.googleapis.com --project="$PROJECT_ID"

echo "--- Services enabled successfully ---"
echo ""
echo "--- Granting required IAM roles to user: $USER_EMAIL ---"

# Grant Gemini for Google Cloud User role
echo "Granting role: roles/cloudaicompanion.user"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="user:$USER_EMAIL" \
  --role="roles/cloudaicompanion.user" \
  --condition=None

# Grant Looker Instance User role
echo "Granting role: roles/looker.instanceUser"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="user:$USER_EMAIL" \
  --role="roles/looker.instanceUser" \
  --condition=None

# Grant BigQuery User role
echo "Granting role: roles/bigquery.user"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="user:$USER_EMAIL" \
  --role="roles/bigquery.user" \
  --condition=None

# Grant BigQuery Studio User role
echo "Granting role: roles/bigquery.studioUser"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="user:$USER_EMAIL" \
  --role="roles/bigquery.studioUser" \
  --condition=None

# Grant Service Usage Consumer role
echo "Granting role: roles/serviceusage.serviceUsageConsumer"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="user:$USER_EMAIL" \
    --role="roles/serviceusage.serviceUsageConsumer" \
    --condition=None

echo "--- IAM roles granted successfully ---"
echo ""
echo "--- Service enablement and IAM configuration complete! ---"
