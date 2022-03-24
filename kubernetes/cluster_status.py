from kubernetes import client, config
from kubernetes.client.rest import ApiException
from concurrent.futures import ThreadPoolExecutor, as_completed
from texttable import Texttable
import argparse
import time
import socket
import ssl
from datetime import datetime

def _nanocore_to_millicore(n):
    n=int(n[:-1])
    return str(round(n/1000000,2))+'m'

def _core_to_millicore(n):
    n=int(n)
    return str(n*1000)+'m'

def _percent_cpu(tcpu,ccpu):
    tcpu=float(tcpu[:-1])
    ccpu=float(ccpu[:-1])
    return str(round((ccpu/tcpu)*100, 2))+'%'

def _to_gibibyte_or_mebibyte(n):
    if n[-2:] == 'Ki':
        n=float(n[:-2])
        if str(round(n*0.000000953674316,2)).split('.')[0]=='0':
            return str(round(n*0.0009765625,2))+'Mi'
        return str(round(n*0.000000953674316,2))+'Gi'
    elif n[-2:] == 'Mi' or n[-2:] == 'Gi':
        return n

def _return_expiry_date(url, port=443):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=url,)
    conn.settimeout(3.0)
    try:
        conn.connect((url, port))
        ssl_info = conn.getpeercert()
        res = datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        return res
    except:
        return 'Expired'


def load_node_list():
    nodes=[]
    config.load_kube_config()
    stats_api = client.CustomObjectsApi()
    node_stats = stats_api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
    for stat in node_stats['items']:
        nodes.append(stat['metadata']['name'])
    return nodes

def node_stats(node):
    k8s_api = client.CoreV1Api()
    api_response = k8s_api.read_node_status(node)
    stats_api = client.CustomObjectsApi()
    node_stats = stats_api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes/{}".format(node))
    field_selector = 'spec.nodeName='+node
    pods = k8s_api.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    node_dict={}
    node_dict[node]=[api_response.metadata.name, api_response.status.node_info.kubelet_version, api_response.metadata.labels['node.kubernetes.io/instance-type'], api_response.metadata.labels['failure-domain.beta.kubernetes.io/region'],api_response.metadata.labels['failure-domain.beta.kubernetes.io/zone'],api_response.spec.provider_id.split('/')[-1], _core_to_millicore(api_response.status.capacity['cpu']), _nanocore_to_millicore(node_stats['usage']['cpu']), _percent_cpu(_core_to_millicore(api_response.status.capacity['cpu']),_nanocore_to_millicore(node_stats['usage']['cpu'])), _to_gibibyte_or_mebibyte(api_response.status.capacity['memory']), _to_gibibyte_or_mebibyte(node_stats['usage']['memory']), _to_gibibyte_or_mebibyte(api_response.status.capacity['ephemeral-storage']), api_response.status.capacity['pods'],len(pods.items)]
    return node_dict

def pod_stats(node):
    k8s_api = client.CoreV1Api()
    stats_api = client.CustomObjectsApi()
    field_selector = 'spec.nodeName='+node
    pods = k8s_api.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    pod_dict={}
    for pod in pods.items:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        phase = pod.status.phase
        pod_ip= pod.status.pod_ip
        if not pod.metadata.owner_references:
            pod_kind=None
        else:
            pod_kind=pod.metadata.owner_references[0].kind
        worker_node=pod.spec.node_name
        try:
            cpu=0
            mem=0
            cpu_mem=stats_api.get_namespaced_custom_object("metrics.k8s.io", "v1beta1", namespace, "pods", pod_name)
            for c in cpu_mem['containers']:
                if c['usage']['cpu'] == '0':
                    pass
                else:
                    cpu=+int(c['usage']['cpu'][:-1])
            cpu=str(cpu)+'n'
            cpu=_nanocore_to_millicore(cpu)
            for m in cpu_mem['containers']:
                mem=+int(m['usage']['memory'][:-2])
            mem=str(mem)+'Ki'
            mem=_to_gibibyte_or_mebibyte(mem)
        except ApiException as x:
            if x.status == 404:
                cpu='Not Found'
                mem='Not Found'
        container_name=[]
        if not pod.status.container_statuses:
            container_name=None
            container_image=None
        else:
            for container in range(len(pod.status.container_statuses)):
                container_name.append('{}:{}'.format(pod.status.container_statuses[container].name, pod.status.container_statuses[container].restart_count))
            container_image=[]
            for container in range(len(pod.status.container_statuses)):
                container_image.append(pod.status.container_statuses[container].image)
        pod_dict[pod_name]=[pod_name,namespace,phase,pod_ip,pod_kind,worker_node,cpu,mem,container_name, container_image]
    return pod_dict

