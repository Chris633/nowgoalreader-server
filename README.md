# nowgoalreader-server
数据源接口服务端 提供RestfulAPI

## 使用流程

* 0.确定etcd已运行，确定已安装最新python-etcd与flask
* 1.配置好 nowgoalreader_server.conf，并修改downloader.py为读取数据接口
* 2.运行 nowgoalreader_server.py
* 3.通过其他机器访问，例: "curl http://127.0.0.1:5000/nowgoalreader/basketball/score?europeId=300056"
* 4.或直接在test目录下运行testclient.py，例:"python testclient.py basketball score 300056"

** Note: **
* 注册运用etcd的python客户端[python-etcd](https://github.com/jplana/python-etcd)，该客户端用的etcdctl_api v2
* 其中testclient　：master分支为输出xml格式数据，text分支为在命令行输出人眼友好的文字数据。

