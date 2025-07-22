
PROJECT_ID=$GCP_PROJECT_ID
JOB_NAME="job_api_cyber_dmdr_high_diario_3am"
REGION="us-central1"
CRON_SCHEDULE="30 3 * * *"
TIME_ZONE="America/Lima"
RUN_URL=$ENDPOINT

BODY="{
    \"organization_id\": \"izipay_high\",
    \"merchant_key_id\": \"a8fe761c-6179-487c-863b-ffb2dc03e2b1\",
    \"merchant_secret_key_id\": \"pPudDBsvHEvvzh7LZAj/1td0FwnWLhQnDZsCnik2HbM=\",
    \"report_name\": \"DMDR-HIGH-DIARIO\"
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
