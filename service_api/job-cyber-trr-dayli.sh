
PROJECT_ID="dev-izipay-advanced-analytics"
JOB_NAME="job_api_cyber_trr_daily_3am"
REGION="us-central1"
CRON_SCHEDULE="10 3 * * *"
TIME_ZONE="America/Lima"
RUN_URL="https://dev-izi-cyber-api-v1-dl7olq7kiq-uc.a.run.app/cyber"
FECHA=$(date +%F)

BODY="{
    \"organization_id\": \"izipay_master_acct\",
    \"merchant_key_id\": \"98c3b49d-0dc0-4a35-933c-0037d1789462\",
    \"merchant_secret_key_id\": \"/mxDSoyXaym+HDoVtqPm8zbdQ3Poos3CO3ZHlIEHOxc==\",
    \"report_name\": \"TRR_daily\",
    \"fecha\": \"$FECHA\"
}"

echo $BODY

HEADERS='Content-Type=application/json, token=izi-cyber-token-7rMVpUvdo8T3BlbkFJvlPEtwcw'

gcloud scheduler jobs create http $JOB_NAME \
  --project=$PROJECT_ID \
  --location=$REGION \
  --schedule="$CRON_SCHEDULE" \
  --time-zone="$TIME_ZONE" \
  --uri="$RUN_URL" \
  --http-method=POST \
  --message-body="$BODY" \
  --headers="$HEADERS"
