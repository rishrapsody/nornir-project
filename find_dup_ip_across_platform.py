from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb
import logging
from nornir.core.filter import F
from collections import Counter

nr = InitNornir(config_file="config.yml")
global_list = []
global_dev_list = []
global outer_dict
outer_dict = { }
global outer_dict2
outer_dict2 = { }
global dup_ip
global final_list
final_list = []

def get_dup_devices(task):
    if task.host.platform == 'ios' or task.host.platform == 'iosxr':
        cisco_list = get_cisco_devices(task)
#        print(cisco_list)
        global_dev_list.extend(cisco_list)
    elif task.host.platform == 'nxos':
        nxos_list = get_nxos_devices(task)
        global_dev_list.extend(nxos_list)
    else:
        junos_list = get_junos_devices(task)
        global_dev_list.extend(junos_list)

def get_cisco_devices(task):
    output = task.run(task=send_command, command="show ip int brief", severity_level=logging.DEBUG)
    task.host["facts_new"] = output.scrapli_response.genie_parse_output()
    inner_dict = { }
    inner_list = []
    for key, value in task.host["facts_new"]["interface"].items():
        if value["ip_address"] != "unassigned":
            inner_dict = { }

            if value["ip_address"] in dup_ip:
                inner_list = []
                for i in dup_ip:
                    if i == value["ip_address"]:
                        inner_dict[key] = task.host
                        final_list.append("{} is configured on interface {} on device {}".format(i,key,task.host))

                    else:
                        pass

            else:
                pass
        else:
            pass

def get_nxos_devices(task):
    output = task.run(task=send_command, command="show interface", severity_level=logging.DEBUG)
    task.host["facts_new"] = output.scrapli_response.genie_parse_output()
    inner_dict2 = {}
    inner_list2 = []
    for key, value in task.host["facts"].items():
        if "ipv4" in value:
            for i,j in value["ipv4"].items():
                if j["ip"] in dup_ip:
                    inner_dict2[task.host] = key
                    inner_list2.append(inner_dict2)
                    outer_dict2[j["ip"]] = inner_list2
                    final_list.append("{} is configured on interface {} on device {}".format(j["ip"], key, task.host))
                    inner_dict2 = {}
        else:
            pass




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
    print("Intf list for {} is {}".format(task.host, sub_list))
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
    print("Intf list for {} is {}".format(task.host,sub_list))
    return(sub_list)

def get_ip_iosxr(task):
    output = task.run(task=send_command, command="show ip int brief", severity_level=logging.DEBUG)
    task.host["facts"] = output.scrapli_response.genie_parse_output()
    sub_list = []
    for key,value in task.host["facts"]["interface"].items():
        if value["ip_address"] != "unassigned":
            sub_list.append(value["ip_address"])
        else:
            pass
    print("Intf list for {} is {}".format(task.host, sub_list))
    return(sub_list)

#devices = nr.filter(F(groups__contains='cloud'))
#results = devices.run(task=get_ip)
results = nr.run(task=get_ip)

dup_ip = [item for item, count in Counter(global_list).items() if count > 1]
if dup_ip:
    print("\n")
    print("Duplicate IP's found: {}".format(dup_ip))
    temp = nr.run(task=get_dup_devices)
#    print(outer_dict)
#    print(outer_dict2)
#    print(sorted(final_list))
    print("#" * 60)
    for line in sorted(final_list):
        print(line)
    print("#" * 60)

else:
    print("No Duplicate IPs found")