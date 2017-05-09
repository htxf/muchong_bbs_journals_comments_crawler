# 从PDF中复制出了TP 自动化技术、计算机技术，
# 进行预处理，去掉第一行，去掉每一行的数字和空格，
# 每一行只留期刊名
journal_names = []

with open('./bdhxqk-zj.txt', 'r') as f:
    for line in f.readlines():
        journal_names.append(line)

del journal_names[0]

pure_names = []

for name in journal_names:
    rank_name = name.split(' ')
    pure_names.append(rank_name[1].strip('\n'))

with open('./bdhxqk-zj-pure-name.txt', 'w') as f:
    for name in pure_names:
        f.write(name + '\n')
