import time
from kubernetes import client, config, utils, stream

config.load_kube_config()
api_client = client.ApiClient()
v1 = client.CoreV1Api()

node_chrome_yaml_file = "./chrome_node/infrastructure/chrome-node-deployment.yaml"
test_case_yaml_file = "./test_controller/infrastructure/test-controller-deployment.yaml"

utils.create_from_yaml(api_client, node_chrome_yaml_file)


def waiting_for_pods(label_selector):
    while True:
        print("All chrome node pods are expected to stand up..")
        pods = v1.list_namespaced_pod(namespace="default", label_selector=label_selector)
        if pods.items:
            pod = pods.items[0]
            pod_phase = pod.status.phase
            if pod_phase == "Running":
                container_statuses = pod.status.container_statuses
                if all(container.ready for container in container_statuses):
                    return pod.metadata.name
        time.sleep(10)


def main():
    label_selector = "app=selenium"
    waiting_for_pods(label_selector)
    utils.create_from_yaml(api_client, test_case_yaml_file)
    label_selector = "app=test-case"
    test_case_pod_name = waiting_for_pods(label_selector)
    print("Test case running...")
    exec_command = ["python3", "-u", "./test-case.py"]
    response = stream.stream(
        v1.connect_get_namespaced_pod_exec,
        test_case_pod_name,
        namespace="default",
        command=exec_command,
        stderr=True,
        stdin=False,
        stdout=True,
        tty=False
    )
    print("çıktı:", response)


if __name__ == "__main__":
    main()
