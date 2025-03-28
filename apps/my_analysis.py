import marimo

__generated_with = "0.11.30"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        r"""


        ## part 1

        这个数据集是订单数据，纬度有订单时间、省份（收货地址），指标则有销售量、销售额、退款金额、退货率、成交率、地区分布、下单时间趋势等。

        ### 1、数据理解与处理
        """
    )
    return


@app.cell
def _():
    import pandas as pd
    data = pd.read_csv('tmall_order_report.csv')
    data.head() 
    return data, pd


@app.cell
def _(data):
    data.info()  # 数据集情况 28010 条，6个字段
    return


@app.cell
def _(mo):
    mo.md(r"""列名有空格，需要处理下""")
    return


@app.cell
def _(data):
    data.columns = data.columns.str.strip()  
    data.columns
    return


@app.cell
def _(mo):
    mo.md(r""" 订单付款情况，电商中存在订单未支付的情况""")
    return


@app.cell
def _(data):
    data.isnull().sum()   
    return


@app.cell
def _(data):
    data['收货地址'] = data['收货地址'].str.replace('自治区|维吾尔|回族|壮族|省', '')  # 对省份做个清洗，便于可视化
    data['收货地址'].unique()
    return


@app.cell
def _(mo):
    mo.md(r"""### 2、数据分析可视化""")
    return


@app.cell
def _(mo):
    mo.md(r"""#### 2.1 整体情况""")
    return


@app.cell
def _(data):
    result = {}
    result['总订单数'] = data['订单编号'].count()  
    result['已完成订单数'] = data['订单编号'][data['订单付款时间'].notnull()].count()  
    result['未付款订单数'] = data['订单编号'][data['订单付款时间'].isnull()].count()  
    result['退款订单数'] = data['订单编号'][data['退款金额'] > 0].count()  
    result['总订单金额'] = data['总金额'][data['订单付款时间'].notnull()].sum()  
    result['总退款金额'] = data['退款金额'][data['订单付款时间'].notnull()].sum()  
    result['总实际收入金额'] = data['买家实际支付金额'][data['订单付款时间'].notnull()].sum()
    return (result,)


@app.cell
def _(result):
    result
    return


@app.cell
def _(result):
    from pyecharts import options as opts
    from pyecharts.charts import Map, Bar, Line
    from pyecharts.components import Table
    from pyecharts.options import ComponentTitleOpts
    from pyecharts.faker import Faker

    table = Table()

    headers = ['总订单数', '总订单金额', '已完成订单数', '总实际收入金额', '退款订单数', '总退款金额', '成交率', '退货率']
    rows = [
        [
            result['总订单数'], f"{result['总订单金额']/10000:.2f} 万", result['已完成订单数'], f"{result['总实际收入金额']/10000:.2f} 万",
            result['退款订单数'], f"{result['总退款金额']/10000:.2f} 万", 
            f"{result['已完成订单数']/result['总订单数']:.2%}",
            f"{result['退款订单数']/result['已完成订单数']:.2%}",
        ]
    ]
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title='整体情况')
    )
    table.render_notebook()
    return (
        Bar,
        ComponentTitleOpts,
        Faker,
        Line,
        Map,
        Table,
        headers,
        opts,
        rows,
        table,
    )


@app.cell
def _(mo):
    mo.md(r"""#### 2.2 地区分析""")
    return


@app.cell
def _(Map, data, opts):
    result2 = data[data['订单付款时间'].notnull()].groupby('收货地址').agg({'订单编号': 'count'})
    result21 = result2.to_dict()['订单编号']
    c = Map().add('订单量', [*result21.items()], 'china', is_map_symbol_show=False).set_series_opts(label_opts=opts.LabelOpts(is_show=True)).set_global_opts(title_opts=opts.TitleOpts(title='地区分布'), visualmap_opts=opts.VisualMapOpts(max_=1000))
    c
    return c, result2, result21


@app.cell
def _(mo):
    mo.md(r"""#### 2.3 时间分析""")
    return


@app.cell
def _(data, pd):
    data['订单创建时间'] = pd.to_datetime(data['订单创建时间'])
    data['订单付款时间'] = pd.to_datetime(data['订单付款时间'])
    return


@app.cell
def _(Line, data, opts):
    result31 = data.groupby(data['订单创建时间'].apply(lambda x: x.strftime("%Y-%m-%d"))).agg({'订单编号':'count'}).to_dict()['订单编号']
    c2 = (
        Line()
        .add_xaxis(list(result31.keys()))
        .add_yaxis("订单量", list(result31.values()))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ]
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="每日订单量走势"))
    )
    c2
    return c2, result31


@app.cell
def _(mo):
    mo.md(r"""从上图来看，2月份上半月由于受新冠疫情影响，订单量比较少，随着复工开展，下半月的订单量增长明显。""")
    return


@app.cell
def _(Bar, data, opts):
    result32 = data.groupby(data['订单创建时间'].apply(lambda x: x.strftime("%H"))).agg({'订单编号':'count'}).to_dict()['订单编号']
    x = [*result32.keys()]
    y = [*result32.values()]
    c3 = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("订单量", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="每小时订单量走势"))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="峰值"),
                    opts.MarkPointItem(name="第二峰值", coord=[x[15], y[15]], value=y[15]),
                    opts.MarkPointItem(name="第三峰值", coord=[x[10], y[10]], value=y[10]),
                ]
            ),
        )
    )
    c3
    return c3, result32, x, y


