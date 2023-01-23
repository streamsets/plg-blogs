import os
from streamsets.sdk import ControlHub

# These will need to be replaced with your credentials
config = {
    # control hub
    'credential-id': 'your-credential-id',
    'token': 'your-token',

    # aws S3
    'aws-access-key': 'your-access-key',
    'aws-secret-access-key': 'your-secret-access-key',

    # redshift
    'jdbc-connection-string': 'your-jdbc-connection-string',
    'redshift-username': 'your-username',
    'redshift-password': 'your-password'
}


"""CONNECT TO CONTROL HUB"""
sch = ControlHub(credential_id=config.get('credential-id'), token=config.get('token'))
print(sch.version)

"""CREATING YOUR ENVIRONMENT"""
environment_builder = sch.get_environment_builder(environment_type='SELF')
environment = environment_builder.build(environment_name='Self-Managed-Env-PythonSDK',
                                        environment_tags=['self-managed-tag'],
                                        allow_nightly_engine_builds=False)
sch.add_environment(environment)
sch.activate_environment(environment)

"""CONFIGURING YOUR DEPLOYMENT"""
deployment_builder = sch.get_deployment_builder(deployment_type='SELF')
deployment = deployment_builder.build(deployment_name='Self-Managed-Deployment-PythonSDK',
                                      environment=environment,
                                      engine_type='DC',
                                      engine_version='5.0.0',
                                      deployment_tags=['self-managed-tag'])
deployment.install_type = 'TARBALL'
# deployment.install_type = 'DOCKER'
sch.add_deployment(deployment)
# equivalent to clicking on 'Start & Generate Install Script'
sch.start_deployment(deployment)
# add sample stage libs
deployment.engine_configuration.stage_libs = ['dataformats', 'basic', 'dev', 'jdbc', 'aws']
# add JDBC redshift driver
deployment.engine_configuration.external_resource_source = 'externalResources.zip'
# update deployment with libraries
sch.update_deployment(deployment)

"""START YOUR ENGINE"""
# retrieves install script
install_script = sch.get_self_managed_deployment_install_script(deployment, install_mechanism="BACKGROUND")
# prints install script
print(install_script)
# deploys engine
os.system(install_script)
# identify data collector
sdc = next(eng for eng in sch.data_collectors if eng.deployment_id == deployment.deployment_id)

"""SET UP YOUR S3 CONNECTION"""
# configure your connection
connection_builder = sch.get_connection_builder()
connection = connection_builder.build(title='s3-connection',
                                      connection_type='STREAMSETS_AWS_S3',
                                      authoring_data_collector=sdc,
                                      tags=None)
connection.connection_definition.configuration['awsConfig.awsAccessKeyId'] = config.get('aws-access-key')
connection.connection_definition.configuration['awsConfig.awsSecretAccessKey'] = config.get('aws-secret-access-key')
sch.add_connection(connection)

"""SELECT AND CONFIGURE THE STAGES WITHIN YOUR PIPELINE"""
pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sdc.id)
origin = pipeline_builder.add_stage('Amazon S3', type='origin')
origin.use_connection(connection)
origin.set_attributes(bucket='pythonsdk', # this should be the name of your S3 bucket
                      prefix_pattern='*.csv', # this will be whatever your file type is
                      data_format='DELIMITED', 
                      header_line='WITH_HEADER', 
                      stage_on_record_error='TO_ERROR')

destination = pipeline_builder.add_stage('JDBC Producer')
destination.set_attributes(default_operation='INSERT', 
                           table_name='netflix-titles', # this should be the name of your destination table in redshift
                           schema_name='public', 
                           field_to_column_mapping=None, 
                           jdbc_connection_string=config.get('jdbc-connection-string'), 
                           username=config.get('redshift-username'), 
                           password=config.get('redshift-password'))

no_more_data_finisher = pipeline_builder.add_stage('Pipeline Finisher Executor')

"""BUILD/PUBLISH YOUR PIPEINE"""
origin >> destination
origin >= no_more_data_finisher
pipeline = pipeline_builder.build('SDK pipeline')
sch.publish_pipeline(pipeline, commit_message='First commit of my sdk pipeline')

"""CONFIGURE THE JOB AND RUN YOUR PIPELINE"""
job_builder = sch.get_job_builder()
pipeline = sch.pipelines.get(name='SDK pipeline')
job = job_builder.build('SDK job', pipeline=pipeline)
job.data_collector_labels = ['Self-Managed-Deployment-PythonSDK']
sch.add_job(job)
sch.start_job(job)
