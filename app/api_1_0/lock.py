#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
锁API类
'''

from flask import make_response, request, current_app, url_for
from flask import g
from .authentication import auth
from . import api
from .decorators import permission_required
from ..models import Lock
from ..core.common import jsonify
from ..core import common
import logging
import json

@api.route('/lock/update', methods=['GET'])
#@auth.login_required
def lock_update():
    '''
    lock定时访问 心跳包

    URL:/lock/update
    GET 参数:
        pid -- 停车场ID
        gid -- 车锁网关ID
        did -- 车锁ID
        type --上报状态或向下发送命令
        action -- 开启或者关闭 锁
    '''
    #data = request.get_json()
    pid = request.args.get('pid',0)
    gid = request.args.get('gid',0)
    did = request.args.get('did',0)
    action = request.args.get('action',0)
    if len(pid)>0 and len(gid)>0 and len(did)>0:
        Lock.update(pid,gid,did,action)
        return jsonify(ret=1)
    else:
        return jsonify(ret=-1)#系统异常

