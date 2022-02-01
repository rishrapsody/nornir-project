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


nr = InitNornir(config_file="config.yml")

def load_vars(task):
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yml", severity_level=logging.DEBUG)
    task.host["facts"] = data.result
#    ipdb.set_trace()
    create_bgp(task)

def create_bgp(task):
    template = task.run(
        task=template_file, template="bgp.j2", path=f"./templates/{task.host.platform}-templates", severity_level=logging.DEBUG)
    task.host["bgp_config"] = template.result
    rendered = task.host["bgp_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)

def get_int(task):
    output = task.run(task=send_command, command="show version")
    task.host["facts"] = output.scrapli_response.genie_parse_output()

devices = nr.filter(F(groups__contains='rtrgroup'))
results = devices.run(task=get_int)
print_result(results)
ipdb.set_trace()
