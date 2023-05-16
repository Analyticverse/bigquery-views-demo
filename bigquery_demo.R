# Author:        Jake Peters
# Date Created:  May 2023
# Date Modified: May 2023
# Description:   
#                This script demonstrates a method of downloading data from 
#                a BigQuery View or Table using bigrquery. This demo was 
#                was prepared for the Connect Coordinating Center's 
#                Feedback and Review (F&R) meeting in May 2023.
# References:         
#   bigrquery reference: https://bigrquery.r-dbi.org/
#   bigrquery man pages: https://rdrr.io/cran/bigrquery/man/

library(bigrquery) # R package that works with BigQuery API

# Authenticate to BigQuery
project <- 'nih-nci-dceg-connect-stg-5519'
billing <- project    # Billing must be same as project
bigrquery::bq_auth()  # Will take you to a pop-up in your browser to sign-in

# Write out SQL query 
sql <-
"-- Demo query for F&R meeting May 16, 2023. 

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
  END)"

# Download data from BQ
bq_query     <- bq_project_query(project, sql)
bq_data      <- bigrquery::bq_table_download(bq_query, bigint = "integer64")
head(bq_data)

