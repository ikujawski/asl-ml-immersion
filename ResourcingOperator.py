import kopf
import sys
import pykube
import yaml
from time import strftime,localtime
import sys
import datetime;

podName = "testpod"
def cpumem(argument):
    switcher = {
    "small": ("200m","500Mi", 1),
    "medium": ("300m","1Gi", 2),
    "big": ("400m","1500Mi", 3)
    }
    return switcher.get(argument, ("200m","500Mi", 1))


def create_deployment(sizing, api):
    (cpu, mem, replicas) = cpumem(sizing)
    obj = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": podName,
            "namespace": "default",
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": "sabrelabs"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "sabrelabs"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "resource-consuming-container",
                            "image": "busybox",
                            "command": [
                                "sleep",
                                "3600",
                            ],
                            "resources": {
                                "requests": {
                                    "memory": mem,
                                    "cpu": cpu
                                },
                            }
                        }
                    ]
                }
            }
        }
    }
    pykube.Deployment(api, obj).create()

def recreate_deployment(sizing): 
    api = pykube.HTTPClient(pykube.KubeConfig.from_file("~/.kube/config"))
    
    deps = pykube.Deployment.objects(api)
   
      
    for d in pykube.Deployment.objects(api):
        if d.name == podName:
            print("Deleting previous deployment...")
            d.delete()
    
    create_deployment(sizing, api)
    api.session.close()
    
    
@kopf.on.create('Event')
def create_fn(body, **kwargs):
    if body["kind"] == "Event" and  "reportingProblemsize" in body["metadata"]["name"]:
        print("Received following event:")
        print(body)
    
    if "small" in body["reason"]:
        print("event seem to request small deployment")
        recreate_deployment("small")
    if "medium" in body["reason"]:
        print("event seem to request medium deployment")
        recreate_deployment("medium")
    if "big" in body["reason"]:
        print("event seem to request big deployment")
        recreate_deployment("big")
    
if __name__ == "__main__":
    recreate_deployment(sys.argv[1])