# nowgoalreader-server
数据源接口服务端 提供RestfulAPI

## 使用流程

* 1.配置好nowgoalreader_server.conf，修改downloader为读取数据接口
* 2.运行 nohup python nowgoalreader_server.py &
* 3.通过其他机器访问 例: "curl http://127.0.0.1:5000/nowgoalreader/basketball/score?europeId=300056"