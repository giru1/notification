FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --progress-bar off --upgrade pip
RUN pip install --progress-bar off -r requirements.txt
COPY . .
#RUN if [ -n "$MODE" ] && [ "$MODE" = "PROD" ] ; then cat ${WP_PRIVATE_KEY_PROD} > credentials/wp/private_key.pem ; else cat ${WP_PRIVATE_KEY_DEV} > credentials/wp/private_key.pem ; fi
#RUN if [ -n "$MODE" ] && [ "$MODE" = "PROD" ] ; then cat ${WP_PUBLIC_KEY_PROD} > credentials/wp/public_key.pem ; else cat ${WP_PUBLIC_KEY_DEV} > credentials/wp/public_key.pem ; fi
#RUN if [ -n "$MODE" ] && [ "$MODE" = "PROD" ] ; then cat ${WP_SERVER_KEY_PROD} > credentials/wp/server_key ; else cat ${WP_SERVER_KEY_DEV} > credentials/wp/server_key ; fi
#RUN cat ${FCM_CREDS} > credentials/fcm/fcm_cred.json

RUN chmod a+x docker/*.sh
