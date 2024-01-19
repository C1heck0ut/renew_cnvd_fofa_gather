# cnvd_fofa_gather
# 0x00 前言
本项目是对项目 https://github.com/colind0pe/new_cnvd_fofa_gather 进行了修改，增加了新的可替换接口，修改了调用规则

# 0x01 简介
通过公司名称，在fofa上搜索可能存在通用产品的公司，原理是判断网站标题数目以及独立IP数达到一定条件时将该标题以及公司名称导出；如果想挖掘cnvd证书，可导出注册资金大于5000w的公司到这个脚本中进行通用系统收集。

# 0x02 使用方法
修改脚本第10、11行为你的FOFA账号的邮箱和API KEY

填入fofa账号的email和API_KEY

email = 'YOUR_EMAIL'

api_key = 'API_KEY'

将公司名称放入gs.txt文件中，执行该脚本即可。

python3 cnvd_fofa_gather.py
