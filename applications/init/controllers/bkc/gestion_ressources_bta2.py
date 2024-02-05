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

db.define_table('resources',
                Field('resources_id','integer',label=T("ID de Octopus")),
                Field('title',length=50),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )


"""
############################################### TEST DB TABLE ###############################################
response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Gestion des projets"), False, '#', [
        (T('Gestion des projets'), False, URL( f='index'),[]),
        (T('Navigateur'), False, URL( f='navigator'),[]),
        (T('Les taches à vérifier'), False, URL( f='to_verify'),[]),
        (T('Tables'), False, URL( f='tables'),[]),
        #(T('Mettre à jour automatique la liste des images'), False, URL( f='pvs_update'),[]),
        ]),
    
    ]


import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()

if auth.is_logged_in():
    if (auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources')|auth.has_membership(role='gestion_ressources_edit_add')):
        create=True
        deletable=True
        editable=True
        user_signature=True
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_ressources_edit')):
        create=True
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


@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources')|auth.has_membership(role='gestion_ressources_read')|auth.has_membership(role='gestion_ressources_edit')|auth.has_membership(role='gestion_ressources_edit_add'))
def index():
    response.menu+=[
        (T('Gestion des projets'), False, URL( f='index'),[]),
        ]
    #db(db.resources_management.id>0).delete()
    #db(db.resources.id>0).delete()
    grid=""
    form=""
    if not request.vars.date_begin:request.vars.date_begin=str(today)
    if not request.vars.date_end:request.vars.date_end=str(datetime.datetime.strptime(request.vars.date_begin, '%Y-%m-%d').date()+datetime.timedelta(days=140))
    #datetime.datetime.strptime(str(today), '%Y-%m-%d').date()

    form=FORM(
        TABLE(
            TR(
                #TD(LABEL("VUE DÉTAILLÉE ",INPUT(_type='checkbox',_class='my_label',_name='detail_view',_value=False))),
                TD(LABEL("DÉBUT",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date_begin',_id='date',value=request.vars.date_begin,_size=10,requires=IS_DATE())),
                TD(LABEL("FIN (vide = début+20 semaines)",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date_end',_id='date',value=request.vars.date_end,_size=10,requires=IS_DATE())),
                TD('',INPUT(_class='button_command',_type='submit',_value='actualiser',_id='actualiser',_name='actualiser',_style='background-color:#339FFF')),
                TD('',INPUT(_class='button_command',_type='submit',_value='aujourd\'hui',_id='aujourd\'hui',_name='aujourd\'hui',_style='background-color:#339FFF')),
            ),
            #TR(''),
            ))
    #qry=(db.resources_management.estimated_begin!=datetime.datetime(2000, 1, 1, 0, 0))&(db.resources_management.estimated_end!=datetime.datetime(2000, 1, 1, 0, 0))
    #(db.resources_management.status_id!=800003)&(db.resources_management.status_id!=800004)
    #grid = SQLFORM.grid(qry,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    # one time per day
    msg=""
    if True:
        msg=weeks_separation()
        
    if form.accepts(request.vars,session):
        tb=db.resources_management
        date_begin=datetime.datetime.strptime(request.vars.date_begin, '%Y-%m-%d')#.date()
        date_end=datetime.datetime.strptime(request.vars.date_end, '%Y-%m-%d')#.date()
        #qry=(tb.estimated_begin.year()<2017)
        #qry=(tb.estimated_begin>=date_begin)&(tb.estimated_begin<=date_end)
        #dt = datetime.date(2010, 6, 16)
        # wk = dt.isocalendar()[1]
        #.isocalendar() return a 3-tuple with (year, wk num, wk day)
        rs_list=[]
        this_end=date_begin
        while this_end<=date_end:
            this_begin=this_end
            ds=6-this_begin.weekday()
            #m,t,w,t,f,s,su
            if not ds:ds=7
            this_end=this_begin+datetime.timedelta(days=ds)
            qry=(tb.estimated_begin>=this_begin)&(tb.estimated_end<this_end)               
            #grid = SQLFORM.grid(qry,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
            #count = tb.id.count()
            sum = tb.estimated_effort.sum()
            rs=db(qry).select(tb.groups,sum,groupby=tb.groups)
            rs_list+=[(this_begin,list(rs)),]
        my_i=""


        grid='<body class="web2py_htmltable" style="width:100%;overflow-x:auto;-ms-overflow-x:scroll"><table>'
        grid+="<tr><th>Semain du:</th><th>Heures disponible</th><th>Heures planifiées</th><th></th>"
        for i in rs_list:
            if len(i[1]):
                week_begin=str(i[0].date())
                grid+="<tr><th>"+week_begin+"</th><th></th><th></th><th></th>"
                #rows rs
                my_i=i[1]
                for j in i[1]:
                    this_sum=str(j[sum])
                    this_groups=j.resources_management.groups
                    grid+="<tr><td>"+this_groups+"</td><td>70</td><td>"+this_sum+"</td><td>--------------</td>"

        grid+="</table></body>"


        #response.flash = str(my_i)
    response.flash = str(msg)
    return dict(form=form,grid=grid)

def weeks_separation():
    tb=db.resources_management
    tb2=db.resources_report
    db(tb2.id>0).delete()
    date_begin=datetime.datetime(2015, 1, 1, 0, 0)
    max=tb.estimated_end.max()
    date_end=db().select(max).first()[max]
    this_end=date_begin
    separated_list=()
    while this_end<=date_end:
        this_begin=this_end
        ds=6-this_begin.weekday()
        #m,t,w,t,f,s,su
        if not ds:ds=7
        this_end=this_begin+datetime.timedelta(days=ds)
        qry=(tb.estimated_begin>=this_begin)&(tb.estimated_begin<this_end)&(tb.estimated_end>=this_end)&(tb.separated==False)
        rs=db(qry).select(tb.ALL)
        if rs:
            separated_list+=(rs[0].id,)
            for r in rs:
                wds=working_days(r.estimated_begin,r.estimated_end)
                estimated_effort=float(r.estimated_effort/wds)
                available_time=35
                #r_end=this_begin
                r_end=r.estimated_begin
                while r_end<=r.estimated_end:
                    r_begin=r_end
                    ds=6-r_begin.weekday()
                    if not ds:ds=7
                    r_end=r_begin+datetime.timedelta(days=ds)
                    if r_end<r.estimated_end:rec_end=r_end-datetime.timedelta(seconds=1)
                    else:rec_end=r.estimated_end
                    wd=working_days(r_begin,rec_end)
                    r_estimated_effort=estimated_effort*wd
                    tb2.insert(
                        resources_id=r.resources_id,
                        resources=r.resources,
                        group_id=r.group_id,
                        groups=r.groups,
                        task_id=r.task_id,
                        task_number=r.task_number,
                        estimated_begin=r_begin,
                        estimated_end=rec_end,
                        estimated_effort=r_estimated_effort,
                        available_time=available_time,
                        status_id=r.status_id,
                        status=r.status
                    )
        db(tb.id.belongs(separated_list)).update(separated=True)
    

    return separated_list

def working_days(time_begin,time_end):
    days_begin=time_begin.weekday()
    days_end=time_end.weekday()
    days=(time_end-time_begin).days+1
    j=days_begin
    d=0
    for i in range(days):
        if j<5:d+=1
        if j<6:j+=1
        else:j=0
    return (d)

def navigator():
    response.menu+=[
        (T('Navigateur'), False, URL( f='navigator'),[]),
        ]

    grid=""
    grid = SQLFORM.smartgrid(db.resources_management,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(form="",grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources')|auth.has_membership(role='gestion_ressources_read')|auth.has_membership(role='gestion_ressources_edit')|auth.has_membership(role='gestion_ressources_edit_add'))
def to_verify():
    response.menu+=[
        (T('Les taches à vérifier'), False, URL( f='to_verify'),[]),
        ]
    grid=""
    qry=(db.resources_management.estimated_begin==datetime.datetime(2000, 1, 1, 0, 0))|(db.resources_management.estimated_end==datetime.datetime(2000, 1, 1, 0, 0))|\
    (db.resources_management.estimated_effort<=0)
    grid = SQLFORM.grid(qry,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #response.flash = T(u'Bievenue au module de gestion des inventaires')
    return dict(form="",grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources'))
def tables():
    menu_url=[]
    tables=["resources","groups","resources_banks","resources_management","resources_report"]

    for table in tables:
    #    if '_' not in table: # tables will be in menu
    #        menu_url+=[(T(table), False, URL(c='manage',f='manage',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[table])),]

    response.menu += [(T("Tables"), False, '#', menu_url)]

    table = request.args(0) or 'resources_management'
    if not table in db.tables(): redirect(URL('error'))

    grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)
    #response.flash = T(u'terminé')
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources'))
def resources_update():
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


