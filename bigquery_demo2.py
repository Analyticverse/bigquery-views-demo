# Author:        Jake Peters
# Date Created:  May 2023
# Date Modified: May 2023
# Description:   
#                This script demonstrates a method of downloading data from 
#                a BigQuery View or Table using pandas_gbq. This demo was 
#                was prepared for the Connect Coordinating Center's 
#                Feedback and Review (F&R) meeting in May 2023.
# Reference:     Example modified from:
#                https://googleapis.dev/python/pandas-gbq/latest/intro.html#authenticating-to-bigquery  

import subprocess
import pandas_gbq

# Authenticate to BigQuery using gcloud CLI
project_id = "nih-nci-dceg-connect-stg-5519"
subprocess.run(['gcloud', 'config', 'set', 'project', project_id]) # set the default GCP project
# subprocess.run(['gcloud', 'auth', 'application-default', 'set-quota-project']) # Uncomment only if needed
subprocess.run(['gcloud', 'auth', 'application-default', 'login'])

# Make query to BigQuery table/view
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
df = pandas_gbq.read_gbq(sql, project_id=project_id)
print(df.head())
# RESULTS ARE JUST TEST DATA FROM STG:
#    Connect_ID                                 token recruitment_type verification_satus
# 0  3003674947  6f576bc0-1bab-4ba4-bdaf-58dd9d133209        854703046          854703046
# 1  7582627128  06834c06-90c1-4cfe-8849-d90b1e58e176        854703046          854703046
# 2  5039196924  3d2da884-4815-488f-8041-ad52c4b9e3ee        854703046          854703046
# 3  5753928363  e2cd2964-2886-41cd-820e-0c61b992c49f        854703046          854703046
# 4  4600083085  8a818f61-6e60-4a80-80bf-ca9616263470        854703046          854703046
