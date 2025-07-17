# Izipay - API CyberSource

## 1. Clone repository

* Clone tradicional

    ```sh
     git clone https://github.com/fsumari/dev-dataops-api-cyber.git
    ```

* Or clone with Personal Token
  
    ```sh
    GITHUB_REPOSITORY=github.com/fsumari/dev-dataops-api-cyber.git
    GITHUB_TOKEN=xxxxxxxxxxxxxxx
    GITHUB_USERNAME=xxxxxxxxxxxxx
    git clone https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@${GITHUB_REPOSITORY}
    ```

## 2. Crear Service Account

Crear SA con el siguiente comando:

```
gcloud iam service-accounts create prd-dataops-apis-izipay-int \
  --display-name "Service account para DataOps APIs para ser usando internamente en Izipay"
```
## 3. Crear el bucket de forma manual

nombre del bucket: prd-ingesta-izipay-fx32

## 4. Dar permisos a la Service Account

Obtener el ID del projecto.

```
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value core/project)
```
Permisos sencillos en el projecto por defecto:

```
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:prd-dataops-apis-izipay-int@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/storage.objectCreator"

gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:prd-dataops-apis-izipay-int@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:prd-dataops-apis-izipay-int@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:prd-dataops-apis-izipay-int@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/viewer"
```

```
Permisos de User para las Cloud Storage en el Projeto prd-izipay-data-storage:

```
gcloud storage buckets add-iam-policy-binding prd-ingesta-izipay-fx32 \
  --member="serviceAccount:prd-dataops-apis-izipay-int@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/storage.objectCreator" \
  --project=prd-izipay-data-storage
```

## 4. Deploy

    ```sh
     cd service_api
     bash deploy.sh
     bash job-cyber-trr-dayli.sh
     bash job-cyber-dmdr-low-diario.sh
     bash job-cyber-dmdr-high-diario.sh
    ```
