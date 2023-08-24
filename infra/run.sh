aws eks --region us-west-1 update-kubeconfig --name gila-cluster
kubectl apply -f message-app-deployment.yaml
kubectl apply -f notification-service-deployment.yaml
kubectl apply -f message-app-service.yaml
kubectl apply -f notification-service-service.yaml
