import tushare as ts

pro = ts.pro_api()


# 股票列表: 获取基础信息数据，包括股票代码、名称、上市日期、退市日期等
def get_stock_basic(**kwargs):
    kwargs['fields'] = ','.join(kwargs['fields'])
    # 查询当前所有正常上市交易的股票列表
    # data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    data = pro.stock_basic(**kwargs)
    print(data)


# get_stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
get_stock_basic(exchange='', list_status='L', fields=['ts_code', 'symbol', 'name', 'area', 'industry', 'list_date'])
# 交易日历
# 股票曾用名
# 沪深股通成分股
# 上市公司基本信息
# 上市公司管理层
# 管理层薪酬和持股
# IPO新股上市
# 备用列表
