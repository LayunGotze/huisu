import time
import re
from api.backtrack_use.mongodb_link import origin,events_tracking
"""
该文件提供了事件回溯接口需要使用到的基本接口函数
"""

#国家映射词典，从'CHN'映射到中文名
country_dict={'AND': '安道尔', 'ARE': '阿联酋', 'AFG': '阿富汗', 'ATG': '安提瓜和巴布达', 'AIA': '安圭拉',
              'ALB': '阿尔巴尼亚', 'ARM': '亚美尼亚', 'AGO': '安哥拉', 'ATA': '南极洲', 'ARG': '阿根廷',
              'ASM': '美属萨摩亚', 'AUT': '奥地利', 'AUS': '澳大利亚', 'ABW': '阿鲁巴', 'ALA': '奥兰群岛',
              'AZE': '阿塞拜疆', 'BIH': '波黑', 'BRB': '巴巴多斯', 'BGD': '孟加拉', 'BEL': '比利时',
              'BFA': '布基纳法索', 'BGR': '保加利亚', 'BHR': '巴林', 'BDI': '布隆迪', 'BEN': '贝宁',
              'BLM': '圣巴泰勒米岛', 'BMU': '百慕大', 'BRN': '文莱', 'BOL': '玻利维亚', 'BES': '荷兰加勒比区',
              'BRA': '巴西', 'BHS': '巴哈马', 'BTN': '不丹', 'BVT': '布韦岛', 'BWA': '博茨瓦纳',
              'BLR': '白俄罗斯', 'BLZ': '伯利兹', 'CAN': '加拿大', 'CCK': '科科斯群岛', 'CAF': '中非',
              'CHE': '瑞士', 'CHL': '智利', 'CMR': '喀麦隆', 'COL': '哥伦比亚', 'CRI': '哥斯达黎加',
              'CUB': '古巴', 'CPV': '佛得角', 'CXR': '圣诞岛', 'CYP': '塞浦路斯', 'CZE': '捷克', 'DEU': '德国',
              'DJI': '吉布提', 'DNK': '丹麦', 'DMA': '多米尼克', 'DOM': '多米尼加', 'DZA': '阿尔及利亚',
              'ECU': '厄瓜多尔', 'EST': '爱沙尼亚', 'EGY': '埃及', 'ESH': '西撒哈拉', 'ERI': '厄立特里亚',
              'ESP': '西班牙', 'FIN': '芬兰', 'FJI': '斐济群岛', 'FLK': '马尔维纳斯群岛（福克兰）',
              'FSM': '密克罗尼西亚联邦', 'FRO': '法罗群岛', 'FRA': '法国', 'GAB': '加蓬', 'GRD': '格林纳达',
              'GEO': '格鲁吉亚', 'GUF': '法属圭亚那', 'GHA': '加纳', 'GIB': '直布罗陀', 'GRL': '格陵兰',
              'GIN': '几内亚', 'GLP': '瓜德罗普', 'GNQ': '赤道几内亚', 'GRC': '希腊', 'SGS': '南乔治亚岛和南桑威奇群岛',
              'GTM': '危地马拉', 'GUM': '关岛', 'GNB': '几内亚比绍', 'GUY': '圭亚那', 'HKG': '中国香港',
              'HMD': '赫德岛和麦克唐纳群岛', 'HND': '洪都拉斯', 'HRV': '克罗地亚', 'HTI': '海地', 'HUN': '匈牙利',
              'IDN': '印尼', 'IRL': '爱尔兰', 'ISR': '以色列', 'IMN': '马恩岛', 'IND': '印度', 'IOT': '英属印度洋领地',
              'IRQ': '伊拉克', 'IRN': '伊朗', 'ISL': '冰岛', 'ITA': '意大利', 'JEY': '泽西岛', 'JAM': '牙买加',
              'JOR': '约旦', 'JPN': '日本', 'KHM': '柬埔寨', 'KIR': '基里巴斯', 'COM': '科摩罗', 'KWT': '科威特',
              'CYM': '开曼群岛', 'LBN': '黎巴嫩', 'LIE': '列支敦士登', 'LKA': '斯里兰卡', 'LBR': '利比里亚',
              'LSO': '莱索托', 'LTU': '立陶宛', 'LUX': '卢森堡', 'LVA': '拉脱维亚', 'LBY': '利比亚', 'MAR': '摩洛哥',
              'MCO': '摩纳哥', 'MDA': '摩尔多瓦', 'MNE': '黑山', 'MAF': '法属圣马丁', 'MDG': '马达加斯加',
              'MHL': '马绍尔群岛', 'MKD': '马其顿', 'MLI': '马里', 'MMR': '缅甸', 'MAC': '中国澳门', 'MTQ': '马提尼克',
              'MRT': '毛里塔尼亚', 'MSR': '蒙塞拉特岛', 'MLT': '马耳他', 'MDV': '马尔代夫', 'MWI': '马拉维',
              'MEX': '墨西哥', 'MYS': '马来西亚', 'NAM': '纳米比亚', 'NER': '尼日尔', 'NFK': '诺福克岛',
              'NGA': '尼日利亚', 'NIC': '尼加拉瓜', 'NLD': '荷兰', 'NOR': '挪威', 'NPL': '尼泊尔', 'NRU': '瑙鲁',
              'OMN': '阿曼', 'PAN': '巴拿马', 'PER': '秘鲁', 'PYF': '法属波利尼西亚', 'PNG': '巴布亚新几内亚',
              'PHL': '菲律宾', 'PAK': '巴基斯坦', 'POL': '波兰', 'PCN': '皮特凯恩群岛', 'PRI': '波多黎各',
              'PSE': '巴勒斯坦', 'PLW': '帕劳', 'PRY': '巴拉圭', 'QAT': '卡塔尔', 'REU': '留尼汪', 'ROU': '罗马尼亚',
              'SRB': '塞尔维亚', 'RUS': '俄罗斯', 'RWA': '卢旺达', 'SLB': '所罗门群岛', 'SYC': '塞舌尔', 'SDN': '苏丹',
              'SWE': '瑞典', 'SGP': '新加坡', 'SVN': '斯洛文尼亚', 'SJM': '斯瓦尔巴群岛和 扬马延岛', 'SVK': '斯洛伐克',
              'SLE': '塞拉利昂', 'SMR': '圣马力诺', 'SEN': '塞内加尔', 'SOM': '索马里', 'SUR': '苏里南', 'SSD': '南苏丹',
              'STP': '圣多美和普林西比', 'SLV': '萨尔瓦多', 'SYR': '叙利亚', 'SWZ': '斯威士兰', 'TCA': '特克斯和凯科斯群岛',
              'TCD': '乍得', 'TGO': '多哥', 'THA': '泰国', 'TKL': '托克劳', 'TLS': '东帝汶', 'TUN': '突尼斯',
              'TON': '汤加', 'TUR': '土耳其', 'TUV': '图瓦卢', 'TZA': '坦桑尼亚', 'UKR': '乌克兰', 'UGA': '乌干达',
              'USA': '美国', 'URY': '乌拉圭', 'VAT': '梵蒂冈', 'VEN': '委内瑞拉', 'VGB': '英属维尔京群岛',
              'VIR': '美属维尔京群岛', 'VNM': '越南', 'WLF': '瓦利斯和富图纳', 'WSM': '萨摩亚', 'YEM': '也门',
              'MYT': '马约特', 'ZAF': '南非', 'ZMB': '赞比亚', 'ZWE': '津巴布韦', 'CHN': '中国', 'COG': '刚果（布）',
              'COD': '刚果（金）', 'MOZ': '莫桑比克', 'GGY': '根西岛', 'GMB': '冈比亚', 'MNP': '北马里亚纳群岛',
              'ETH': '埃塞俄比亚', 'NCL': '新喀里多尼亚', 'VUT': '瓦努阿图', 'ATF': '法属南部领地', 'NIU': '纽埃',
              'UMI': '美国本土外小岛屿', 'COK': '库克群岛', 'GBR': '英国', 'TTO': '特立尼达和多巴哥', 'VCT': '圣文森特和格林纳丁斯',
              'TWN': '中国台湾', 'NZL': '新西兰', 'SAU': '沙特阿拉伯', 'LAO': '老挝', 'PRK': '朝鲜 北朝鲜',
              'KOR': '韩国', 'PRT': '葡萄牙', 'KGZ': '吉尔吉斯斯坦', 'KAZ': '哈萨克斯坦', 'TJK': '塔吉克斯坦',
              'TKM': '土库曼斯坦', 'UZB': '乌兹别克斯坦', 'KNA': '圣基茨和尼维斯', 'SPM': '圣皮埃尔和密克隆', 'SHN': '圣赫勒拿',
              'LCA': '圣卢西亚', 'MUS': '毛里求斯', 'CIV': '科特迪瓦', 'KEN': '肯尼亚', 'MNG': '蒙古'}

