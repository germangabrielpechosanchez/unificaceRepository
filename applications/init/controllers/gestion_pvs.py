# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
############################################### TEST DB TABLE ###############################################
"""

import datetime
today=datetime.date.today()
now=datetime.datetime.now()

db.define_table('pvs_prod_image',
                Field('title',length=50),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('pvs_dev_image',
                Field('title',length=50),
                Field('description',length=100),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('pvs_admin',
                Field('title',length=50),
                Field('description',length=100),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('pvs_management',
                Field('dev_name',db.pvs_dev_image,requires=IS_IN_DB(db,'pvs_dev_image.id','pvs_dev_image.title')),
                Field('prod_name',db.pvs_prod_image,requires=IS_IN_DB(db,'pvs_prod_image.id','pvs_prod_image.title')),
                Field('time_begin','datetime'),
                Field('time_end','datetime'),
                Field('description',length=1024),
                Field('admin_name',db.pvs_admin,requires=IS_IN_DB(db,'pvs_admin.id','pvs_admin.title')),
                Field('applicant',length=50),
                Field('description',length=2048),
                Field('replace_id','integer'),
                Field('edit_by','integer',requires=IS_IN_SET([auth_id]),default=auth_id),
                Field('edit_time','datetime',default=now),
                )
"""
############################################### TEST DB TABLE ###############################################
response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Gestion des PVS"), False, '#', [
        (T('Gestion des PVS - Les images'), False, URL( f='index'),[]),
        (T('Gestion des PVS - Les changements en cours'), False, URL( f='pvs_current_image'),[]),
        (T('Tables'), False, URL( f='tables'),[]),
        (T('Mettre à jour automatique la liste des images'), False, URL( f='pvs_update'),[]),
        ]),
    
    ]



import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()

if auth.is_logged_in():
    if (auth.has_membership(role='admin')|auth.has_membership(role='gestion_pvs')): #auth.has_membership(role='gestion_pvs_edit_add')
        create=True
        deletable=True
        editable=True
        user_signature=True
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_pvs_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=True
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_pvs_edit')):
        create=False
        deletable=False
        editable=True
        user_signature=True
        searchable=True
        details=True
    else:
        create=False
        deletable=False
        editable=False
        user_signature=False
        searchable=True
        details=False
else:
    create=False
    deletable=False
    editable=False
    user_signature=False
    searchable=True
    details=False

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_pvs')|auth.has_membership(role='gestion_pvs_read')|auth.has_membership(role='gestion_pvs_edit')|auth.has_membership(role='gestion_pvs_edit_add'))
def index():
    response.menu+=[
        (T('Gestion des PVS - Les images'), False, URL( f='index'),[]),
        ]
    grid=""
    qry=(db.pvs_management.id>0)&(db.pvs_management.dev_name==db.pvs_dev_image.id)&(db.pvs_management.prod_name==db.pvs_prod_image.id)
    fields=[db.pvs_management.id,db.pvs_management.dev_name,db.pvs_management.prod_name,db.pvs_management.time_begin,db.pvs_management.time_end,db.pvs_management.description,db.pvs_management.admin_name,db.pvs_management.applicant,db.pvs_management.notes,db.pvs_management.edit_by,db.pvs_management.edit_time]
    grid = SQLFORM.grid(qry,fields=fields,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #grid = SQLFORM.smartgrid(db.pvs_management,maxtextlength=70,\
    #deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #response.flash = T(u'Bievenue au module de gestion des inventaires')
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_pvs')|auth.has_membership(role='gestion_pvs_read')|auth.has_membership(role='gestion_pvs_edit')|auth.has_membership(role='gestion_pvs_edit_add'))
def pvs_current_image():
    response.menu+=[
        (T('Gestion des PVS - Les changements en cours'), False, URL( f='pvs_current_image'),[]),
        ]
    grid=""
    #table = request.args(0) or 'pvs_management'
    #grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,\
    #deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    grid = SQLFORM.grid(db.pvs_management.time_end==None,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #response.flash = T(u'Bievenue au module de gestion des inventaires')
    return dict(grid=grid)
#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_pvs'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_pvs')|auth.has_membership(role='gestion_pvs_edit')|auth.has_membership(role='gestion_pvs_edit_add'))
def tables():
    menu_url=[]
    tables=["pvs_prod_image","pvs_dev_image","pvs_admin","pvs_management"]

    for table in tables:
    #    if '_' not in table: # tables will be in menu
    #        menu_url+=[(T(table), False, URL(c='manage',f='manage',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[table])),]

    response.menu += [(T("Tables"), False, '#', menu_url)]

    table = request.args(0) or 'pvs_prod_image'
    if not table in db.tables(): redirect(URL('error'))

    grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)
    #response.flash = T(u'terminé')
    return dict(grid=grid)




#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_pvs'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_pvs')|auth.has_membership(role='gestion_pvs_edit')|auth.has_membership(role='gestion_pvs_edit_add'))
def pvs_update():
    import os
    grid =""

    files=[r'\\S01VWPR00010.cemtl.rtss.qc.ca\P\Production',r'\\S01VWPR00010.cemtl.rtss.qc.ca\P\Dev']
    tables=[db.pvs_prod_image,db.pvs_dev_image]
    #msg=""
    for i in range(0,2):
        for file in os.listdir(files[i]):
            if file.endswith(".vhdx")|file.endswith(".VHDX"):
                file_lower=file.lower()
                found=db(tables[i].title==file_lower).select()
                if not found:
                    tables[i].insert(title=file_lower)
    #response.flash = msg
    
    response.flash = T(u'terminé')
    


    
    return dict(grid=grid)


###############################################################################################






def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


