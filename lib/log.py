#!/usr/bin/env python
#coding=utf-8


import os
import logging
import time
import traceback


class LOG:
    def __init__(self,logger):
        self.fileHandlerName=''
        self.fileHandler=None
        self.loggerName=logger
        self.logger=logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        self.formatter=logging.Formatter("%(asctime)s - %(levelname)s -  %(message)s")

        #流日志
        sh=logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(self.formatter)
        self.logger.addHandler(sh)


    #文件日志
    def setfh(self):
        fdate=time.strftime("%Y%m%d")
        path=str(os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))) + "/logs/"
        if os.path.isdir(path) == False:
            os.makedirs(path)
        fh=logging.FileHandler(path+self.loggerName+"_"+fdate+".log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        self.fileHandlerName=fdate
        self.fileHandler=fh


    #处理msg
    def _fmtMsg(self,msg):
        if len(msg) >0:
            _tmp=[msg[0]]
            if len(traceback.format_exc()) >0 and traceback.format_exc().strip() != "None":
                _tmp.append(traceback.format_exc())
                return '\n'.join(_tmp)
            else:
                return '\n'.join(_tmp)

        else:
            if len(traceback.format_exc()) > 0 and traceback.format_exc().strip() != "None":
                msg=traceback.format_exc()
                return msg


    def info(self,*msg):
        _info=self._fmtMsg(msg)
        try:
            self.setfh()
            self.logger.info(_info)
        except:
            print ('log info:' + _info)

    def warning(self,*msg):
        _info=self._fmtMsg(msg)
        try:
            self.setfh()
            self.logger.warning(_info)
        except:
            print ('log warning:' + _info)


    def error(self,*msg):
        _info=self._fmtMsg(msg)
        try:
            self.setfh()
            self.logger.error(_info)
        except:
            print ('log error:' + _info)



