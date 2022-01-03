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
    pprint(task.host["facts"])
    inner_list = []
    outer_list = []
    test_dict = {}
    for key,value in task.host["facts"]["cdp"]["index"].items():
        inner_list.append(key["device_id"])
        inner_list.append(key["port_id"])
        test_dict[key["local_interface"]] = outer_list.append(inner_list)
    pprint(test_dict)





results = nr.run(task=pull_cdp)
#print_result(results)
#ipdb.set_trace()
