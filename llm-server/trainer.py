from dotenv import load_dotenv
from google.cloud import storage
import base64
import json
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

from PIL import Image
from io import BytesIO

import os 
import json 
import joblib 

load_dotenv(override=True)
BUCKET_NAME: str = os.getenv("BUCKET_NAME")

gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

images_blob = bucket.blob(os.path.join(
    "TRAINING_DATA",
    "train.json"
))

with images_blob.open("r") as fp: 
    train = json.load(fp) 

features = []
labels = []

for item in train:
    if isinstance(item, list): 
        for book_item in item: 
            img_data = base64.b64decode(book_item['img_b64'])
            img = Image.open(BytesIO(img_data)).convert('L')

            img_resized = img.resize((1240, 1240))

            img_array = np.array(img_resized).flatten()
            features.append(img_array)

            labels.append(int(book_item['label']))
    else: 
        img_data = base64.b64decode(item['img_b64'])
        img = Image.open(BytesIO(img_data)).convert('L')

        img_resized = img.resize((1240, 1240))

        img_array = np.array(img_resized).flatten()
        features.append(img_array)

        labels.append(int(item['label']))

X = np.array(features)
y = np.array(labels)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier( eval_metric="logloss", random_state=0)
model.fit(X_train, y_train)

model_blob = bucket.blob(os.path.join(
    "TRAINING_DATA", 
    "model.joblib"
))

report_blob = bucket.blob(os.path.join(
   "TRAINING_DATA", 
   "report.txt" 
))

y_pred = model.predict(X_test)

with model_blob.open("wb") as fp: 
    joblib.dump(model, fp)

with report_blob.open("w") as fp: 
    fp.write(classification_report(y_test, y_pred))
