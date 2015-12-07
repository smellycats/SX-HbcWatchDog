# -*- coding: utf-8 -*-
import time
import json

import arrow
import requests

class WatchDog(object):

    def __init__(self):
        self.kkdd_dict = {
            '441302': u'惠城区',
            '441303': u'惠阳',
            '441305': u'大亚湾',
            '441322': u'博罗',
            '441323': u'惠东',
            '441324': u'龙门'
        }

        self.date_flag = arrow.now().replace(days=-1).date()
        print self.date_flag
        #早上9时发送信息
        self.send_time = 9
        self.mobiles_list = ['123', '456']
        self.cgs_ini = {
            'host': '127.0.0.1',
            'port': 8080,
            'username': 'test1',
            'password': '123456',
            'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MzI1NjcyMiwiaWF0IjoxNDQzMjQ5NTIyfQ.eyJzY29wZSI6WyJzY29wZV9nZXQiLCJoemhiY19nZXQiXSwidWlkIjoyM30.Qga6zksBXBu8Aq9zVBb7tsR_vQFI4A7IfzdgMvGEfrw'
        }

    def __del__(self):
        pass

    def sms_send(self, content, mobiles):
        """发送短信"""
        return 0

    def get_hbc_count(self, date, kkdd):
        """根据日期，地点获取黄标车数据量"""
        headers = {
            'content-type': 'application/json',
            'access_token': self.cgs_ini['token']
        }
        url = 'http://%s:%s/hbc/count/%s/%s' % (
            self.cgs_ini['host'], self.cgs_ini['port'], date, kkdd)

        # 黄标车数据量
        count_int = 0
        try:
            r = requests.get(url, headers)
            if r.status_code == 200:
                count_int = json.loads(r.text)['count']
        except Exception as e:
            print e
        finally:
            return count_int

    def get_count_dict(self, date):
        """根据日期获取各地区黄标车数据量"""
        self.count_dict = {}
        for i in self.kkdd_dict.keys():
            self.count_dict[self.kkdd_dict[i]] = self.get_hbc_count(date, i)
        return self.count_dict
        
    def run(self):
        print 'run'
        while 1:
            try:
                # 当前时间
                t = arrow.now()
                # 如果当前日期大于记录日期并且当前小时大于额定发送小时
                if t.date() > self.date_flag and t.hour >= self.send_time:
                    count_dict = self.get_count_dict(t.date())
                    self.sms_send('%s: %s' % (str(t.date()), str(count_dict)[1:-1]),
                                  self.mobiles_list)
                    print '[%s]%s' % (str(t), str(count_dict))
                    self.date_flag = t.date()
            except Exception as e:
                print e
            finally:
                time.sleep(1)

if __name__ == "__main__":
    wd = WatchDog()
    wd.run()
    #print wd.hbc_count('2014-02-03')
    del wd
