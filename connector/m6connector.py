#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append("..")

import time
import uuid

from connector.client import Client
from protocol.submission import Submission
from connector.proxy import Proxy
import start.config as config

class M6Connector(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(M6Connector, cls).__new__(
                    cls, *args, **kwargs
                    )
        return cls._instance

    is_online = False

    def online(self):
        config.logger.info("尝试上线。。。。")
        try:
            proxy = Proxy()
            response = proxy.online()
            self.is_online = True
            config.logger.info("上线成功，节点ID：%s" % response['siteId'])
        except (), msg:
            config.logger.error("上线失败，错误信息：%s" % msg)

    def on_load(self):
        client = Client()
        while True:
            wait = 1
            success = client.connect()
            if success:
                break
            config.logger.warning("连接失败，%s s后重新连接." % wait)
            time.sleep(wait)
        if not self.is_online:
            self.online()
            config.logger.info("M6Connector 已经上线成功.")

    def get_submission(self):
        response = None
        is_valid = False
        while not response or not is_valid:
            try:
                proxy = Proxy()
                response = proxy.get_submission()
            except (), e:
                config.logger.error(e)
                self.is_online = False
                self.on_load()
            if response['valid']:
                is_valid = True


        inputDataFile = config.tempPath + '/' + str(uuid.uuid4())
        sourceCodeFile = config.tempPath + '/Main'

        outputDataFile = self.prepare(response, inputDataFile, sourceCodeFile)

        submissionId = response['submissionId']
        timeLimit = response['timeLimit']
        memoryLimit = response['memoryLimit']
        compiler = response['compiler']
        validator = response['validator']
        saveOutput = response['keepOutput']

        submission = Submission(submissionId, compiler, validator, sourceCodeFile, config.tempPath,
                inputDataFile, outputDataFile, timeLimit, memoryLimit, saveOutput
            )
        return submission


    def prepare(self, response, inputDataFile, sourceCodeFile):
        return config.tempPath + '/1'
        pass

    def send_result(self):
        pass

    def update_state(self):
        pass

