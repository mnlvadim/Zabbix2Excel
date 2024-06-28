import xlsxwriter
import time
from pyzabbix import ZabbixAPI
from config import *

def correct_worksheet_name(name):
    invalid_chars="/\\?*[]:"
    for char in invalid_chars:
        name=name.replace(char,"_")
    return name[:31]

def collect_and_write_metrics(zabbix_server, zabbix_user, zabbix_password, group_names, metric_keys, time_intervals, history_parameter):
    bold = workbook.add_format({'bold': True})
    for group_name in group_names:
        safe_name = correct_worksheet_name(group_name)
        worksheet = workbook.add_worksheet(name=safe_name)
        worksheet.write('A1', 'Hosts', bold)
        worksheet.set_column('A:A', 42)
        worksheet.set_column('B:Z', 11)
        col = 1
        for key in metric_keys:
            for interval in time_intervals:
                col_name = f"{key}_{interval // 86400}d_ago"
                worksheet.write(0, col, col_name, bold)
                col += 1

        group_id = zapi.hostgroup.get(filter={'name': group_name})[0]['groupid']
        hosts = zapi.host.get(groupids=group_id, output=['name', 'hostid'])

        row = 1
        for host in hosts:
            host_name = host['name']
            host_id = host['hostid']
            worksheet.write(row, 0, host_name)
            col = 1
            for key in metric_keys:
                for interval in time_intervals:
                    current_time = int(time.time())
                    item = zapi.item.get(hostids=host_id, search={'key_': key}, output=['itemid'])
                    if item:
                        item_id = item[0]['itemid']
                        history = zapi.history.get(itemids=item_id, time_from=current_time - interval, time_till= current_time - interval+120, output='extend', history=history_parameter, limit=1)
                        value = history[0]['value'] if history else 'N/A'
                    else:
                        value = 'N/A'
                    worksheet.write(row, col, value)
                    col += 1
            row += 1


zapi = ZabbixAPI(zabbix_server)
zapi.login(zabbix_user,zabbix_password)
workbook = xlsxwriter.Workbook(file_name)
for params in calls_parameters:
    collect_and_write_metrics(
        zabbix_server=zabbix_server,
        zabbix_user=zabbix_user,
        zabbix_password=zabbix_password,
        group_names=params["group_names"],
        metric_keys=params["metric_keys"],
        time_intervals=time_intervals,
        history_parameter=params["history_parameter"]
    )
workbook.close()
print("Excel файл успешно создан!")
zapi.logout
