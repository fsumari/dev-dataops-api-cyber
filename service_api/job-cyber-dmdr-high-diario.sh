
PROJECT_ID="dev-izipay-advanced-analytics"
JOB_NAME="job_api_cyber_dmdr_high_diario_3am"
REGION="us-central1"
CRON_SCHEDULE="30 3 * * *"
TIME_ZONE="America/Lima"
RUN_URL="https://dev-izi-cyber-api-v1-dl7olq7kiq-uc.a.run.app/cyber"
FECHA=$(date +%F)

BODY="{
    \"organization_id\": \"izipay_high\",
    \"merchant_key_id\": \"a8fe761c-6179-487c-863b-ffb2dc03e2b1\",
    \"merchant_secret_key_id\": \"pPudDBsvHEvvzh7LZAj/1td0FwnWLhQnDZsCnik2HbM=\",
    \"report_name\": \"DMDR-HIGH-DIARIO\",
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
