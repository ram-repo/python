import os
import json
import requests
from kubernetes import client, config
from kubernetes.stream import portforward
from threading import Thread
import time

def port_forward(namespace, pod_name, local_port, target_port, kube_config_path):
    """
    Port forward from a local port to a target port on a Kubernetes pod.
    
    Parameters:
        namespace (str): Namespace of the pod.
        pod_name (str): Name of the pod.
        local_port (int): Local port to forward to.
        target_port (int): Target port on the pod.
        kube_config_path (str): Path to the Kubernetes configuration file.
        
    Returns:
        None
    """
    # Load Kubernetes configuration from the specified path
    config.load_kube_config(config_file=kube_config_path)

    # Get the API client
    api_client = client.ApiClient()

    # Create a PortForward object
    pf = portforward(api_client, namespace, pod_name, ports={local_port: target_port})

    print(f"Port forwarding: localhost:{local_port} -> {pod_name}:{target_port}")
    try:
        # Keep the port forward running
        pf.run_forever()
    except KeyboardInterrupt:
        print("Port forwarding stopped.")

def hit_api_and_save_to_file(local_host, local_port, endpoint, output_file):
    """
    Hit the API endpoint on the forwarded port and save the JSON response to a file.
    
    Parameters:
        local_host (str): The local host (localhost).
        local_port (int): The local port to which the API is forwarded.
        endpoint (str): The API endpoint to hit.
        output_file (str): The path to the output file where the response will be saved.
        
    Returns:
        None
    """
    url = f"http://{local_host}:{local_port}{endpoint}"
    
    try:
        # Send GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4xx/5xx responses
        
        # Save the JSON response to the file
        with open(output_file, 'w') as file:
            json.dump(response.json(), file, indent=4)
        
        print(f"API response saved to {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")

if __name__ == "__main__":
    # Kubernetes port-forward settings
    namespace = "default"  # Your Kubernetes namespace
    pod_name = input("Enter the pod name: ")  # Your pod name in Kubernetes
    local_port = 9200  # Local port to forward to
    target_port = 9200  # Target port on the pod (usually the same as local)

    # API endpoint settings
    local_host = "localhost"
    endpoint = "/api/some/endpoint"  # Modify with your API endpoint
    output_file = "output.json"  # The JSON file to save the response
    
    # Path to the custom kube config file (admin.config)
    kube_config_path = "admin.config"  # Change this to the actual path of your kube config file
    
    # Step 1: Start port forwarding in a separate thread
    port_forward_thread = Thread(target=port_forward, args=(namespace, pod_name, local_port, target_port, kube_config_path))
    port_forward_thread.daemon = True  # Daemonize the thread so it exits when the main program ends
    port_forward_thread.start()
    
    # Wait for port forwarding to establish
    print("Waiting for port forwarding to establish...")
    time.sleep(5)  # Sleep to allow time for the port-forwarding to be established
    
    # Step 2: Hit the API and store the JSON response
    hit_api_and_save_to_file(local_host, local_port, endpoint, output_file)