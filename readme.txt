弱网健康问答存储转发站
偏远地区卫生员在断续网络下采集基础健康问答和小型附件，分块校验、离线排队并在重连后与医生端回执合并。

测试：python3 -m unittest discover -s tests/rural_store_forward -p 'test_*.py'
构建：python3 -m compileall -q store_forward_health tests/rural_store_forward
验收：python3 -m store_forward_health.station.operator_cli --fixture fixtures/demo.json --database /tmp/rural_store_forward-acceptance.sqlite3
