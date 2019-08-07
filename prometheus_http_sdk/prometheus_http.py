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
                result=[PrometheusApiDataResult(query=self.query, start=self.start, end=self.end, step=self.step,
                                                values=i["values"]) for i in response["data"]['result']]
            )
        else:
            raise PrometheusApiException(response["errorType"], response["error"])

    def query_all(self, query, step=15):
        '''
        :param query: query
        :param step: default 15s
        :return:
        '''
        self.query = query
        self.step = step
        self.end = time.time()
        self.start = self.end - (11000 * 15)
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
                        [PrometheusApiDataResult(query=self.query, start=self.start, end=self.end, step=self.step,
                                                 values=i["values"]) for i in response["data"]['result']])
                    self.end = self.start
                    self.start = self.end - (11000 * 15)
                else:
                    break
            else:
                raise PrometheusApiException(response["errorType"], response["error"])
        return PrometheusApiData(
            resultType=response["data"].get("resultType"),
            result=result
        )

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
        query=":node_cpu_saturation_load1:",
        range_time="6h",
    )
    print(data)
    data = PrometheusApi("http://prometheus.ps.appeasou.com").query_all(
        query=":node_cpu_saturation_load1:",
    )
    print(data)
