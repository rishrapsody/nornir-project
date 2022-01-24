from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
import ipdb
from pprint import pprint
import logging
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir.core.filter import F
from ipaddress import IPv4Address
from collections import Counter

nr = InitNornir(config_file="config.yml")
global_list = []

def get_net(task):
    if task.host.platform == 'ios':
        ios_list = get_net_ios(task)
        global_list.extend(ios_list)
#        print("Global list is {}".format(global_list))
        count = Counter(global_list)
        print(count)
    elif task.host.platform == 'iosxr':
        find_ip_iosxr(task)
    elif task.host.platform == 'nxos':
        find_ip_nxos(task)
    else:
        find_ip_junos(task)
    l = list([item for item in count if count[item]>1])
    print(item)
    print(l)

def get_net_ios(task):
    output = task.run(task=send_command, command="show ip int brief", severity_level=logging.DEBUG)
    task.host["facts"] = output.scrapli_response.genie_parse_output()
#    print(task.host)
#    pprint(task.host["facts"])
    sub_list = []
#    print(task.host["facts"]["interface"].items())
    for key,value in task.host["facts"]["interface"].items():
 #       print(value["ip_address"])
        if value["ip_address"] != "unassigned":
#            print("inside")
            sub_list.append(value["ip_address"])
#    print("Inner list for host {} is {}".format(task.host,sub_list))
#    print("i am outside for loop")
    return(sub_list)




#devices = nr.filter(F(groups__contains='cloud'))
results = nr.run(task=get_net)