@app.cell
def _(mo):
    mo.md(r"""从每小时订单量走势来看，一天中有3个高峰期（10点、15点、21点），其中21点-22点之间是一天中订单量最多的时候，。对于卖家的指导意义就是，为了提高订单量，高峰期时应该尽量保证客服的回复速度，尤其是晚上21点-22点之间，所以很多做电商的基本都有夜班。""")
    return


@app.cell
def _(data):
    s = data['订单付款时间'] - data['订单创建时间']
    s[s.notnull()].apply(lambda x: x.seconds / 60 ).mean()  # 从下单到付款的平均耗时为 7.7 分钟
    return (s,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## part2

        这个数据集是美妆店铺的双十一销售数据，纬度有日期、店铺，指标则有销售量、销售额、评论数等。
        ### 1、数据基础情况与处理
        """
    )
    return


@app.cell
def _(pd):
    # import pandas as pd
    data2 = pd.read_csv('双十一淘宝美妆数据.csv')
    data2.head()
    return (data2,)


@app.cell
def _(data2):
    data2.info()  # 数据集情况 28010 条，6个字段
    return


@app.cell
def _(data2):
    data2[data2.duplicated()].count() # 有86条完全重复数据 
    return


@app.cell
def _(data2):
    data2.drop_duplicates(inplace=True)   # 删除重复数据
    data2.reset_index(drop=True, inplace=True)  # 重建索引
    data2.isnull().sum()  # 查看空值 ，销售数量和评论数有空值
    return


@app.cell
def _(data2, pd):
    data2.fillna(0, inplace=True) # 空值填充
    data2['update_time'] = pd.to_datetime(data2['update_time']).apply(lambda x: x.strftime("%Y-%m-%d")) # 日期格式化，便于统计
    return


@app.cell
def _(data2):
    data2[data2['sale_count']>0].sort_values(by=['sale_count']).head() # 从数据来看，sale_count 是销售量
    return


@app.cell
def _(data2):
    data2['sale_amount'] = data2['price'] * data2['sale_count']  # 增加一列销售额
    data2[data2['sale_count']>0].sort_values(by=['sale_count'])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### 2、数据分析与可视化
        #### 2.1 每日整体销售量走势
        """
    )
    return


@app.cell
def _(Line, data2, opts):
    _result = data2.groupby('update_time').agg({'sale_count':'sum'}).to_dict()['sale_count']
    _c = (
        Line()
        .add_xaxis(list(_result.keys()))
        .add_yaxis("销售量", list(_result.values()))
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="每日整体销售量走势"))
    )
    _c
    return


@app.cell
def _(mo):
    mo.md(r"""#### 2.2 谁家的化妆品卖的最好""")
    return


@app.cell
def _(data2):
    dts = list(data2['update_time'].unique())
    dts.reverse()
    dts
    return (dts,)


@app.cell
def _(Bar, data2, dts, opts):
    # from pyecharts import options as opts
    # from pyecharts.charts import Map, Timeline, Bar, Line, Pie
    # from pyecharts.components import Table
    # from pyecharts.options import ComponentTitleOpts
    from pyecharts.charts import Timeline

    tl = Timeline()
    tl.add_schema(
    #         is_auto_play=True,
            is_loop_play=False,
            play_interval=500,
        )
    for dt in dts:
        item = data2[data2['update_time'] <= dt].groupby('店名').agg({'sale_count': 'sum', 'sale_amount': 'sum'}).sort_values(by='sale_count', ascending=False)[:10].sort_values(by='sale_count').to_dict()
        bar = (
            Bar()
            .add_xaxis([*item['sale_count'].keys()])
            .add_yaxis("销售量", [round(val/10000,2) for val in item['sale_count'].values()], label_opts=opts.LabelOpts(position="right", formatter='{@[1]/} 万'))
            .add_yaxis("销售额", [round(val/10000/10000,2) for val in item['sale_amount'].values()], label_opts=opts.LabelOpts(position="right", formatter='{@[1]/} 亿元'))
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts("累计销售量排行 TOP10")
            )
        )
        tl.add(bar, dt)
    tl
    return Timeline, bar, dt, item, tl


@app.cell
def _(data2, opts):
    from pyecharts.charts import Pie
    item1 = data2.groupby('店名').agg({'sale_count': 'sum'}).sort_values(by='sale_count', ascending=False)[:10].to_dict()['sale_count']
    item2 = {k: round(v/10000, 2) for k, v in item1.items()}
    _c = (
        Pie()
        .add("销量", [*item2.items()])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} 万({d}%)"))
    )
    _c
    return Pie, item1, item2


@app.cell
def _(mo):
    mo.md(r"""#### 2.4 谁家的化妆品最贵""")
    return


@app.cell
def _(Bar, data2, opts):
    item3 = data2.groupby('店名').agg({'price': 'mean'}).sort_values(by='price', ascending=False)[:20].sort_values(by='price').to_dict()
    _c = (
        Bar()
        .add_xaxis([*item3['price'].keys()])
        .add_yaxis("销售量", [round(v, 2) for v in item3['price'].values()], label_opts=opts.LabelOpts(position="right"))
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts("平均价格排行 TOP20")
        )
    )
    _c
    return (item3,)


if __name__ == "__main__":
    app.run()
