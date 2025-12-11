Process of Pipeline  ->  EC2 producer → Kinesis → Databricks (Bronze → Silver → Gold, Delta tables) -> S3 storage



1: aws kinesis  -> created the data stream inside that these configuration were done - what is on demand and provisioned shards and why we need them what is shard estimator and what is MiB/seconds.



2: EC2 instance with the configuration as -> aws service (trusted entity type) and ec2 (service or use case) , attach permission (amazon kinesis full access) haven't restricted it yet -> create role and name the role (KinesisProducerRole) , selecting ubuntu and default t3micro with that. we went default security groups RAJ



3: accessing the (ec2 mkdir keys)

cd keys using wsl after that shifting the pem file in that file location -> cp /mnt/d/Revature-Training/weather-streamkey.pem .



That final dot . means “put the file in the current folder”.



-> after that set permission -> chmod 400 weather-streamkey.pem



\*Now connect ec2  : ssh -i weather-streamkey.pem ubuntu@<YOUR\_EC2\_PUBLIC\_IP>

then it asks -> Are you sure you want to continue connecting (yes/no/\[fingerprint]) yes

imp for accesing the instance (ssh -i weather-streamkey.pem ubuntu@98.92.159.87)



\*error when u dont send ping to the instance we encounter this error( ubuntu@ip-172-31-70-226:~$ client\_loop: send disconnect: Broken pipe codebind@Ratz:~/keys$ does this happen when ur not working on anything with that instance so it disconnects?)



so now we have to fix this by nano ~/.ssh/config  , Host \*

    ServerAliveInterval 60

    ServerAliveCountMax 3



This sends a small ping every 60 seconds so AWS doesn’t disconnect you.



\* Now Run ALL PHASE 2 commands inside this EC2 terminal:

STEP 1 — Update EC2

sudo apt update

sudo apt install -y python3-pip



step 2 :Fix: Install boto3 via apt



Run these commands inside EC2 (you’re already there):



sudo apt update

sudo apt install -y python3-pip python3-boto3





Proper login in ssh ->

start instance then check for the ipv4 address as it changes whenever u terminate and start the instance and add the ssh -i weather and the address after that type yes after that add I have added a ping script code to ping the instance or else it get closed if it doesn't get pinged after that cd weather-producer -> then nano producer\_kinesis.py file -> after that run the script using

-> python3 producer\_kinesis.py



step 3: Create folder



mkdir weather-producer





cd weather-producer





 STEP 4 — Create producer script

nano producer\_kinesis.py



after creating ur in instance in that instance ur now inside the producer script im righting the py script which contains the random generation of data and following :- DE

<<

import boto3, json, random, time

from datetime import datetime, timezone



\# Create a Kinesis client

kinesis = boto3.client("kinesis", region\_name="us-east-1")



def make\_event():

    return {

        "station\_id": "ST\_" + str(random.randint(1, 5)),

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "temperature\_c": round(random.uniform(-5, 40), 1),

        "humidity\_pct": round(random.uniform(10, 100), 1),

        "wind\_speed\_kph": round(random.uniform(0, 120), 1),

        "status": "OK" if random.random() > 0.02 else "SENSOR\_ERR"

    }



while True:

    event = make\_event()

    kinesis.put\_record(

        StreamName="weather-stream",

        Data=json.dumps(event),

        PartitionKey=event\["station\_id"]

    )

    print("sent:", event)

    time.sleep(1)

>>





Step 6: Now Run the Producer ->



python3 producer\_kinesis.py



after this I am seeing my data -> 00:00', 'temperature\_c': -3.9, 'humidity\_pct': 16.6, 'wind\_speed\_kph': 107.6, 'status': 'OK'}

