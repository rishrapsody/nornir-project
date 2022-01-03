from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb
from pprint import pprint

nr = InitNornir(config_file="config.yml")

def pull_cdp(task):
    output = task.run(task=send_command, command="show cdp neighbors")
    task.host["facts"] = output.scrapli_response.genie_parse_output()
#    print(task.host)
#    print(task.host["facts"])
    inner_list = []
    outer_list = []
    test_dict = {}
    for key,value in task.host["facts"]["cdp"]["index"].items():
#        print(key)
#        print(value)
        inner_list.append(value["device_id"])
        inner_list.append(value["port_id"])
#        print(inner_list)
        test_dict[value["local_interface"]] = inner_list
    print("Parsed output for {} is:> {}".format({task.host},test_dict))





results = nr.run(task=pull_cdp)
#print_result(results)
#ipdb.set_trace()
