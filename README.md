## Beijing RealBus
*A CLI Tool for Monitoring Beijing Bus*

### Usage
```
Usage:
    bus <bus_code>
    bus [-ih]

Options:
    -h              Show help information
    -i              Show application information
```

### Example
- Show information
#### Command
```python bus.py -i```

#### Result
```
 ------- BeiJing Real Bus -------
|                                |
|      Author: Harpsichord       |
|   Contact: liutao25@baidu.com  |
 --------------------------------
```

- Monitor Coming Bus 438
#### Command
```python bus.py 438```

#### Result
```
+----+--------------------+------+-----+----+--------------------+------+
| #0 |   UP:5:30-21:00    | Bus0 |     | #1 |  DOWN:6:00-22:00   | Bus1 |
+----+--------------------+------+-----+----+--------------------+------+
| 1  |    永丰公交场站      |      |     | 1  |      西直门北      |      |
| 2  |      丰润中路        |      |     | 2  |    地铁西直门站    |      |
...
...
...
| 16 |       骚子营       |      |     | 16 |       骚子营       |      |
| 17 |        西苑        |      |     | 17 |       小清河       |  B   |
| 18 |    颐和园路东口     |      |     | 18 |       肖家河       |      |
...
...
...
```
#### 'B' in the column Bus1 means a bus near XiaoQingHe station

### Requirements
```
beautifulsoup4==4.6.0
bs4==0.0.1
certifi==2018.1.18
chardet==3.0.4
colorama==0.3.9
docopt==0.6.2
idna==2.6
prettytable==0.7.2
requests==2.18.4
urllib3==1.22
```