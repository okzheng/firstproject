#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import re
import csv
import jmespath
from pathlib import Path
import math


def parse_lshw():
    parent_path = Path('C:\\Users\LanLan\\Desktop\\工作\\east-1-lshw-json.20190308')
    result = []
    for jsonfile in parent_path.iterdir():
        with jsonfile.open() as file_obj:
            result_row = {}
            data_file = json.load(file_obj)
            # data_file = file_obj.read()
            # print(type(file_obj))
            # print(type(data_file))

            hostname = jmespath.search('id', data_file)
            uuid = jmespath.search('configuration.uuid', data_file)
            product = jmespath.search('product', data_file).split('(')[0].strip()
            vendor = jmespath.search('vendor', data_file)
            serial = jmespath.search('serial', data_file)
            print(hostname, uuid, product, vendor, serial)
            result_row['hostname'] = hostname
            result_row['uuid'] = uuid
            result_row['product'] = product
            result_row['vendor'] = vendor
            result_row['serial'] = serial
            result_row['BIOS'], result_row['CPU'] = (parse_description(data_file, 'BIOS', 'CPU'))
            result_row['power'] = parse_power(data_file)
            result_row['memory'] = parse_memory(data_file)
            ip = parse_ip(data_file)
            if not ip:
                ip = jsonfile.name[0:-10]
            result_row['ip'] = ip
            result.append(result_row)
    return result


def parse_description(dict_data, *items):
    result = []
    for item in items:
        item = jmespath.search("children[0].children[?description=='" + item + "'].version | [0]", dict_data)
        # item = jmespath.search("children[0].children[?contains(description,'"+item+"') == 'true'].version", dict_data)
        print(item)
        result.append(item)
    return result


def parse_memory(dict_data):
    memory = jmespath.search("children[0].children[?id=='memory'].size | [0]", dict_data)
    if memory:
        print("memory is :", memory / 1024 / 1024 / 1024)
        return math.ceil(memory / 1024 / 1024 / 1024)
    # memory_slot = jmespath.search("length(children[0].children[?id=='memory' || id=='memory:0' || id=='memory:1'].children[].size )", dict_data)
    memory_sum = jmespath.search(
        "sum(children[0].children[?id=='memory' || id=='memory:0' || id=='memory:1'].children[].size)", dict_data)
    memory = memory_sum / 1024 / 1024 / 1024
    print(memory)
    return math.ceil(memory)


def parse_power(dict_data):
    power = jmespath.search("children[?class=='power'].capacity | [0]", dict_data)
    print(power)
    return power


def parse_netcard(dict_data):
    pass


def parse_ip(dict_data):
    ip = jmespath.search("children[?logicalname=='team1.13'].configuration.ip", dict_data)
    print(ip)
    if not ip:
        return ''
    return ip[0]



