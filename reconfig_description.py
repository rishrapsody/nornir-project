from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb
from pprint import pprint

nr = InitNornir(config_file="config.yml")

def pull_cdp(task):
    output = task.run(task=send_command, command="show cdp neighbors")
    task.host["facts"] = output.scrapli_response.genie_parse_output()
    pprint(task.host["facts"])


results = nr.run(task=pull_cdp)
#print_result(results)
ipdb.set_trace()
