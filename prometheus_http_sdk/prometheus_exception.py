#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@auther = 'Redheat'
@create = '2019/8/5 17:56'
@email = 'qjyyn@qq.com'
'''


class PrometheusApiException(Exception):
    '''
    Prometheus Api Exception class
    '''

    def __init__(self, ex_type, message):
        '''

        :param ex_type: exception type
        :param message: exception message
        '''
        super().__init__(self)
        self.ex_type = ex_type
        self.message = message

    def __str__(self):
        '''
        exception message
        :return: str
        '''
        return "{}:{}".format(self.ex_type, self.message)