#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@auther = 'Redheat'
@create = '2019/8/5 11:25'
@email = 'qjyyn@qq.com'
'''
import requests
import json
import time
import math
from urllib.parse import urljoin
from prometheus_http_sdk.prometheus_data_struct import PrometheusApiData, PrometheusApiDataResult
from prometheus_http_sdk.prometheus_exception import PrometheusApiException


class PrometheusApi(object):
    '''
    Prometheus http Api
    '''

    def __init__(self, url):
        '''

        :param url: promethues http address
        '''
        self.url = urljoin(url, "api/v1/")
        self.query = None
        self.range_time = None
        self.start = None
        self.end = None
        self.step = None

    def query_range(self, **kwargs):
        '''
        :param kwargs:  query 查询语句 type:str
                        range_time 查询时间范围 type: m 分 h 时 d 天 w 周 y 年
                        start 查询时间开始 type: unix_timestamp
                        end 查询时间结束 type: unix_timestamp
                        step 步长 type: unix_timestamp
        :return:
        '''
        self.query = kwargs.get("query")
        self.range_time = kwargs.get("range_time")
        if self.range_time:
            self.start = time.time() - self._range_time_stamp(self.range_time)
            self.end = time.time()
        else:
            self.start = kwargs.get("start")
            self.end = kwargs.get("end") or time.time()
        self.step = kwargs.get("step") or self._step(self.start, self.end)
        response = requests.post(
            url=urljoin(self.url, "query_range"),
            data={
                "query": self.query,
                "start": self.start,
                "end": self.end,
                "step": self.step
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response = json.loads(str(response.content, "utf-8"))
        if response["status"] == "success":
            return PrometheusApiData(
                resultType=response["data"].get("resultType"),
                result=[PrometheusApiDataResult(query=i["metric"]["__name__"], start=self.start, end=self.end,
                                                step=self.step,
                                                values=i["values"]) for i in response["data"]['result']]
            )
        else:
            raise PrometheusApiException(response["errorType"], response["error"])

    def query_all(self, query, step=15, end=None):
        '''
        :param query: query
        :param step: default 15s
        :param end: end time, default is now
        :return:
        '''
        self.query = query
        self.step = step
        if end is None:
            self.end = time.time()
        else:
            self.end = end
        self.start = self.end - (11000 * self.step)
        result = []
        while True:
            response = requests.post(
                url=urljoin(self.url, "query_range"),
                data={
                    "query": self.query,
                    "start": self.start,
                    "end": self.end,
                    "step": self.step
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response = json.loads(str(response.content, "utf-8"))
            if response["status"] == "success":
                if response["data"]['result']:
                    result.extend(
                        [PrometheusApiDataResult(query=i["metric"]["__name__"], start=self.start, end=self.end,
                                                 step=self.step, values=i["values"]) for i in
                         response["data"]['result']])
                    self.end = self.start
                    self.start = self.end - (11000 * self.step)
                else:
                    break
            else:
                raise PrometheusApiException(response["errorType"], response["error"])
        return PrometheusApiData(
            resultType=response["data"].get("resultType"),
            result=result
        )

    def merage(self, data):
        d = {}
        for i in data.result:
            for j in i.values:
                if j[0] in d:
                    d[j[0]].update({i.query: j[1]})
                else:
                    d[j[0]] = {i.query: j[1]}
        a = []
        for k, v in d.items():
            x = {"time": k}
            x.update(v)
            a.append(x)
        return a

    @staticmethod
    def _range_time_stamp(range_time):
        '''
        :param range_time: range time
            m minute
            h hour
            d day
            w week
            y year
        :return: unix_timestamp
        '''
        if range_time.endswith("m"):
            return float(range_time.replace("m", "")) * 60
        if range_time.endswith("h"):
            return float(range_time.replace("h", "")) * 60 * 60
        if range_time.endswith("d"):
            return float(range_time.replace("d", "")) * 60 * 60 * 24
        if range_time.endswith("w"):
            return float(range_time.replace("w", "")) * 60 * 60 * 24 * 7
        if range_time.endswith("y"):
            return float(range_time.replace("y", "")) * 60 * 60 * 24 * 365

    @staticmethod
    def _step(start, end):
        '''
        results points can not max than 11,000
        :param start: start time
        :param end: end time
        :return: step
        '''
        return math.ceil((end - start) / 11000)


if __name__ == "__main__":
    data = PrometheusApi("http://prometheus").query_range(
        query='{__name__=~":node_cpu_saturation_load1:"}',
        range_time="1m",
        step=15
    )
    print(data.convertDict(tfType=True))
    data = PrometheusApi("http://prometheus").query_all(
        query='{__name__=~":node_cpu_saturation_load1:|:node_memory_utilisation:"}',
        step=60,
        end=time.time()-600
    )
    print(data.convertDict())
