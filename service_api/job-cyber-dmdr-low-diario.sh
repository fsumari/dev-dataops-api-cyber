
PROJECT_ID=$GCP_PROJECT_ID
JOB_NAME="job_api_cyber_dmdr_low_diario_3am"
REGION="us-central1"
CRON_SCHEDULE="20 3 * * *"
TIME_ZONE="America/Lima"
RUN_URL=$ENDPOINT

BODY="{
    \"organization_id\": \"izipay_low\",
    \"merchant_key_id\": \"a4a51476-564b-41f8-b95a-50a3374dfd2e\",
    \"merchant_secret_key_id\": \"JnlUrHHtGXf41VBWilrJP74CXx7mDCqrHMMQztMVlsk=\",
    \"report_name\": \"DMDR-LOW-DIARIO\"
}"

echo $BODY

HEADERS="Content-Type=application/json, token=$SECRET_TOKEN"

gcloud scheduler jobs create http $JOB_NAME \
  --project=$PROJECT_ID \
  --location=$REGION \
  --schedule="$CRON_SCHEDULE" \
  --time-zone="$TIME_ZONE" \
  --uri="$RUN_URL" \
  --http-method=POST \
  --message-body="$BODY" \
  --headers="$HEADERS"
