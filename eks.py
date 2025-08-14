from kubernetes import client, config

# Load the kubeconfig file (for local use; use load_incluster_config() for in-cluster)
config.load_kube_config()

# Create the API client
api_client = client.ApiClient()

# Create the Deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "my-flask-app"}),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="568373317874.dkr.ecr.us-east-1.amazonaws.com/my_monitoring_app_image:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
apps_v1 = client.AppsV1Api(api_client)
apps_v1.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Create the Service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(
            protocol="TCP",
            port=5000,
            target_port=5000
        )],
        type="NodePort"  # Optional: "ClusterIP" is default, use "NodePort" to expose outside cluster
    )
)

# Create the service
core_v1 = client.CoreV1Api(api_client)
core_v1.create_namespaced_service(
    namespace="default",
    body=service
)
