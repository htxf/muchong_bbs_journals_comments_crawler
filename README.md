# muchong_bbs_journals_comments_crawler

最近准备投论文，想投北大核心期刊列出的31个期刊中的一个。先在网上查了查这些期刊，想了解些基本情况。发现了[小木虫中文期刊点评](http://muchong.com/bbs/journal_cn.php)，这上边有很多期刊，有期刊的基本信息，也有网友的点评，很不错。但是要一个一个搜索的，再点开来看不能很好的相互比较，要重新查看时，又得重新搜索。所以想把这31个期刊的相关信息爬取下来。

有了之前爬取Instagram和Tumblr的经验，这次写的就快多了。与上次不同的是，这次想要的信息不是通过XMLHttpRequest传递的，返回的都是html文件。
最终将爬到的信息存储为json格式。

有个问题，比如搜索“计算机工程”时，会同时显示“计算机工程”，“计算机工程与设计”，“计算机工程与应用”，而在代码中写的寻找“计算机工程”的方法有问题，还是会找见“计算机工程与应用”。后来想，应该找见所有的a标签，然后a中的text与“计算机工程”完全一致时才可进行下一步。