#event_code 0-20对应的映射，来自于EVENTCODES
#0-4 5-9 10-14 15-19  分别 对呀口头合作，实质性合作，口头冲突，实质冲突
event_code_map={'官方声明':'01','呼吁':'02','表达合作意向':'03','商议':'04',
                '从事外交合作': '05','开展物质合作':'06','提供援助':'07','不再反对':'08','调查':'09',
                '询问': '10','反对':'11','拒绝':'12','威胁':'13','抗议':'14',
                '展现武力': '15','减少联系':'16','逼迫':'17','攻击':'18','战斗':'19'}



def timestr2stamp10(time_str):
    #将'20180501'的字符串转换为10位时间戳
    return int(time.mktime(time.strptime(time_str, "%Y%m%d")))

def timestr2stamp13(timestr):
    #将形如"20180506"的时间字符串转换成13位时间戳整数，便于前端展示
    return int(time.mktime(time.strptime(timestr,'%Y%m%d'))*1000)

def senid2index(sentid):
    #将形如"592436239afc10f2c9a240c8_12"的SENTID分解为id和index，其中，index转换为整数
    res=sentid.split('_')
    id=res[0]
    index=int(res[1])
    return id,index

def create_time_dict(start,end):
    #根据提供的开始和结束时间（字符串），生成这期间的所有日期构成的字典
    #便于根据日期统计热度
    #返回的字典形如：{'20180501': 0, '20180502': 0, '20180503': 0}
    start_int = timestr2stamp10(start)
    end_int = timestr2stamp10(end)
    ret_data = {start: 0}
    begin = start_int + 86400
    while begin <= end_int:
        # 生成从START到END的日期，ret_data为返回数据
        time_tmp = time.strftime("%Y%m%d", time.localtime(begin))
        ret_data[time_tmp] = 0
        begin = begin + 86400
    print(ret_data)
    return ret_data

