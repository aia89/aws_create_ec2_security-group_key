import boto3
import os

ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')


class Create_SG:
    def __init__(self, sg_type, sgname):
        self.sg_type = sg_type
        self.sgname = sgname


    def ec2_create_sg(self):

        try:
            if self.sg_type == 'ssh':
                response = ec2_client.create_security_group(GroupName=self.sgname, Description='SG for ssh')
                ec2_client.authorize_security_group_ingress(
                    GroupId=response['GroupId'],
                    IpPermissions=[
                        {'IpProtocol': 'tcp',
                         'FromPort': 22,
                         'ToPort': 22,
                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                    ]
                )
                print("Security GroupID {} was crated".format(response['GroupdId']))
                return 1
            elif self.sg_type == 'web':
                response = ec2_client.create_security_group(GroupName=self.sgname, Description='SG for web')
                ec2_client.authorize_security_group_ingress(
                    GroupId=response['GroupId'],
                    IpPermissions=[
                        {'IpProtocol': 'tcp',
                         'FromPort': 443,
                         'ToPort': 443,
                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                        {'IpProtocol': 'tcp',
                         'FromPort': 80,
                         'ToPort': 80,
                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                        {'IpProtocol': 'tcp',
                         'FromPort': 22,
                         'ToPort': 22,
                         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                    ]
                )
                print("Security GroupID {} was crated".format(response['GroupdId']))
                return 1
            else:
                print("Security Group creation process had failed, unknown type!")
                return 0
        except:
            print("Security Group creation process had failed, very likely due to duplicate SG Naming!")
            return 0

class Create_Key:
    def __init__(self, key_name):
        self.key_name = key_name


    def ec2_create_key(self):
        my_path = os.path.expanduser("~/" + self.key_name + "_ssh.pem")

        try:
            if os.path.exists(my_path) and os.path.getsize(my_path) > 0:
                print("Warning!!! Key wasn't created because " + my_path + " already exists")
                return 0
            else:
                keypair = ec2_client.create_key_pair(KeyName=self.key_name)

                print("Key is being exported to "  + my_path)
                with open(my_path, "w+") as line:
                    print(keypair['KeyMaterial'], file=line)
                    print(keypair['KeyMaterial'])
                line .close()
                return 1
        except:
            return 0


class Create_EC2(Create_SG, Create_Key):

    def __init__(self, sg_type, sg_name, key_name):
        self.sg_name = sg_name
        self.key_name = key_name

        Create_SG.__init__(self, sg_type, sg_name)
        Create_Key.__init__(self, key_name)


    def create_ec2_instance(self):
        instance = ec2_resource.create_instances(ImageId='ami-bf4193c7', MinCount=1, MaxCount=1, SecurityGroups=[self.sg_name], KeyName=self.key_name, InstanceType='t2.micro')
        print(instance)


web1 = Create_EC2("web", "web1_sg", "web1_key")
web1.ec2_create_sg()
web1.ec2_create_key()
web1.create_ec2_instance()
