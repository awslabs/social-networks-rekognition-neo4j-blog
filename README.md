# Social Networks with AWS Rekognition and Neo4j Graph Database
This is a Jupyter notebook that highlights the use of AWS Rekognition's facial identification functionality.  It will identify celebrity faces (http://docs.aws.amazon.com/rekognition/latest/dg/celebrity-recognition.html) and use the Movie Graph Database (https://neo4j.com/developer/movie-database/#_download) hosted in a Neo4j database instance to render a graphical representation of the relationship between two celebrities (ala Six Degrees of Kevin Bacon).

## Dependencies
 - aws-cli


## Setup
Cloudformation templates are located under <project>/cft.  Run the following:
```
aws cloudformation create-stack –-stack-name rekognitionblog \
  --template-body file://rek-neo4j-blogpost-git.template \
  --parameters ParameterKey=KeyName,ParameterValue=<YOURKEYHERE> \
  --capabilities CAPABILITY_NAMED_IAM
```

Get the Public IP and Public DNS from the resulting stack completion:
```
aws cloudformation describe-stacks –-stack-name rekognitionblog
. . .
. . .
“Outputs”: [
    {
        “OutputKey”:”IPPublicInstance”,
        “OutputValue”:”XX.XX.XX.XX
},
    {
        “OutputKey”:”DNSPublicInstance”,
        “OutputValue”:”ec2-XX-XX-XX-XX.compute-1.amazonaws.com”
}

. . . 

```

Browse to the instance on port 7474 to set the Neo4j database password (one time event).
```
   https://<DNSPublicInstance>:7474
```

The intitial username / password combination is neo4j / neo4j  
You set the password to whatever you'd like...but remember what it is.

## Access the Notebook
SSH onto the instance and start the Jupyter server.  Make note of the DNS and token.....
```
> cd /opt/notebook
> jupyter notebook –no-browser
. . . 
. . .
Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8888/?token=0b640d92e8114965441a8cac2af61864dbf99086afcd6762
 

```


The EC2 instance is not set up to expose the Jupyter notebook, so open another ssh terminal and tunnel to the instance:
```
sudo ssh –I <your-pubic-key> -N -L 8888:localhost:8888 ubuntu@<publicDNS>
```


Now you can browse to the notebook and begin to enjoy.


