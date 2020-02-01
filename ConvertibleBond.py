# https://www.jisilu.cn/data/calendar/get_calendar_data/?qtype=CNV&start=1546185600&end=1549814400
import requests
import datetime, time
import json
import matplotlib.pyplot as plt

# 输入两个时间
# 开始时间
begin='2019-01-01'
end='2020-01-01'
format='%Y-%m-%d'

lr=[]
dataList=[]

beginT=datetime.datetime.strptime(begin,format)
endT=datetime.datetime.strptime(end,format)

while beginT<endT:
    url_1="https://www.jisilu.cn/data/calendar/get_calendar_data/?qtype=CNV&start="+str(int(time.mktime(beginT.timetuple())))+"&end="+str(int(time.mktime((beginT+datetime.timedelta(days=1)).timetuple())))
    for item in requests.get(url_1).json():
        if '上市日' in item['title'] and item['start']==beginT.strftime(format):
            dataList.append(item['start'])
            print(item)
            # {'id': 'CNV5954', 'code': '128051', 'title': '【上市日】光华转债', 'start': '2019-01-09', 'description': '转债代码:128051<br>', 'url': '/data/convert_bond_detail/128051', 'color': '#FFE66F'}
            # begin = int(time.mktime(beginT.timetuple()) * 1000)
            reqUrl = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ" + item['code'] + "&begin=" + str(
                int(time.mktime(beginT.timetuple()) * 1000)) + "&period=day&type=before&count=-1&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"
            # print("\t" + reqUrl)
            header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                      "Accept-Encoding": "gzip,deflate,br", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
                      "Cache-Control": "max-age=0", "Connection": "keep-alive", "Host": "stock.xueqiu.com",
                      "Upgrade-Insecure-Requests": "1",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
            header[
                'Cookie'] = "xq_a_token=e50af02165b86c42cf428646aec7411e6404439f; xq_r_token=ee241f41de25b44579f4409da423f8e0e114e005; Hm_lvt_1db88642e346389874251b5a1eded6e3=1580282027,1580452251,1580526636; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1580526654; u=951580526654433; cookiesu=951580526654433; device_id=24700f9f1986800ab4fcc880530dd0ed"
            detail = requests.get(reqUrl, headers=header)
            if json.loads(detail.text)['data']=={}:
                reqUrl = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH" + item[
                    'code'] + "&begin=" + str( int(time.mktime( beginT.timetuple()) * 1000)) + "&period=day&type=before&count=-1&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"
                detail = requests.get(reqUrl, headers=header)
            price=json.loads(detail.text)['data']['item'][0][5]
            print("\t" + str(price))
            # https: // stock.xueqiu.com / v5 / stock / chart / kline.json?symbol = SZ128051 & begin = 1546963200000 & period = day & type = before & count = -1 & indicator = kline, pe, pb, ps, pcf, market_capital, agt, ggt, balance
            if len(lr)==0:
                lr.append((price-100)*10)
            else:
                lr.append(lr[-1]+(price-100)*10)

    beginT+=datetime.timedelta(days=1)
plt.plot(dataList,lr)
plt.show()