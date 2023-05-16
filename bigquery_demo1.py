# Author:        Jake Peters
# Date Created:  May 2023
# Date Modified: May 2023
# Description:   
#                This script demonstrates a method of downloading data from 
#                a BigQuery View or Table using Google's Python client library, 
#                google.cloud. This demo was was prepared for the Connect Coordinating 
#                Center's Feedback and Review (F&R) meeting in May 2023.
# References:         
# 
# Before using this example, you must install/set-up the gcloud CLI: 
#      - Instructions: https://cloud.google.com/sdk/docs/install


import subprocess
import google.auth
from google.cloud import bigquery

# Authenticate and construct a BigQuery client object.
project_id = 'nih-nci-dceg-connect-stg-5519'
subprocess.run(['gcloud', 'config', 'set', 'project', project_id]) # set the default GCP project
# subprocess.run(['gcloud', 'auth', 'application-default', 'set-quota-project'])
subprocess.run(['gcloud', 'auth', 'application-default', 'login'])
credentials, project = google.auth.default()
client = bigquery.Client(project=project, credentials=credentials)

sql = \
"""
-- Demo query for F&R meeting May 16, 2023. 

-- Context: Say we want to investigate a GitHub Issue saying that two individuals
--          (Connect_ID: '4429973054', '3521720963') have a recruit status of 
--          'Not Active' and have a verification status of 'Verified.'

SELECT
  Connect_ID,
  token,
  d_512820379 AS recruitment_type,  -- 180583933 = Not Active
  d_821247024 AS verification_satus -- 197316935 = Verified
FROM
  `nih-nci-dceg-connect-stg-5519.RecruitmentBySite.HealthPartners`
WHERE
  Connect_ID IS NOT NULL 

-- Put the participants of interest first in the table
ORDER BY
  (CASE WHEN Connect_ID IN ('4429973054', '3521720963') THEN 1
        ELSE 2
  END)
"""

# Start the query, passing in the extra configuration.
df = client.query(sql).to_dataframe()
print(df.head())

