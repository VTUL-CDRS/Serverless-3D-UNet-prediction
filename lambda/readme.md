## Docker

* Build the docker
```
docker build -t docker_name .
```

* Push the docker image to ECR
```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS account>.dkr.ecr.us-east-1.amazonaws.com

aws ecr create-repository --repository-name repository_name --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

docker tag docker_name:latest <AWS account>.dkr.ecr.us-east-1.amazonaws.com/docker_name:latest

docker push <AWS account>.dkr.ecr.us-east-1.amazonaws.com/docker_name:latest        

```

## AWS SAM CLI

* build the sam template
```
sam build
``` 

* deploy the sam template
```
sam deploy --guided
``` 

stack_name = "stack_name"
ENDPOINT = "Sagemaker endpoint"
S3BucketName = "S3_bucket_name"

* invoke the lambda function
``` 
sam local invoke --event event.json
```
