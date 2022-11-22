# __music_clustering_recommendation__
Recommend musics using clustering (the project in database class)

---

## __Scraping Data__
<br>

### __1) Create an application in Spotify for Developers__
<br>

* Spotify App Dashboard: https://developer.spotify.com/dashboard/login

* App setting guide: https://developer.spotify.com/documentation/general/guides/authorization/app-settings/

<br>

### __2) Download extracted.mpd.slice data and script__
<br>

* ./extracted_data/extracted.mpd.slice.*.json

* ./spotify_api.py

* ./spotify_config.py

* ./spotify_scraper.py

<br>

### __3) Set up your config.ini__
<br>

* run script below to initialize config file

```bash
python spotify_config.py
```

* set up client_id and client_secret in authentication section of config.ini

```ini
[authentication]
client_id = 3a...1c
client_secret = tv...0x
```

<br>

### __4) Run spotify_scraper.py__
<br>

* refer to help option in spotify_scraper.py

```bash
python spotify_scraper.py --type=artists --all=False
```

<br>

---

## __AWS Lake Formation__
<br>

sources: https://docs.aws.amazon.com/lake-formation/latest/dg/getting-started-setup.html

<br>

### __1) Complete initial AWS configuration tasks__
<br>

&ensp;&ensp; - Create an Administrator IAM User
<br>
&ensp;&ensp; - Sign in as an IAM User

<br>

### __2) Create an IAM role for workflows__
<br>

&ensp;&ensp; - A workflow defines the data source and schedule to import data into your data lake
<br>
&ensp;&ensp; - A workflow can be created by AWS Glue crawlers
<br>
&ensp;&ensp; 1) Sign in as an Administrator
<br>
&ensp;&ensp; 2) Choose roles and create roles
<br>
&ensp;&ensp; 3) Choose AWS service and Glue
<br>
&ensp;&ensp; 4) Add permissions within AWSGlueServiceRole and name the role LakeFormationWorkflowRole
<br>
&ensp;&ensp; 5) On Roles page, choose the LakeFormationWorkflowRole
<br>
&ensp;&ensp; 6) On Summary page, under the Permission tab, choose Add inline policy, add the policy below
<br>

```json
# Replace <account-id> with a valid AWS account number

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                 "lakeformation:GetDataAccess",
                 "lakeformation:GrantPermissions"
             ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": ["iam:PassRole"],
            "Resource": [
                "arn:aws:iam::<account-id>:role/LakeFormationWorkflowRole"
            ]
        }
    ]
}
```
&ensp;&ensp; 7) Verify that LakeFormationWorkflowRole has two policies attached
<br>
&ensp;&ensp; 8) If you import data from outside, add an inline policy granting permissions to read the source data

<br>

### __3) Create a data lake administrator__
<br>

&ensp;&ensp; 1) Choose one user who is to be a data lake administrator
<br>
&ensp;&ensp; 2) Add a inline policy, which grants the data lake administrator permission to create the Lake Formation service-linked role
<br>

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": "lakeformation.amazonaws.com"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:PutRolePolicy"
            ],
            "Resource": "arn:aws:iam::<account-id>:role/aws-service-role/lakeformation.amazonaws.com/AWSServiceRoleForLakeFormationDataAccess"
        }
    ]
}
```

&ensp;&ensp; 3) Add a PassRole inline policy to create and run workflows
<br>

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PassRolePermissions",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::<account-id>:role/LakeFormationWorkflowRole"
            ]
        }
    ]
}
```

&ensp;&ensp; 4) Add a RAMAcess inline policy to grant or receive cross-account Lake Formation permissions
<br>

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ram:AcceptResourceShareInvitation",
                "ram:RejectResourceShareInvitation",
                "ec2:DescribeAvailabilityZones",
                "ram:EnableSharingWithAwsOrganization"
            ],
            "Resource": "*"
        }
    ]
}
```

&ensp;&ensp; 5) Open the AWS Lake Formation console and sign in as the IAM administrator user
<br>
&ensp;&ensp; 6) If a Welcome to Lake Formation window appears, choose get started

<br>

### __4) Change the default permission model__
<br>

<br>

### __5) Create additional Lake Formation users__
<br>

<br>

### __6) Configure an Amazon S3 location for your data lake__
<br>

<br>

### __7) Prepare for using governed tables__
<br>

<br>

---

## __AWS RDS__
<br>

sources: https://www.youtube.com/watch?v=bC-G4OcLr5g

<br>

### __1) Create an RDS instance with MySQL__
<br>

### __2) Make the database public__
<br>

### __3) Install MySQL Work bench and establish a connection__
<br>

### __4) Import Data to table__
<br>

---