def gkg_person_list(data):
    #提取GKG中的人物名称
    #将gkg中的person字符串转换成list
    list=[]
    if(data==""):
        return list
    list=data.split(';')
    return list

def gkg_country_extract(text):
    #提取GKG中的国家名称
    #返回提取到的三字符信息list
    country_pattern = re.compile("[A-Z]{3}")
    match = re.finditer(country_pattern, text)
    res=[]
    for item in match:
        res.append(item.group(0))
    return res

def dict_sort(dict,top):
    #将dict按值排序，返回前num位的二维数组，每个数字包含key,value
    items=dict.items()
    backitem=[[v[1],v[0]] for v in items]
    backitem.sort(reverse=True)
    backitem=backitem[:top]
    for item in backitem:
        item.reverse()
    return backitem

def data2html(data):
    #将形如{'20180501': 607, '20180502': 0, '20180503': 0, '20180504': 0, '20180505': 0, '20180506': 0}
    #的字典数据转换为前端输入的LIST数据
    ret={'hot':[]}
    max_value=-1
    min_value=0
    for key in data:
        ret['hot'].append([timestr2stamp13(key),data[key]])
        if data[key]>max_value:
            max_value=data[key]
    ret['hot'].sort()
    ret['max_value']=max_value
    ret['min_value']=min_value
    print(ret)
    return ret

def rankdata(data,key_name,value_name):
    #将dict_sort输出的排名字典，转换为前端适合的字典形式
    #从[['Donald Trump', 103], ['Trump', 76], ['Buffett', 13], ['Emmanuel Macron', 10], ['Mueller', 9], ['Kim Jong-un', 9], ['Barack Obama', 9], ['Wolf', 8], ['Stormy Daniels', 8], ['Robert Mueller', 8]]
    #到{'hot': [103, 76, 13, 10, 9, 9, 9, 8, 8, 8], 'person': ['Donald Trump', 'Trump', 'Buffett', 'Emmanuel Macron', 'Mueller', 'Kim Jong-un', 'Barack Obama', 'Wolf', 'Stormy Daniels', 'Robert Mueller']}
    #data是原始数据，key_name是要生成的名称（国家或者人名），value_name是值的名称
    ret_data={key_name:[],value_name:[]}
    for item in data:
        ret_data[key_name].append(item[0])
        ret_data[value_name].append(item[1])
    return ret_data