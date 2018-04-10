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
```python bus.py -i```
```
 ------- BeiJing Real Bus -------
|                                |
|      Author: Harpsichord       |
|   Contact: liutao25@baidu.com  |
 --------------------------------
```

- Monitor Coming Bus 438
```python bus.py 438```
```
+----+--------------------+------+-----+----+--------------------+------+
| #0 |   UP:5:30-21:00    | Bus0 |     | #1 |  DOWN:6:00-22:00   | Bus1 |
+----+--------------------+------+-----+----+--------------------+------+
| 1  |    永丰公交场站    |      |     | 1  |      西直门北      |      |
| 2  |      丰润中路      |      |     | 2  |    地铁西直门站    |      |
...
...
...
| 16 |       骚子营       |      |     | 16 |       骚子营       |      |
| 17 |        西苑        |      |     | 17 |       小清河       |  B   |
| 18 |    颐和园路东口    |      |     | 18 |       肖家河       |      |
...
...
...
```
#### 'B' in the column Bus1 means a bus near XiaoQingHe station