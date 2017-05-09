import requests
from bs4 import BeautifulSoup
import json
import codecs

# 读取期刊名存入journal_names
journal_names = []

with open('./bdhxqk-zj-pure-name.txt', 'r') as f:
    for line in f.readlines():
        journal_names.append(line.strip('\n'))

print(journal_names)


def find_info_single(info_name):
    info = soup2.find(
        'td', text=info_name).next_sibling.next_sibling.text.strip('\n')
    return info


def find_info_list(info_name):
    infos = soup2.find('td', text=info_name).next_sibling.next_sibling.text
    infos_list = infos.split('\n')
    infos_list = [x.strip('\xa0') for x in infos_list]
    infos_list = [x for x in infos_list if x != '']
    return infos_list


def find_comment_author_name(index):
    # 0不是第一个，有两个其他东西
    # 第3个是第一个
    name = soup2.find_all('span', class_='xmc_blue')[index + 2].find('a').text
    return name


def find_comment_time(index):
    time = soup2.find_all('span', class_='xmc_lm10')[
        index].text.split('\n')[1].strip('\xa0 ')
    return time[3:]


def find_comment_author_info(index, info_name):
    tag = soup2.find_all('td', class_='xmc_lp20')[
        index].find('b', text=info_name)
    if (str(tag) != 'None'):
        info = tag.next_sibling
    else:
        info = '无'
    return info


def find_comment_content(index):
    # print(index)
    content = ''
    try:
        for ele in soup2.find_all('td', class_='xmc_lp20')[index].find_all('br')[1].next_siblings:
            content = content + str(ele)
    except:
        content = soup2.find_all('td', class_='xmc_lp20')[index].text
    return content.lstrip()


def find_all_comments():
    comment_len = len(soup2.find_all('span', class_='xmc_lm10'))
    comments = []
    for index in range(0, comment_len):
        # print(index)
        comment = {}
        comment['作者'] = find_comment_author_name(index)
        comment['时间'] = find_comment_time(index)
        comment['研究方向'] = find_comment_author_info(index, '研究方向:')
        comment['投稿周期'] = find_comment_author_info(index, '投稿周期:')
        comment['录用情况'] = find_comment_author_info(index, '录用情况:')
        comment['审稿费'] = find_comment_author_info(index, '审稿费:')
        comment['版面费'] = find_comment_author_info(index, '版面费:')
        comment['内容'] = find_comment_content(index)
        comments.append(comment)
    return comments


headers = {
    'cookie': '粘贴控制台处的cookie',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'host': 'muchong.com',
    'referer': 'http://muchong.com/bbs/journal_cn.php',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive'
}

journals = []

for i in range(len(journal_names)):

    # 根据期刊名，name='xx'去get请求url1
    payload1 = {'name': journal_names[i].encode('gb2312')}

    url1 = 'http://muchong.com/bbs/journal_cn.php?issn=&tagname=&ssubmit=%CB%D1%CB%F7'

    print('第' + str(i) + '个期刊，第一次请求地址', url1)

    r1 = requests.get(url1, headers=headers, params=payload1)

    soup1 = BeautifulSoup(r1.text, "html.parser")

    print('第' + str(i) + '个期刊，搜索名字，返回代码', r1.status_code)

    try:
        # 具体的期刊点评信息get请求url2
        url2_tail = soup1.find('th', class_='xmc_line_bno').find('a').get('href')

        url2 = 'http://muchong.com/bbs/' + url2_tail

        print('第' + str(i) + '个期刊，第二次请求地址', url2)

        r2 = requests.get(url2, headers=headers)

        soup2 = BeautifulSoup(r2.text, "html.parser")

        print('第' + str(i) + '个期刊，查询信息与评论，返回代码', r2.status_code)

        journal = {}

        journal['期刊名'] = find_info_single('期刊名：')
        journal['主办单位'] = find_info_single('主办单位：')
        journal['出版地'] = find_info_single('出版地：')
        journal['复合影响因子'] = find_info_single('复合影响因子：')
        journal['综合影响因子'] = find_info_single('综合影响因子：')
        journal['投稿录用比例'] = find_info_single('投稿录用比例：')
        journal['审稿速度'] = find_info_single('审稿速度：')
        journal['审稿费用'] = find_info_single('审稿费用：')
        journal['版面费用'] = find_info_single('版面费用：')
        journal['数据库收录/荣誉'] = find_info_list('数据库收录/荣誉：')
        journal['偏重的研究方向'] = find_info_list('偏重的研究方向：')
        journal['所有评论'] = find_all_comments()

        print('第' + str(i) + '个期刊' +
              journal['期刊名'] + '共有评论' + str(len(journal['所有评论'])) + '条。')

        journals.append(journal)
    except:
        print('搜索不到这个期刊：', journal_names[i])

print('共有期刊数量', len(journals))

# 这里用codecs库打开文件，可以指定写入时的编码格式，
# 用python自带的open方法，不能指定
with codecs.open('./journals.json', 'w', encoding='utf-8') as f:
    # 本来在这里json.dump方法有一个参数是encoding，但这个版本的没有
    # 若不写ensure_ascii=False（默认是True），文件中都是'\uxxx\uxxx'
    json.dump(journals, f, ensure_ascii=False)
    print('将所有杂志的信息和评论存储在了journals.json中。')
