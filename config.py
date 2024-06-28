zabbix_server = 'http://zabbix-host/api_jsonrpc.php'
zabbix_user = 'user'
zabbix_password = 'password'
file_name='TSMetrics.xlsx'
#time_intervals = [86400, 172800, 259200, 345600, 432000, 518400, 604800]
time_intervals = [604800, 518400, 432000, 345600, 259200, 172800, 86400]

calls_parameters = [
    {
        "group_names": ['Hosts'],
        "metric_keys": ['system.cpu.util.total','vm.memory.size[pavailable]'],
        "history_parameter": 0
    },
    {
        "group_names": ['Main SOA Servers','Standby SOA Servers'],
        "metric_keys": [ 'jmx["java.lang:type=Memory",HeapMemoryUsage.used]'],
        "history_parameter": 3
    },
    {
        "group_names": ['TS Statistics'],
        "metric_keys": ['loadAccLogSum'],
        "history_parameter": 3
    },
]