sent: {'station\_id': 'ST\_4



<also when the script is running and the ur able to look at the output we need to stop it just by pressing ctrl c to interrupt it>



\*now we will stop the instance  when we need to run this again we need  to

1:cd ~/keys

2: then the ssh command

ssh into EC2 → run the script again





now phase 3 with databricks



we go with databricks cloud provider option to launch with the 40$ credits and if we go with express installation one it will not

work as it creates serverless sql based workspace and it cant create cluster and its use less basically



so now we go with 14 day free trial and have the aws cloud attachment and admin access



\*\*for this we need go with cloud provider and go with aws it will direct you to aws market place setup payment method of 15k after that

we need to subscribe and create the agreement and create the account and opt for the 14 days trial with databricks and 400$ credit



but this was not able to complete due to errors so we need to go with mircosoft acc through which we are able to proceed and create t

 40$ account



create the cluster and remove normal off and photon off and md5 large or md4 large and need to add polcies and key value and create it will take 30 to 40 mins



also set the status of cluster from 120 to 10minutes activity of the cluster. EP







Phase 3 starts setting up the notebook inside the workspace



where you add the bronze layer inside which u add the py lib and boto 3 with that code of ur requirements and with that you face error after step 5



policy changes in databricks-computre-role in aws also



\*\* to add the the instance role its in main ui of db where it is present in databricks.



no add the instance from databricks-weather-role two things are are arn instance and arn add both and if stil cause error skip validation





\*\* now go to Compute → Your Cluster → Edit → Advanced options → Instance Profile

select the databricks instance and restart the cluster







Microsoft account used rajdeep19



#####  AFTER ALL OF THIS ENCOUNTERED ERROR OF INSTANCE ARN PROFILE IN DB AS ITS NOT LETTING ME ADD THE INSTANCE PERMISSION OUT SIDE OF ACCOUNT

##### AND EVEN THE BOUNDARY ROLE OF Databricks-Compute role its getting an error and its not working tried for almost 10 plus hrs and its not working going for another approach now ..........



as UC is not available for me to access





###### New process pipeline ->



EC2 Producer → Kinesis Data Stream → Firehose → S3 → Databricks (Bronze → Silver → Gold, Delta Tables) -> S3





as we already have ec2 and kinesis data streama nd databricks compute already in place we will go with S3 bucket creation first ->



\*\*\*created s3 bucket with the name ---->(weather-stream-raw-ap-south-1)



we will go to amazon data firehose --->>>



\*\*firehose streams in that we will setup the incoming data from amazon kinesis as the stream source and it will get stored in S3 of weather-ap-south-1



firehose stream name is -> weather-firehose



transform and convert records should not be selected as we are already doing the transformation in databricks



S3 bucket  input prefix - optional-->>> kinesis/weather/



s3 bucket output prefix - kinesis/error/  (while typing this if ur cursor is in new line it gives u error of cannot contain hiddennew line)





buffer size = 1



and buffer interval = 60sec



Gan Gan Gannat Boteh



New firehose stream is created and is ACTIVE NOW!



#### NOW TO READ THE DATA

1: FIRE UP THE INSTANCE THEN LOGIN USING THE TERMINAL OF UR REMOTE SYSTEM



2: THEN UR LIVE DATA IS BEING FETECHED FROM THE EC2 -> KINESIS -> FIRE HOSE -> S3 And its getting stored there in year month and date with cron if required at last GZ file format





 now I have stopped the ec2 and now we will proceed with the databricks connection to s3 path





user access key AKIAWAIXHM4F4JXWMFVC

secrect acess key -TiFjgkH6etd5AF9gPwvC5NH0OgVKfRapPGUcaeqX





ran this in databricks and after the user creation and back and forth for 12 hours it ran finally!!



now DATABRICKS is talking with S3 HARDEST PART!!!!!!!!!!



connections works user can now read write and have full acess with that I am able to see and store and create spark job at 4:46pm 7/12/25



data now after fetching it from s3 in real time it stores in hivemetastore instead of dbfs which requires unity catalog

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*RANNNNN\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

You’ve officially completed the entire Kinesis → Firehose → S3 → Databricks Bronze flow. at 4:58 PM 7/12/25



Returned rows. This means:



The path s3a://weather-stream-raw-ap-south-1/bronze/weather\_readings/ contains valid Delta files.



Databricks successfully registered that path inside hive\_metastore.weather\_db.



Your cluster has the correct AWS credentials active (the access key you injected).



Delta transaction log (\_delta\_log) exists and is readable.




visualization and spark job automation done !

Line Chart Example



Keys (X-axis): event\_date



Values (Y-axis): avg\_temp\_c



Series Grouping: station\_id



Bar Chart Example



X: station\_id



Y: max\_wind\_speed\_kph



Pie Chart Example



Label: station\_id



Value: row\_count







BRONZE\_PATH = "s3a://weather-stream-raw-ap-south-1/bronze/weather\_readings/"

SILVER\_PATH = "s3a://weather-stream-raw-ap-south-1/silver/weather\_readings/"

GOLD\_PATH   = "s3a://weather-stream-raw-ap-south-1/gold/weather\_hourly\_metrics/"

RAW\_PATH    = "s3a://weather-stream-raw-ap-south-1/kinesis/weather/"



