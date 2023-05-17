from json import dumps
from argparse import ArgumentParser
from inquirer import prompt, List
from colorama import Fore
from http.client import HTTPConnection
from kubernetes.stream import portforward
from kubernetes.stream.ws_client import PortForward
from kubernetes import client, config

parser = ArgumentParser()

parser.add_argument("-s", "--service", required=True, help="The name of the service you wish to change log level.")
parser.add_argument("-n", "--namespace", required=True, help="The namespace the service is in.")
parser.add_argument("-l", "--logger", default="com.gocity", help="The logger that you wish to change the level of.")

args = parser.parse_args()

questions = [
    List(
        "level",
        message=f"What log level do you want to change the {args.logger} logger in {args.service} to?",
        choices=["DEBUG", "INFO", "WARN", "ERROR", "TRACE", "OFF"]
    ),
]

answers = prompt(questions)
level = answers["level"]


class ForwardedKubernetesHTTPConnection(HTTPConnection):
    def __init__(self, forwarding: PortForward, port: int):
        super().__init__("127.0.0.1", port)
        self.sock = forwarding.socket(port)

    def connect(self) -> None:
        pass

    def close(self) -> None:
        pass


config.load_kube_config()

v1 = client.CoreV1Api()

pods = v1.list_namespaced_pod(args.namespace)
pods = list(filter(lambda p: args.service in p.metadata.name, pods.items))

if len(pods) == 0:
    print(f"Cannot find pods for {Fore.GREEN}{args.service}{Fore.RESET} in namespace {Fore.RED}{args.namespace}{Fore.RESET} exiting...")
    exit()

headers = {
    "Content-Type": "application/json"
}

body = {
    "configuredLevel": level
}

for i in pods:
    print(
        f"Changing the log level for {Fore.GREEN}{i.metadata.name}{Fore.RESET} in {Fore.RED}{i.metadata.namespace}{Fore.RESET} to {Fore.CYAN}{level}{Fore.RESET}...")

    forward = portforward(
        v1.connect_post_namespaced_pod_portforward,
        i.metadata.name,
        i.metadata.namespace,
        ports="8081"
    )

    connection = ForwardedKubernetesHTTPConnection(forward, 8081)
    connection.request("POST", f"/actuator/loggers/{args.logger}", dumps(body), headers)

    response = connection.getresponse()
    print(f"Response status for {Fore.GREEN}{i.metadata.name}{Fore.RESET}: {Fore.CYAN}{response.status}{Fore.RESET}")
    connection.close()
