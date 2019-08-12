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

    def convertDict(self):
        '''
        convert to dict
        :return: pass
        '''
        pass

    def convertJson(self):
        '''
        convert to json
        :return: json
        '''
        return json.dumps(self.convertDict())


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

    def convertDict(self, tfType=False):
        '''convert to tensorflow useful type
        :param tfType: be sure to convert
        :return:
        '''
        self.result = [i.convertDict() for i in self.result]  # convert to dict
        if tfType:
            points = {}
            for i in self.result:
                for j in i["values"]:
                    if j[0] in points:
                        points[j[0]].update({i["query"]: j[1]})
                    else:
                        points[j[0]] = {i["query"]: j[1]}
            point_list = []
            for k, v in points.items():
                point = {"time": k}
                point.update(v)
                point_list.append(point)
            points_data = {"start": self.result[0]["start"], "end": self.result[0]["end"],
                           "step": self.result[0]["step"], "values": point_list}
            self.result = points_data
        return {
            "resultType": self.resultType,
            "result": self.result
        }

    def convertJson(self, tfType=False):
        return json.dumps(self.convertDict(tfType))

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

    def convertDict(self):
        return {
            "query": self.query,
            "start": self.start,
            "end": self.end,
            "step": self.step,
            "values": self.values
        }
