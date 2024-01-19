import base64
import json
import re
import time
import requests

requests.packages.urllib3.disable_warnings()

# 填入fofa账号的email和API_KEY
email = ''
api_key = ''

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}


# 调用fofa api的统计聚合接口
def fofa_search(kjgs):
    # fofa_api = 'http://fofa.red/api/v1/search/stats??email={}&key={}&fields=title,ip&qbase64='.format(email,api_key)
    fofa_api = 'http://fofa.red/?key=&page=1&size=100&fields=title,ip&qbase64='
    keyword = '"' + kjgs + '"'
    bs64_keyword = str(base64.b64encode(keyword.encode("utf-8")), "utf-8")
    url = fofa_api + bs64_keyword

    result = requests.get(url, headers=headers, verify=False, timeout=10)
    time.sleep(5)  # fofa限制请求速率，设置请求间隔为5秒
    json_result = json.loads(result.content)
    # print(json_result)
    title_blacklist = ["赌"]
    title_duplicates = {}
    title_unique_ips = {}
    with open('result.txt', 'a+', encoding='utf-8') as file:
        # 遍历JSON数据中的results列表
        file.write(gs+'\n')
        for result in json_result['results']:
            if len(result) >= 2:  # 确保结果至少包含两个元素，即标题和IP地址
                title = result[0]  # 获取标题
                ip = result[1]  # 获取IP地址

                if any(keyword in title for keyword in title_blacklist):
                    continue
                # 如果标题中包含"平台"或"系统"，则继续处理，否则跳过
                if "平台" in title or "系统" in title :
                    # 记录title重复的数量
                    if title in title_duplicates:
                        title_duplicates[title] += 1
                    else:
                        title_duplicates[title] = 1

                    # 如果标题已存在于字典中，将IP地址添加到对应标题的IP集合中
                    if title in title_unique_ips:
                        title_unique_ips[title].add(ip)
                    else:
                        title_unique_ips[title] = {ip}

        # 将去重后的唯一title值，重复项数量，以及每个title对应的不重复IP数量写入result.txt文件
        for title, unique_ips in title_unique_ips.items():
            unique_ip_count = len(unique_ips)
            duplicate_count = title_duplicates.get(title, 0)
            file.write(f'系统名称: {title}, 标题数量: {duplicate_count},ip数量: {unique_ip_count},ip: {unique_ips}\n')


if __name__ == '__main__':
    # 打开公司列表，获取公司名称
    print("开始收集--------")
    for f in open('gs.txt', 'rb'):
        gs = str(f, "utf-8")
        gs = gs.strip()
        print("-----"+gs+"开始收集-----")
        # 去除科技、技术、股份、有限公司等字符
        try:
            if re.search(r'科技', gs):
                print("step1")
                start = re.search(r'科技', gs).span()[0]
                kj = gs[:start]

                # 去除括号内容
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last)
                else:
                    fofa_search(kj)

            elif re.search(r'技术', gs):
                start = re.search(r'技术', gs).span()[1]
                kj = gs[:start]
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last)
                else:
                    fofa_search(kj)

            elif re.search(r'软件', gs):
                start = re.search(r'软件', gs).span()[1]
                kj = gs[:start]
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last)
                else:
                    fofa_search(kj)

            elif re.search(r'股份', gs):
                start = re.search(r'股份', gs).span()[0]
                kj = gs[:start]
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last)
                else:
                    fofa_search(kj)

            elif re.search(r'有限', gs):
                start = re.search(r'有限', gs).span()[0]
                kj = gs[:start]
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last)
                else:
                    fofa_search(kj)

            else:
                if '(' in gs:
                    start = re.search(r'\(', gs).span()[0]
                    end = re.search(r'\)', gs).span()[1]

                    gs_last = gs.replace(gs[start:end], '')

                    fofa_search(gs_last)
                else:
                    kj = gs
                    fofa_search(kj)
        except Exception as u:
            print('main_err:', u)
    print('结果已写入到result.txt文件中。')
