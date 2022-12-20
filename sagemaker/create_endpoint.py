import boto3
import sagemaker

from sagemaker.tensorflow import TensorFlowModel

instance_type = "ml.g4dn.xlarge"
role_name = "AmazonSageMaker-ExecutionRole-example"

iam = boto3.client('iam')
role = iam.get_role(RoleName=role_name)['Role']['Arn']

sm_session = sagemaker.Session()
bucket_name = sm_session.default_bucket()

sagemaker_model = TensorFlowModel(
    model_data=f"s3://{bucket_name}/model/model.tar.gz",
    role=role,
    framework_version="2.9",
)

predictor = sagemaker_model.deploy(
    initial_instance_count=1, instance_type=instance_type)
