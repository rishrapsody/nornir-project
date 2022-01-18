from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
import ipdb
from pprint import pprint
import logging

nr = InitNornir(config_file="config.yml")

def pull_cdp(task):
    output = task.run(task=send_command, command="show cdp neighbors",severity_level=logging.DEBUG)
    task.host["facts"] = output.scrapli_response.genie_parse_output()
#    print(task.host["facts"])
 #   inner_list = []
#    outer_list = []
    test_dict = {}
    for key,value in task.host["facts"]["cdp"]["index"].items():
#        print(key)
#        print(value)
        inner_list = []
        inner_list.append(value["device_id"])
        inner_list.append(value["port_id"])
        test_dict[value["local_interface"]] = inner_list
#    print("Parsed output for {} is:> {}".format({task.host},test_dict))
    for intf,data in test_dict.items():
#        print(intf)
#        print(data)
        i=0
#        print(len(data))
        while(i<len(data)):
            j=i+1
            task.run(task=send_configs, configs=["interface {}".format(intf),"description local {} to remote port {} on device {}".format(intf,data[j],data[i]),"exit"])
            i=i+2


results = nr.run(task=pull_cdp)
print_result(results)
#ipdb.set_trace()
