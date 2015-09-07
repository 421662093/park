#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, flash
from flask import g
from .authentication import auth
from werkzeug import secure_filename
from flask.ext.login import login_required, current_user, logout_user
from . import admin
from .decorators import permission_required
from .forms import EditUserForm,EditTopicForm,EditInventoryForm,EditRoleForm,EditAdForm
from ..models import collection,Lock
from .. import conf#searchwhoosh,rs
from ..core import common
import logging
import time

@admin.route('/logout')
@auth.login_required
def logout():
    logout_user()
    return jsonify(msg='用户已登出')


@admin.route('/locklist',methods=['GET', 'POST'])
#@admin.route('/topiclist/<string:uid>', methods=['GET', 'POST'])
@admin.route('/locklist/<string:pid>/<string:gid>/<int:index>', methods=['GET', 'POST'])
#@auth.login_required
def lock_list(pid=0,gid=0,index=1):
    if request.method == 'POST':
        pass
    else:
    	pagesize = 8
    	count = Lock.getcount(pid=pid,gid=gid)
        print str(count)
    	pcount = common.getpagecount(count,pagesize)
    	if index>pcount:
    		index = pcount
    	if index<1:
    		index=1
        '''
        lock = Lock()
        lock.park_id = 1
        lock.gateway_id = 1
        lock.device_id = 1
        lock.state = 1
        lock.saveinfo()
        '''
        locklist = Lock.getlist(index=index,count=pagesize)
        func = {'stamp2time': common.stamp2time,'getlockstate':common.getlockstate,'can': common.can}

        return render_template('admin/lock_list.html',locklist=locklist, func=func,pid=pid,gid=gid,pagecount=pcount,index=index)#,uinfo=g.current_user

@admin.route('/lockedit',methods=['GET', 'POST'])
@admin.route('/lockedit/<int:id>', methods=['GET', 'POST'])
@admin.route('/lockedit/<int:id>/<int:pindex>', methods=['GET', 'POST'])
#@auth.login_required
def lock_edit(id=0,pindex=1):
    if request.method == 'POST':
        lock = Lock()
        lock._id = id
        lock.park_id = request.form.get('park_id',0)
        lock.gateway_id = request.form.get('gateway_id',0)
        lock.device_id = request.form.get('device_id',0)
        lock.saveinfo()
        return redirect(url_for('.lock_list',pid=0,gid=0,index=pindex))
    else:
        islock = False
        lock = None
        if id > 0 :
            lock = Lock.getinfo(id)
            if lock:
                islock = True
        return render_template('admin/lock_edit.html',lock=lock,id=id, islock=islock,pindex=pindex)#,uinfo=g.current_user
