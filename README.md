## Custom-k8s-health-dashboard
Containerized python application that can read kubeconfig and create a custom dashboard so you 
can hit refresh on page instead of logging in to node and running commands

## Requirements
When running it as a container make sure to run it on a node and provide mount path to kubeconfig.
If not make sure the mounted path to the deployment/pod contains kubeconfig.

The docker image is readily available at [docker image link](https://hub.docker.com/repository/docker/dhonnappa/k8shealth)
