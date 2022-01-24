from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb
import logging
from nornir.core.filter import F
from collections import Counter

nr = InitNornir(config_file="config.yml")
global_list = []

def get_ip(task):
    if task.host.platform == 'ios':
        ios_list = get_ip_ios(task)
        global_list.extend(ios_list)
    elif task.host.platform == 'iosxr':
        iosxr_list = get_ip_iosxr(task)
        global_list.extend(iosxr_list)
    elif task.host.platform == 'nxos':
        nxos_list = get_ip_nxos(task)
        global_list.extend(nxos_list)
    else:
        find_ip_junos(task)




def get_ip_ios(task):
    output = task.run(task=send_command, command="show ip int brief", severity_level=logging.DEBUG)
    task.host["facts"] = output.scrapli_response.genie_parse_output()
    sub_list = []
    for key,value in task.host["facts"]["interface"].items():
        if value["ip_address"] != "unassigned":
            sub_list.append(value["ip_address"])
    print("sub list for {} is {}".format(task.host, sub_list))
    return(sub_list)

def get_ip_nxos(task):
    output = task.run(task=send_command, command="show interface", severity_level=logging.DEBUG)
    task.host["facts"] = output.scrapli_response.genie_parse_output()
    sub_list = []
    for key, value in task.host["facts"].items():
        if "ipv4" in value:
            for i,j in value["ipv4"].items():
                sub_list.append(j["ip"])
        else:
            pass
    print("sub list for {} is {}".format(task.host,sub_list))
    return(sub_list)

def get_ip_iosxr(task):
    output = task.run(task=send_command, command="show ip int brief", severity_level=logging.DEBUG)
    task.host["facts"] = output.scrapli_response.genie_parse_output()
    sub_list = []
    for key,value in task.host["facts"]["interface"].items():
        if value["ip_address"] != "unassigned":
            sub_list.append(value["ip_address"])
    print("sub list for {} is {}".format(task.host, sub_list))
    return(sub_list)

devices = nr.filter(F(groups__contains='cloud'))
results = devices.run(task=get_ip)
#results = nr.run(task=get_net)

dup_ip = [item for item, count in Counter(global_list).items() if count > 1]
if dup_ip:
    print("Duplicate IP's found: {}".format(dup_ip))
else:
    print("No Duplicate IPs found")