# old function
def parse_hardwareInfo(*items):
    result_all = []
    # result = {}
    parent_path = 'C:\\Users\LanLan\\Desktop\\工作\\east-1-lshw-json.20190308'
    main_info = ('hostname', 'product', 'vendor', 'serial', 'uuid')
    for jsonfile in os.listdir(parent_path):
        file_path = os.path.join(parent_path, jsonfile)
        print(file_path)
        result = {}
        # result.clear()
        with open(file_path) as data_file:
            jsonobject = json.load(open(file_path, 'r'))

            result_motherboard = {}
            content = jsonobject['children'][0]['children']
            i = 0
            j = 0
            k = 0
            l = 0
            memory = 0
            while i < len(content):
                # print i
                try:
                    # print content[i]['id']
                    if 'BIOS' == content[i]['description']:
                        result_motherboard['BIOS'] = content[i]['version']
                        # print result_motherboard
                        i = i + 1
                        continue
                    elif 'CPU' == content[i]['description']:
                        result_motherboard['CPU'] = content[i]['version']
                        # result_motherboard['frequency'] = result_motherboard['CPU'].split(' ')[-1]
                        i = i + 1
                        continue
                    elif 'System Memory' == content[i]['description']:
                        if 'size' in content[i]:
                            result_motherboard['Memory'] = content[i]['size'] / 1024 / 1024
                        else:
                            memoryslot = len(content[i]['children'])
                            for val in range(memoryslot):
                                print(val)
                                if 'size' in content[i]['children'][val]:
                                    memory = memory + content[i]['children'][val]['size']
                            result_motherboard['Memory'] = memory / 1024 / 1024
                        i = i + 1
                        # break
                        continue
                    while j < len(content[i]['children']):
                        try:
                            # print i,j,content[i]['children'][j]['children'][0]['description']
                            if 'Ethernet controller' == content[i]['children'][j]['children'][0]['description']:
                                if 'Ethernet controller' in result_motherboard.keys():
                                    # temp = result_motherboard['Ethernet controller']
                                    # result_motherboard.pop('Ethernet controller')#del result_motherboard['Ethernet controller']
                                    result_motherboard['Ethernet controller-2'] = \
                                    content[i]['children'][j]['children'][0]['product']
                                    # result_motherboard.pop('Ethernet controller')
                                else:
                                    result_motherboard['Ethernet controller'] = \
                                    content[i]['children'][j]['children'][0]['product']
                            # break
                            if 'RAID bus controller' == content[i]['children'][j]['children'][0]['description']:
                                result_motherboard['RAID bus controller'] = content[i]['children'][j]['children'][0][
                                    'product']
                                # break
                        except KeyError as ex:
                            j = j + 1
                            continue
                        j = j + 1
                except KeyError as e:
                    i = i + 1
                    continue

                #      break
                i = i + 1
            # print result_motherboard
            for item in items:
                if item in main_info:
                    if item == 'hostname':
                        result[item] = jsonobject['id']
                    elif item == 'uuid':
                        result[item] = jsonobject['configuration']['uuid']
                    elif item == 'product':
                        itema = jsonobject['product']
                        # value = re.findall(r'(.*)[(]',itema)
                        result[item] = itema.split('(')[0].strip()
                    elif item == 'serial' or item == 'vendor':
                        result[item] = jsonobject[item]
                        if '...' in result[item]:
                            result[item] = jsonobject['children'][0]['serial']
                elif item == 'ip':
                    while k < len(jsonobject['children']):
                        # print k,len(jsonobject['children'])
                        try:
                            if jsonobject['children'][k]['logicalname'] == 'team1.13':
                                result['ip'] = jsonobject['children'][k]['configuration']['ip']
                        except KeyError as iperror:
                            k = k + 1
                            continue
                        # print jsonobject['children'][k]['logicalname']
                        k = k + 1
                    if 'ip' not in result:
                        result['ip'] = jsonfile[0:-10]
                elif item == 'power':
                    temp = 0
                    while l < len(jsonobject['children']):
                        try:
                            if jsonobject['children'][l]['class'] == 'power':
                                temp = temp + int(jsonobject['children'][l]['capacity'])
                                print(temp)
                        except KeyError as powererror:
                            l = l + 1
                            continue
                        l = l + 1
                    result['power'] = str(temp / 2)
                else:
                    try:
                        result[item] = result_motherboard[item]
                    except KeyError as othererror:
                        result[item] = ''
                # else:
            print(result)
            result_all.append(result)
    # print result_all
    return result_all



def generateCSV(fileName="", dataList=[]):
    # difference of open operation between python2 and python3
    with open(fileName, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        fieldnames = dataList[0].keys()  # solve the problem to automatically write the header
        w.writerow(fieldnames)
        for row in dataList:
            w.writerow(row.values())




if __name__ == "__main__":
    # parse_hardwareInfo('hostname','serial','uuid','CPU','Memory','vendor','product')
    # generateCSV("C:/Users/LanLan/Desktop/工作/north-csvinfo.csv",
    #             parse_hardwareInfo('ip', 'serial', 'hostname', 'BIOS', 'uuid', 'CPU', 'Memory', 'vendor', 'product',
    #                                'power'))
    generateCSV("C:/Users/LanLan/Desktop/工作/north-csvinfo1.csv", parse_lshw())
    # print(jmespath.search("machines[*].x[?name=='a'].state",testa()))
