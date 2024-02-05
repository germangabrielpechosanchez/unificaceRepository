# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Gestion des projets"), False, '#', [
        (T('Gestion des projets'), False, URL( f='index'),[]),
        (T('Disponibilité'), False, URL( f='availability'),[]),
        (T('Navigateur'), False, URL( f='navigator'),[]),
        (T('Tâches non-conformes'), False, URL( f='to_verify'),[]),
        (T('Tables'), False, URL( f='tables'),[]),
        (T('Mettre à jour manuelle'), False, URL( f='project_update'),[]),
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


@auth.requires(auth.has_membership(role='admin'))
def index():


    response.menu+=[
        (T('Gestion des projets'), False, URL( f='index'),[]),
        ]
    #db(db.capacity_management.id>0).delete()
    #db(db.resources.id>0).delete()
    grid=""
    form=""
    if not request.vars.date_begin:
        #request.vars.date_begin=str(today)
        date_begin=datetime.datetime(this_year, this_month, this_day, 0, 0)
        ds=date_begin.weekday()+1
        if ds==7:ds=0
        date_begin=date_begin+datetime.timedelta(days=-ds)
        request.vars.date_begin=str(date_begin.date())

    if not request.vars.date_end:request.vars.date_end=str(datetime.datetime.strptime(request.vars.date_begin, '%Y-%m-%d').date()+datetime.timedelta(days=140))
    #datetime.datetime.strptime(str(today), '%Y-%m-%d').date()

    form=FORM(
        TABLE(
            TR(
                #TD(LABEL("VUE DÉTAILLÉE ",INPUT(_type='checkbox',_class='my_label',_name='detail_view',_value=False))),
                TD(LABEL("DÉBUT(vide = début de cette semaine)",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date_begin',_id='date',value=request.vars.date_begin,_size=10,requires=IS_DATE())),
                TD(LABEL("FIN (vide = début+20 semaines)",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date_end',_id='date',value=request.vars.date_end,_size=10,requires=IS_DATE())),
                TD('',INPUT(_class='button_command',_type='submit',_value='par groupes',_id='par_groupes',_name='par_groupes',_style='background-color:#339FFF')),
                TD('',INPUT(_class='button_command',_type='submit',_value='par ressources',_id='par_ressources',_name='par_ressources',_style='background-color:#339FFF')),
            ),
            #TR(''),
            ))
    

    msg=""

    if not db(db.capacity_reports_created.created==today).select():
        msg=weeks_separation()
        db.capacity_reports_created.insert(created=today)
        db.commit()
    
        
    #if form.accepts(request.vars,session):
    if True:

        tb=db.capacity_reports
        date_begin=datetime.datetime.strptime(request.vars.date_begin, '%Y-%m-%d')#.date()
        date_end=datetime.datetime.strptime(request.vars.date_end, '%Y-%m-%d')#.date()
        
        if request.vars.has_key("par_groupes"):
            this_groupby='groups'
            this_search_group=None
            this_search_resource=None
        elif request.vars.has_key("par_ressources"):
            this_groupby='resources'
            this_search_group=request.vars.search_group
            this_search_resource=request.vars.search_resource
            request.vars.search_resource=None
        else:
            if request.vars.search_group:
                this_groupby='resources'
                this_search_group=request.vars.search_group
                request.vars.search_group=None
            elif request.vars.search_resource:
                this_groupby='task_number'
                this_search_resource=request.vars.search_resource
                request.vars.search_resource=None
                this_search_group=None                
            else:
                this_groupby='groups'
                this_search_group=None
                this_search_resource=None
        
        
        rs_list=[]
        this_end=date_begin
        while this_end<=date_end:
            this_begin=this_end
            ds=6-this_begin.weekday()
            #m,t,w,t,f,s,su
            if not ds:ds=7
            this_end=this_begin+datetime.timedelta(days=ds)
            
            #qry=(tb.estimated_begin>=this_begin)&(tb.estimated_end<this_end)&(tb.group_id!=0)&(tb.group_id!=97)&(tb.resources_id!=1342) #for all
            qry=(tb.estimated_begin>=this_begin)&(tb.estimated_end<this_end)&(tb.group_id!=0)&(tb.group_id!=97)&(tb.resources_id!=1342)
            if this_search_group:
                qry=qry&(tb.groups==this_search_group)
            elif this_search_resource:
                qry=qry&(tb.resources==this_search_resource)
                              
            sum_available = tb.available_time.sum()
            sum_effort = tb.estimated_effort.sum()
            sum_effort2 = tb.estimated_effort2.sum()
            sum_no_effort = tb.estimated_no_effort.sum()
            rs=db(qry).select(tb[this_groupby],sum_available,sum_effort,sum_effort2,sum_no_effort,groupby=tb[this_groupby])
            rs_list+=[(this_begin,list(rs)),]
        my_i=""

        grid='<body class="web2py_htmltable" style="width:100%;overflow-x:auto;-ms-overflow-x:scroll"><table>'

        if this_groupby=='task_number':
            grid+="<tr class='big_head'><td>Semain du:</td><td>Heures totals</td><td>Heures planifiées</td><td>Tâches sans effort</td></tr>"            
        else:
            grid+="<tr class='big_head'><td>Semain du:</td><td>Heures totals</td><td>Pourcentage utilisé</td><td>Heures disponibles</td><td>Tâches sans effort</td></tr>"
        for i in rs_list:
            if len(i[1]):
                week_begin=str(i[0].date())
                grid+="<tr><th>"+week_begin+"</th><th></th><th></th><th></th><th></th></tr>"
                #rows rs
                my_i=i[1]
                for j in i[1]:
                    this_sum_available=j[sum_available]
                    this_sum_effort=j[sum_effort]
                    this_sum_no_effort=j[sum_no_effort]
                    #this_groups=j.capacity_reports.groups
                    
                    this_groups=j['capacity_reports'][this_groupby]
                    #create these links
                    if this_groupby=='groups':
                        this_groups='<a href="./index/?search_group='+this_groups+'">'+this_groups+'</a>' 
                    elif this_groupby=='resources':
                        this_groups='<a href="./index/?search_resource='+this_groups+'">'+this_groups+'</a>'                        
                    if this_sum_available>0:percents=int(float(this_sum_effort)/float(this_sum_available)*100)
                    else:
                        percents=100000
                        this_sum_available=0
                    if this_sum_available:
                        this_sum_total="{:5.2f}".format(this_sum_available/60.)
                    else:
                        this_sum_total=""

                    this_sum_available=(this_sum_available-this_sum_effort)/60.
                    if this_sum_available<0:
                        red_class="class='red_class'"
                    else:
                        red_class=""

                    if this_sum_available:
                        this_sum_available="{:5.2f}".format(this_sum_available)
                    else:
                        this_sum_available=""
                    if this_sum_effort:
                        this_sum_effort="{:5.2f}".format(this_sum_effort/60.)
                    else:
                        this_sum_effort=""
                    if this_sum_no_effort:
                        this_sum_no_effort="{:5d}".format(this_sum_no_effort)
                    else:
                        this_sum_no_effort=""
                    if percents==100000:
                        percents='<div></div>'
                    else:
                        percents=str(percents)
                        #percents='<div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="'+percents+'"aria-valuemin="0" aria-valuemax="100" style="width:'+percents+'%">'+percents+'%</div></div>'
                        percents='<div class="progress"><div class="progress-bar progress-bar-animated" role="progressbar" aria-valuenow="'+percents+'"aria-valuemin="0" aria-valuemax="100" style="width:'+percents+'%;"><div align="left" style="margin-left: 20px;">'+percents+'%</div></div></div>'

                    #grid+="<tr><td>"+this_groups+"</td><td>"+this_sum_available+"</td><td>"+this_sum_effort+"</td><td>"+percents+"</td><td>"+this_sum_no_effort+"</td></tr>"
                    if this_groupby=='task_number':
                        if this_groups=="":
                             this_groups='<i>'+this_search_resource+'</i>'                       
                        grid+="<tr><td>"+this_groups+"</td><td>"+this_sum_total+"</td><td>"+this_sum_effort+"</td><td>"+this_sum_no_effort+"</td></tr>"
                    else:
                        grid+="<tr><td>"+this_groups+"</td><td>"+this_sum_total+"</td><td>"+percents+"</td><td "+red_class+">"+this_sum_available+"</td><td>"+this_sum_no_effort+"</td></tr>"

        grid+="</table></body>"

    response.flash = msg
    return dict(form=form,grid=grid)

#tranformation for rapport
def weeks_separation():
    tb=db.capacity_management
    tb2=db.capacity_reports
    #db(tb2.id>0).delete() already deleted in python import script
    redo=True
    separated_list_sum=()
    errors=()
    while redo:
        #date_begin=datetime.datetime(2015, 1, 1, 0, 0)
        date_begin=datetime.datetime(2016, 1, 1, 0, 0)
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
            #qry=(tb.estimated_begin>=this_begin)&(tb.estimated_begin<this_end)&(tb.estimated_end>=this_end)&(tb.id.belongs==(separated_list))
            rs=db(qry).select(tb.ALL)
            
            if rs:
                separated_list+=(rs[0].id,)
                #db(tb.id==rs[0].id).update(separated=True)
                for r in rs:
                    wds=working_days(r.estimated_begin,r.estimated_end)
                    #estimated_effort=float(r.estimated_effort)/float(wds)
                    try:
                        estimated_effort=float(r.estimated_effort)/float(wds)
                    except:
                        estimated_effort=float(r.estimated_effort)
                        #test to see what record do error
                        errors+=(r.task_number,)

                    #r_end=this_begin
                    r_end=r.estimated_begin
                    while r_end<=r.estimated_end:
                        r_begin=r_end
                        ds=6-r_begin.weekday()
                        if not ds:ds=7

                        b=r_begin.date()
                        #r_end=r_begin+datetime.timedelta(days=ds) #problem with
                        r_end=datetime.datetime(b.year,b.month,b.day)+datetime.timedelta(days=ds)
                        if r_end<r.estimated_end:rec_end=r_end-datetime.timedelta(seconds=1)
                        else:rec_end=r.estimated_end

                        wd=working_days(r_begin,rec_end)
                        r_estimated_effort=int(estimated_effort*wd)

                        available_time=0
                        if r_estimated_effort:estimated_no_effort=0
                        else:estimated_no_effort=1

                        if r.project==0:
                            estimated_effort=0
                            estimated_effort2=r_estimated_effort
                        else:
                            estimated_effort=r_estimated_effort
                            estimated_effort2=0

                        qry=(tb2.resources_id==r.resources_id)&\
                            (tb2.resources==r.resources)&\
                            (tb2.group_id==r.group_id)&\
                            (tb2.groups==r.groups)&\
                            (tb2.task_id==r.task_id)&\
                            (tb2.task_number==r.task_number)&\
                            (tb2.estimated_begin==r_begin)&\
                            (tb2.estimated_end==rec_end)&\
                            (tb2.estimated_effort==estimated_effort)&\
                            (tb2.estimated_effort2==estimated_effort2)&\
                            (tb2.estimated_no_effort==estimated_no_effort)&\
                            (tb2.available_time==available_time)&\
                            (tb2.status_id==r.status_id)&\
                            (tb2.status==r.status)

                        if not(db(qry).select(tb2.id)):#problem here
                            tb2.insert(
                                resources_id=r.resources_id,
                                resources=r.resources,
                                group_id=r.group_id,
                                groups=r.groups,
                                task_id=r.task_id,
                                task_number=r.task_number,
                                estimated_begin=r_begin,
                                estimated_end=rec_end,
                                estimated_effort=estimated_effort,
                                estimated_effort2=estimated_effort2,
                                estimated_no_effort=estimated_no_effort,
                                available_time=available_time,
                                status_id=r.status_id,
                                status=r.status,
                            )
                            
        if len(separated_list)>0:
            separated_list_sum+=separated_list
            db(tb.id.belongs(separated_list)).update(separated=True)
            #db.commit() #db.commit()
            redo=True
        else:
            redo=False
            #insert all ~
            rs=db(~tb.id.belongs(separated_list_sum)).select(tb.ALL)
            for r in rs:
                available_time=0
                if r.estimated_effort:estimated_no_effort=0
                else:estimated_no_effort=1
                #isolate project from another
                if r.project==0:
                    estimated_effort=0
                    estimated_effort2=r.estimated_effort
                else:
                    estimated_effort=r.estimated_effort
                    estimated_effort2=0

                tb2.insert(
                            resources_id=r.resources_id,
                            resources=r.resources,
                            group_id=r.group_id,
                            groups=r.groups,
                            task_id=r.task_id,
                            task_number=r.task_number,
                            estimated_begin=r.estimated_begin,
                            estimated_end=r.estimated_end,
                            estimated_effort=estimated_effort,
                            estimated_effort2=estimated_effort2,
                            estimated_no_effort=estimated_no_effort,
                            available_time=available_time,
                            status_id=r.status_id,
                            status=r.status
                )

    #insert available_time for all ressources by week
    #date_begin=datetime.datetime(this_year, this_month, this_day, 0, 0)
    date_begin=datetime.datetime(2016, 1, 1, 0, 0)    
    ds=date_begin.weekday()+1
    if ds==7:ds=0
    date_begin=date_begin+datetime.timedelta(days=-ds)#bengining of week-sunday
    max=tb.estimated_end.max()
    date_end=db().select(max).first()[max]
    active_resources=db((db.resources.is_active==True)).select(db.resources.id,db.resources.title,db.resources.resources_id)
    for r in active_resources:
        active_groupe=db((db.resource_group.resources_id==r.resources_id)&(db.resource_group.groups_id==db.groups.groups_id)).select(db.resource_group.groups_id,db.groups.title)
        #"""
        if active_groupe:
            r_groups_id=active_groupe[0].resource_group.groups_id
            r_groups_title=active_groupe[0].groups.title
        else:
            r_groups_id=0
            r_groups_title="Sans groupe"
        this_end=date_begin+datetime.timedelta(seconds=-1)
        while this_end<=date_end:
            this_begin=this_end+datetime.timedelta(seconds=1)
            this_end=this_begin+datetime.timedelta(seconds=604799)#7*24*60*60=604800 one week time 604800-1
            qry=(db.capacity_availability.time_begin<= this_begin)&(db.capacity_availability.time_end>=this_end)&(db.capacity_availability.resources==db.resources.id)&(db.resources.resources_id==r.resources_id)
            available_time=db(qry).select(db.capacity_availability.bank)
            if available_time:
                available_time=available_time[0].bank
            else:
                ##### condition for available need remove in record too
                #if r.id in (27,36,31):available_time=600
                #else:available_time=1050
                #available_time=1050 #35*60=2100 good line original
                available_time=2100 #full availablity in one week

            tb2.insert(
                resources_id=r.resources_id,
                resources=r.title,
                group_id=r_groups_id,
                groups=r_groups_title,
                task_id=0,
                task_number='',
                estimated_begin=this_begin,
                estimated_end=this_end,
                estimated_effort=0,
                estimated_effort2=0,
                estimated_no_effort=0,
                available_time=available_time,
                status_id=0,
                status=''
            )
        #"""


               
    #return separated_list_sum
    return str(errors)

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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources'))
def availability():
    response.menu+=[
        (T('Disponibilité'), False, URL( f='availability'),[]),
        ]
    grid = SQLFORM.smartgrid(db.capacity_availability,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(form="",grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources'))
def navigator():
    response.menu+=[
        (T('Navigateur'), False, URL( f='navigator'),[]),
        ]
    grid = SQLFORM.smartgrid(db.capacity_management,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(form="",grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources')|auth.has_membership(role='gestion_ressources_read')|auth.has_membership(role='gestion_ressources_edit')|auth.has_membership(role='gestion_ressources_edit_add'))
def to_verify():
    response.menu+=[
        (T('Tâches non-conformes'), False, URL( f='to_verify'),[]),
        ]
    grid=""
    qry=(db.capacity_management.estimated_begin==datetime.datetime(2000, 1, 1, 0, 0))|(db.capacity_management.estimated_end==datetime.datetime(2000, 1, 1, 0, 0))|\
    (db.capacity_management.estimated_effort<=0)
    grid = SQLFORM.grid(qry,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #response.flash = T(u'Bievenue au module de gestion des inventaires')
    return dict(form="",grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources'))
def project_update():
    import subprocess 
    script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_capacite\read_octopus_projet_affaires.py'
    p1 = subprocess.Popen([r'C:\python27\python.exe',script],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,error = p1.communicate()
    
    redirect(URL('index'))


@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources'))
def tables():
    menu_url=[]
    tables=["resources","groups","resource_group","capacity_availability","capacity_management","capacity_reports","capacity_reports_created"]

    for table in tables:
    #    if '_' not in table: # tables will be in menu
    #        menu_url+=[(T(table), False, URL(c='manage',f='manage',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[table])),]

    response.menu += [(T("Tables"), False, '#', menu_url)]

    table = request.args(0) or 'capacity_management'
    if not table in db.tables(): redirect(URL('error'))

    grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)

    
    return dict(grid=grid)






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


