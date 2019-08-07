#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@auther = 'Redheat'
@create = '2019/8/5 17:57'
@email = 'qjyyn@qq.com'
'''
import json


class PrometheusApiDataBase(object):
    '''
    Prometheus Api Data Base class
    '''

    def coverDict(self):
        '''
        cover to dict
        :return: pass
        '''
        pass

    def coverJson(self):
        '''
        cover to json
        :return: json
        '''
        return json.dumps(self.coverDict())


class PrometheusApiData(PrometheusApiDataBase):
    '''
    Prometheus Api Data structure
    '''

    def __init__(self, resultType, result=[]):
        '''

        :param resultType: resultType
        :param result: result, type list
        '''
        self.resultType = resultType
        self.result = result

    def coverDict(self):
        self.result = [i.coverDict() for i in self.result]  # cover to dict
        return {
            "resultType": self.resultType,
            "result": self.result
        }

    def __len__(self):
        return len(self.result)


class PrometheusApiDataResult(PrometheusApiDataBase):
    '''
    Prometheus Api Result data structure
    '''

    def __init__(self, query, start, end, step, values):
        '''

        :param query: query
        :param start: start time
        :param end:  end time
        :param step: step for result
        :param values: return values
        '''
        self.query = query
        self.start = start
        self.end = end
        self.step = step
        self.values = values

    def coverDict(self):
        return {
            "query": self.query,
            "start": self.start,
            "end": self.end,
            "step": self.step,
            "values": self.values
        }
