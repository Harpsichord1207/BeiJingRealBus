#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Usage:
    bus <bus_code>
    bus [-ih]

Options:
    -h              Show help information
    -i              Show application information

Example:
    bus 438         Show stations, directions and positions of bus 438
"""

import requests
import re
import json
from docopt import docopt
from bs4 import BeautifulSoup
from time import time, sleep
from better_print import print_info, print_direction_and_station

index_url = r'http://www.bjbus.com/home/index.php'
main_url = r'http://www.bjbus.com/home/ajax_rtbus_data.php'


def get_bus_code_list():
    with open('db/bus.txt', 'r', encoding='utf-8') as f:
        db_data = json.loads(f.read())
        if db_data['time'] >= time() - 12*3600:
            print('Getting bus code from db...')
            return db_data['data']
    resp = requests.get(index_url).content.decode('utf-8')
    print('Getting bus code from web...')
    bus_code_string = re.findall('<dd id="selBLine">([\s\S]*?)</dd>', resp)
    bus_code_string = bus_code_string[0].strip().replace('<a href="javascript:;">', '')
    bus_code_list = bus_code_string.split('</a>')[:-1]
    db_data = {
        'time': time(),
        'data': bus_code_list
    }
    with open('db/bus.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(db_data, ensure_ascii=False, indent=2))
    return bus_code_list


def get_bus_direction(bus_code):
    with open('db/direction.txt', 'r', encoding='utf-8') as f:     # TODO：'r+' is not simple / SegmentFault
        db_data = json.loads(f.read())
        bus_direction = db_data.get(str(bus_code))
        if bus_direction and bus_direction['time'] >= time() - 12*3600:
            print('Getting bus direction from db...')
            return bus_direction['data']
    payload = {
        'act': 'getLineDirOption',
        'selBLine': bus_code
    }
    resp = requests.get(url=main_url, params=payload).content.decode('utf-8')
    print('Getting bus direction from web...')
    direction_no = re.findall('value="(\d+)"', resp)
    if not direction_no:
        print('%s路公交车未找到' % str(bus_code))
        return []
    direction_path = re.findall(str(bus_code) + '(.*?)<', resp)
    data = []
    for j in range(2):
        direction_path_str = direction_path[j][1:-1]
        data.append([direction_no[j], direction_path_str])
    with open('db/direction.txt', 'r+', encoding='utf-8') as f:
        db_data[str(bus_code)] = {
            'time': time(),
            'data': data
        }
        f.write(json.dumps(db_data, ensure_ascii=False, indent=2))
    return data


def get_bus_stations(bus_code, direction):
    with open('db/station.txt', 'r', encoding='utf-8') as f:
        db_data = json.loads(f.read())
        bus_station = db_data.get(str(bus_code) + '#' + str(direction))
        if bus_station and bus_station['time'] >= time() - 12 * 3600:
            print('Getting bus station from db...')
            return bus_station['data']
    payload = {
        'act': 'getDirStationOption',
        'selBLine': bus_code,
        'selBDir': direction
    }
    resp = requests.get(main_url, params=payload).content.decode('utf-8')
    print('Getting bus station from web...')
    stations = re.findall('<option value="\d*?">(.*?)</option>', resp)[1:]
    with open('db/station.txt', 'w+', encoding='utf-8') as f:
        db_data[str(bus_code) + '#' + str(direction)] = {
            'time': time(),
            'data': stations
        }
        f.write(json.dumps(db_data, ensure_ascii=False, indent=2))
    return stations


def get_bus_status(bus_code, direction, station_no):
    payload = {
        'act': 'busTime',
        'selBLine': bus_code,
        'selBDir': direction,
        'selBStop': station_no
    }
    resp = requests.get(main_url, params=payload).json()['html']
    print('Getting bus status from web...')
    soup = BeautifulSoup(resp, 'html.parser')
    path = str(soup.find(id="lm").contents[0])      # 将bs的string类型转换为普通string
    station_name, operation_time, *_ = soup.article.p.string.split('\xa0')
    tip = ''
    for content in soup.article.p.next_sibling.contents:
        if isinstance(content, str):
            tip += content.replace('\xa0', '')
        else:
            tip += content.string
    bus_position = []
    for tag in soup.find_all('i', attrs={'clstag': True}):
        temp_dic = dict()
        station_id = tag.parent['id']
        temp_dic['near_station'] = False if 'm' in station_id else True
        station_id = station_id.replace('m', '')
        temp_dic['station_id'] = station_id
        temp_dic['distance'] = int(tag['clstag']) if tag['clstag'].isdigit() else -1
        bus_position.append(temp_dic)
    result = {
        'path': path,
        'station_name': station_name,
        'operation_time': operation_time,
        'bus_position': bus_position,   # A list of dict
        'tip': tip
    }
    return result


if __name__ == "__main__":
    args = docopt(__doc__)
    if args['-i']:
        print_info(__doc__)
    else:
        b_code = args['<bus_code>']
        if b_code:
            [d0, _], [d1, _] = get_bus_direction(b_code)
            stations0 = get_bus_stations(b_code, d0)
            stations1 = get_bus_stations(b_code, d1)
            while 1:
                direction0 = []
                direction1 = []
                status0 = get_bus_status(b_code, d0, len(d0))
                status1 = get_bus_status(b_code, d1, len(d1))
                pos0 = status0['bus_position']
                pos0_id = [p['station_id'] for p in pos0]
                pos1 = status1['bus_position']
                pos1_id = [p['station_id'] for p in pos1]
                for i, d in enumerate(stations0):
                    bus = ' '
                    if str(i+1) in pos0_id:
                        bus = 'B'
                    direction0.append([i+1, d, bus])
                for i, d in enumerate(stations1):
                    bus = ' '
                    if str(i + 1) in pos1_id:
                        bus = 'B'
                    direction1.append([i+1, d, bus])
                print_direction_and_station(direction0, direction1, status0['operation_time'], status1['operation_time'])
                sleep(5)