def ingress_stat():
    config.load_kube_config()
    v1 = client.ExtensionsV1beta1Api()
    ret = v1.list_ingress_for_all_namespaces()
    ingress_summary={}
    for ing in ret.items:
        ing_name=ing.metadata.name
        ing_ns=ing.metadata.namespace
        url=ing.spec.rules[0].host
        if url == None:
            continue
        expiry_date=_return_expiry_date(url)
        ingress_summary[ing_name]=[ing_name,ing_ns,url,expiry_date]
    table3 = Texttable(max_width=180)
    ingresses_table=[['Ingress Name', 'Ingress Namespace', 'Ingress URL', 'Ingress Expiry date']]
    for ingress in ingress_summary:
        ingresses_table.append(ingress_summary[ingress])
    table3.add_rows(ingresses_table)
    print(table3.draw())

def node_run():
    start=time.perf_counter()
    node_list=load_node_list()
    with ThreadPoolExecutor() as executor:
        futures = []
        for node in node_list:
            futures.append(executor.submit(node_stats, node))
        node_summary={}
        for future in as_completed(futures):
            a=future.result()
            node_summary.update(a)
    table1 = Texttable(max_width=180)
    node_table = [['Node Name', 'Kubelet Ver', 'Instance Type', 'Region', 'Zone', 'Provide ID', 'Total CPU', 'CPU Usage', 'Percent CPU','Total Memory', 'Memory Usage', 'Total Storage', 'Allocatable PODs', 'Current PODs']]
    for node in node_summary:
        node_table.append(node_summary[node])
    table1.add_rows(node_table)
    print(table1.draw())
    end=time.perf_counter()
    print("Finished collecting node stats in {} secs".format(round(end-start,2)))

def pod_run():
    start=time.perf_counter()
    node_list=load_node_list()
    with ThreadPoolExecutor() as executor:
        futures = []
        for node in node_list:
            futures.append(executor.submit(pod_stats, node))
        pod_summary={}
        for future in as_completed(futures):
            a=future.result()
            pod_summary.update(a)
    table2 = Texttable(max_width=180)
    pod_table=[['Pod Name', 'Namespace', 'Phase', 'POD IP', 'POD Kind', 'Worker Node', 'CPU Usage', 'Mem Usage', 'Container Name:Restart', 'Container Image']]
    for pod in pod_summary:
        pod_table.append(pod_summary[pod])
    table2.add_rows(pod_table)
    print(table2.draw())
    end=time.perf_counter()
    print("Finished collecting pod stats in {} secs".format(round(end-start,2)))

def ing_run():
    start=time.perf_counter()
    ingress_stat()
    end=time.perf_counter()
    print("Finished collecting ing stats in {} secs".format(round(end-start,2)))

  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kubernetes Status.', epilog="Please run the script to check kubernetes status.")
    parser.add_argument('-n', '--nodes', action=argparse.BooleanOptionalAction, type=bool, required=False, help="if true, get node status.")
    parser.add_argument('-p', '--pods', action=argparse.BooleanOptionalAction, type=bool, required=False, help="if true, get pods status.")
    parser.add_argument('-i', '--ingresses', action=argparse.BooleanOptionalAction, type=bool, required=False, help="if true, get ingresses status.")
    params = parser.parse_args()
    nodes=params.nodes
    pods=params.pods
    ingresses=params.ingresses
    if nodes:
        node_run()
    elif pods:
        pod_run()
    elif ingresses:
        ing_run()
    elif not nodes and not pods and not ingresses:
        node_run()
        pod_run()
        ing_run()
