import pykube
import yaml
from time import strftime,localtime
import sys
import datetime;
  
def send_event(ProblemSize):
    
    ct = localtime()
    doc = {
            "apiVersion": "v1",
            "count": 1,
            "firstTimestamp": strftime("%Y-%m-%dT%H:%M:%SZ", ct),
            "lastTimestamp": strftime("%Y-%m-%dT%H:%M:%SZ", ct),
            "involvedObject": {
                "kind": "Pod",
                "name": "sabrelabs", #TODO, add param maybe?
                "uid": "" #TODO, add param maybe?
            },
            "kind": "Event",
            "message":  str(datetime.datetime.now()) + ": Setting problem size to " + ProblemSize,
            "metadata": {
                "name": "Pod_podname_reportingProblemsize_" + str(datetime.datetime.now().timestamp()), #what to do with that?
                "namespace": "default",
                "time": strftime("%Y-%M-%dT%H:%M:%SZ", ct),
            },
            "reason": "Python API send_event(" + ProblemSize + ") called",
            "type": "Normal"
        }

    #print(str(doc))
    # Actually create an object by requesting the Kubernetes API.
    api = pykube.HTTPClient(pykube.KubeConfig.from_file("~/.kube/config"))
    
    pod = pykube.Event(api, doc)
    pod.create()
    api.session.close()
    
if __name__ == "__main__":
    send_event(sys.argv[1])
