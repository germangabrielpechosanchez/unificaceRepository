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

#@auth.requires(auth.has_membership(role='admin'))
def index():
    response.menu+=[
        (T('Gestion des projets'), False, URL( f='index'),[]),
        #(T("Par projets"), False, URL( f='index',args=["par_projets",]),[]),
        (T("Par projets"), False, URL( f='report_project',args=["par_projets",]),[]),
        (T("Par groupes"), False, URL( f='index',args=["par_groupes",]),[]),
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
    first_arg=request.args(0) or None

    if first_arg=="par_groupes":
        groups_key='groups'
        groups_btn="par_groupes"
    elif first_arg=="par_projets":
        groups_key='task_parent'
        groups_btn="par_projets"
    else:
        groups_key='groups'
        groups_btn="par_groupes"
        

    form=FORM(
        TABLE(
            TR(
                #TD(LABEL("VUE DÉTAILLÉE ",INPUT(_type='checkbox',_class='my_label',_name='detail_view',_value=False))),
                TD(LABEL("DÉBUT(vide = début de cette semaine)",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date_begin',_id='date',value=request.vars.date_begin,_size=10,requires=IS_DATE())),
                TD(LABEL("FIN (vide = début+20 semaines)",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date_end',_id='date',value=request.vars.date_end,_size=10,requires=IS_DATE())),
                TD('',INPUT(_class='button_command',_type='submit',_value=groups_btn.replace('_',' '),_id=groups_btn,_name=groups_btn,_style='background-color:#339FFF')),
                TD('',INPUT(_class='button_command',_type='submit',_value='par ressources',_id='par_ressources',_name='par_ressources',_style='background-color:#339FFF')),
            ),
            #TR(''),
            ))    
    msg=""

    #if form.accepts(request.vars,session):
    if True:

        tb=db.capacity_report
        date_begin=datetime.datetime.strptime(request.vars.date_begin, '%Y-%m-%d')#.date()
        date_end=datetime.datetime.strptime(request.vars.date_end, '%Y-%m-%d')#.date()
        
        if request.vars.has_key(groups_btn):
            this_groupby=groups_key
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
                this_groupby=groups_key
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
            #qry=(tb.estimated_begin>=this_begin)&(tb.estimated_end<this_end)&(tb.group_id!=0)&(tb.group_id!=97)&(tb.resources_id!=1342) #&(tb.project==1)
            qry=(tb.estimated_begin>=this_begin)&(tb.estimated_end<this_end)&(tb.group_id!=0)&(tb.group_id!=97)&(tb.resources_id!=44488) #&(tb.project==1)

            if this_search_group:
                qry=qry&(tb[groups_key]==this_search_group)
            elif this_search_resource:
                qry=qry&(tb.resources==this_search_resource)
            task_parent = tb.task_parent.max()

            status = tb.status.max()

            sum_available = tb.available_time.sum()
            sum_full = tb.total_time.sum()
            sum_effort = tb.estimated_effort.sum()
            sum_effort2 = tb.estimated_effort2.sum()
            sum_no_effort = tb.estimated_no_effort.sum()
            sum_no_effort2 = tb.estimated_no_effort2.sum()
            #
            sum_available_total = tb.available_time.sum()
            sum_effort_total = tb.estimated_effort.sum()

            #rs=db(qry).select(tb[this_groupby],sum_available,sum_full,sum_effort,sum_effort2,sum_no_effort,sum_no_effort2,groupby=tb[this_groupby])
            #rs=db(qry).select(tb[this_groupby],task_parent,sum_available,sum_full,sum_effort,sum_effort2,sum_no_effort,sum_no_effort2,groupby=tb[this_groupby])
            rs=db(qry).select(tb[this_groupby],task_parent,sum_available,sum_full,sum_effort,sum_effort2,sum_no_effort,sum_no_effort2,status,groupby=tb[this_groupby])
            #
            rs_sum_total=db(qry).select(tb["resources_id"],sum_available_total,sum_effort_total,groupby=tb["resources_id"])
            if rs_sum_total:
                rs_list+=[(this_begin,list(rs),rs_sum_total[0],1,)]
            else:
                rs_list+=[(this_begin,list(rs),0,0,)]

        grid='<body class="web2py_htmltable" style="width:100%;overflow-x:auto;-ms-overflow-x:scroll"><table>'
        if (this_groupby=='task_number')|(this_groupby=='task_parent'):
            #grid+="<tr><td class='head1'>Semain du:</td><td class='head1'>Heures totals</td><td class='head2'>Projet</td><td class='head2'>Heures planifiées</td><td class='head2'>Tâches sans effort</td><td class='head3'>Infra</td><td class='head3'>Heures planifiées</td><td class='head3'>Tâches sans effort</td></tr>"              
            grid+="<tr><td class='head1'>Semain du:</td><td class='head1'>Heures totals</td><td class='head2'></td><td class='head2'>Heures planifiées</td><td class='head2'>Tâches sans effort</td><td class='head3'>Infra</td><td class='head3'>Heures planifiées</td><td class='head3'>Tâches sans effort</td></tr>"              
        else:
            #grid+="<tr><td class='head1'>Semain du:</td><td class='head1'>Heures totals</td><td class='head2'>Projet</td><td class='head2'>Pourcentage utilisé</td><td class='head2'>Heures disponibles</td><td class='head2'>Tâches sans effort</td><td class='head3'>Infra</td><td class='head3'>Pourcentage utilisé</td><td class='head3'>Heures disponibles</td><td class='head3'>Tâches sans effort</td></tr>"
            grid+="<tr><td class='head1'>Semain du:</td><td class='head1'>Heures totals</td><td class='head2'></td><td class='head2'>Pourcentage utilisé</td><td class='head2'>Heures disponibles</td><td class='head2'>Tâches sans effort</td><td class='head3'>Infra</td><td class='head3'>Pourcentage utilisé</td><td class='head3'>Heures disponibles</td><td class='head3'>Tâches sans effort</td></tr>"
        #total=(0,0,0)
        for i in rs_list:
            if len(i[1]):
                #date head
                week_begin=str(i[0].date())
                if (this_groupby=='task_number')|(this_groupby=='task_parent'):
                    grid+="<tr><th class='date_group1'>"+week_begin+"</th><th class='date_group1'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group3'></th><th class='date_group3'></th><th class='date_group3'></th></tr>"
                else:
                    grid+="<tr><th class='date_group1'>"+week_begin+"</th><th class='date_group1'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group3'></th><th class='date_group3'></th><th class='date_group3'></th><th class='date_group3'></th></tr>"
                    
                #rows rs
                for j in i[1]:
                    this_task_parent=j[task_parent]
                    #add vp
                    this_status=j[status]

                    this_sum_available=j[sum_available]
                    this_sum_full=j[sum_full]
                    this_sum_effort=j[sum_effort]#projet affaire
                    this_sum_effort2=j[sum_effort2]#infra
                    this_sum_no_effort=j[sum_no_effort]
                    this_sum_no_effort2=j[sum_no_effort2]
                    
                    this_groups=j['capacity_report'][this_groupby]
                    
                    #create these links
                    
                    if this_groupby==groups_key:
                        #this_groups='<a href="./index/?search_group='+this_groups+'">'+this_groups+'</a>'
                        this_groups='<a href="https://'+request.env.http_host+'/init/gestion_ressources/index/'+groups_btn+'?search_group='+this_groups+'">'+this_groups+'</a>'
                        #this_groups='<a href="https://unificace2.cemtl.rtss.qc.ca/init/gestion_ressources/index/'+groups_btn+'?search_group='+this_groups+'&date_begin='+request.vars.date_begin+'">'+this_groups+'</a>'  
                    elif this_groupby=='resources':
                        #this_groups='<a href="./index/?search_resource='+this_groups+'">'+this_groups+'</a>'
                        this_groups='<a href="https://'+request.env.http_host+'/init/gestion_ressources/index/'+groups_btn+'?search_resource='+this_groups+'">'+this_groups+'</a>'
                        #this_groups='<a href="https://unificace2.cemtl.rtss.qc.ca/init/gestion_ressources/index/'+groups_btn+'?search_resource='+this_groups+'&date_begin='+request.vars.date_begin+'">'+this_groups+'</a>'

                    if this_sum_available:
                        #35h to 28h availablity
                        #not change is in gestion_absence
                        #if (this_groupby=='task_number')|(this_groupby=='resources'):
                        #    this_sum_available=this_sum_available-420
                        #    if this_sum_available<0:this_sum_available=0
                        #
                        this_sum_total="{:5.2f}".format(this_sum_available/60.)
                    else:
                        #this_sum_total="0.00"
                        this_sum_total=""

                    #definition portion de projets
                    #hours2=this_sum_full/2.#infra priority
                    hours2=0#no infra
                    hours=this_sum_available-hours2#for proj
                    #definition available/available2
                    this_sum_available=(hours-this_sum_effort)/60.#infra
                    this_sum_available2=(hours2-this_sum_effort2)/60.#proj

                    #if this_sum_available<0:
                    if this_sum_available<0:
                        #red_class="class='red_class'"
                        red_class="red_class"
                        #
                        this_sum_available=0
                    else:
                        red_class=""
                    #2
                    if this_sum_available2<0:
                        #red_class="class='red_class'"
                        red_class2="red_class"
                    else:
                        red_class2=""  

                    #if this_sum_available>0:
                    if hours:
                        percents=int(float(this_sum_effort)/float(hours)*100)
                    else:
                        percents=100000
                    #2
                    #if this_sum_available2>0:
                    if hours2:
                        percents2=int(float(this_sum_effort2)/float(hours2)*100)
                    else:
                        percents2=100000

                    if this_sum_available:
                        this_sum_available="{:5.2f}".format(this_sum_available)
                    else:
                        this_sum_available="0.00"
                        #this_sum_available=""
                    #2
                    if this_sum_available2:
                        this_sum_available2="{:5.2f}".format(this_sum_available2)
                    else:
                        this_sum_available2=""

                    if this_sum_effort:
                        this_sum_effort="{:5.2f}".format(this_sum_effort/60.)
                    else:
                        this_sum_effort=""
                    #2
                    if this_sum_effort2:
                        this_sum_effort2="{:5.2f}".format(this_sum_effort2/60.)
                    else:
                        this_sum_effort2=""

                    if this_sum_no_effort:
                        this_sum_no_effort="{:5d}".format(this_sum_no_effort)
                    else:
                        this_sum_no_effort=""
                    #2
                    if this_sum_no_effort2:
                        this_sum_no_effort2="{:5d}".format(this_sum_no_effort2)
                    else:
                        this_sum_no_effort2=""

                    if percents==100000:
                        percents_text=''
                    else:
                        percents_text=str(percents)
                    percents=str(percents)
                    percents='<div class="progress"><div class="progress-bar progress-bar-animated" role="progressbar" aria-valuenow="'+percents+'"aria-valuemin="0" aria-valuemax="100" style="width:'+percents+'%;"><div align="left" style="margin-left: 20px;">'+percents_text+'%</div></div></div>'

                    if percents2==100000:
                        percents2_text=''
                    else:
                        percents2_text=str(percents2)
                    percents2=str(percents2)
                    percents2='<div class="progress"><div class="progress-bar progress-bar-animated" role="progressbar" aria-valuenow="'+percents2+'"aria-valuemin="0" aria-valuemax="100" style="width:'+percents2+'%;"><div align="left" style="margin-left: 20px;">'+percents2_text+'%</div></div></div>'

                    if (this_groupby=='task_number')|(this_groupby=='task_parent'):
                        if this_groups=="":
                            this_groups='<i>'+this_search_resource+'</i>'
                            this_sum_total="<b>"+this_sum_total+"</b>"
                            if (this_groupby=='task_number')|i[3]:
                                #total effort by resource 
                                this_sum_effort="{:5.2f}".format(i[2][sum_effort_total]/60.)
                                this_sum_effort="<b>"+this_sum_effort+"</b>"
                                
                        else:
                            #task description detail
                            #this_groups=this_groups+' - '+this_task_parent.split('|')[0]+'' 
                            this_groups=this_groups+' - '+this_status+' - '+this_task_parent.split('|')[0]+''
                        
                        ####                       
                        grid+="<tr><td class='details1'>"+this_groups+"</td><td class='details1'>"+this_sum_total+"</td><td class='details2'></td><td class='details2'>"+this_sum_effort+"</td><td class='details2'>"+this_sum_no_effort+"</td><td class='details3'></td><td class='details3'>"+this_sum_effort2+"</td><td class='details3'>"+this_sum_no_effort2+"</td></tr>"
                    else:
                        grid+="<tr><td class='details1'>"+this_groups+"</td><td class='details1'>"+this_sum_total+"</td><td class='details2'></td><td class='details2'>"+percents+"</td><td class="+"'details2 "+red_class+"'>"+this_sum_available+"</td><td class='details2'>"+this_sum_no_effort+"</td><td class='details3'></td><td class='details3'>"+percents2+"</td><td class='details3 "+red_class2+"'>"+this_sum_available2+"</td><td class='details3'>"+this_sum_no_effort2+"</td></tr>"




        grid+="</table></body>"



    """
    rs=db(db.capacity_report.id>0).select()
    for r in rs:
        groups=r.groups.replace('&','ET')
        db(db.capacity_report.id==r.id).update(groups=groups)
    response.flash = len(rs)#this_groupby
    """
    #response.flash = request.vars.date_begin


    return dict(form=form,grid=grid)

def report_project():
    response.menu+=[
        (T('Gestion des projets'), False, URL( f='index'),[]),
        #(T("Par projets"), False, URL( f='index',args=["par_projets",]),[]),
        (T("Par projets"), False, URL( f='report_project',args=["par_projets",]),[]),
        (T("Par groupes"), False, URL( f='index',args=["par_groupes",]),[]),
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
    first_arg=request.args(0) or None
    #first_arg="par_projets"
    if first_arg=="par_groupes":
        groups_key='groups'
        groups_btn="par_groupes"
    elif first_arg=="par_projets":
        groups_key='task_parent'
        groups_btn="par_projets"
    else:
        groups_key='groups'
        groups_btn="par_groupes"
        

    form=FORM(
        TABLE(
            TR(
                #TD(LABEL("VUE DÉTAILLÉE ",INPUT(_type='checkbox',_class='my_label',_name='detail_view',_value=False))),
                #TD(LABEL("DÉBUT(vide = début de cette semaine)",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date_begin',_id='date',value=request.vars.date_begin,_size=10,requires=IS_DATE())),
                #TD(LABEL("FIN (vide = début+20 semaines)",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date_end',_id='date',value=request.vars.date_end,_size=10,requires=IS_DATE())),
                TD(LABEL(XML(50*"&nbsp"))),
                TD(LABEL(XML(50*"&nbsp"))),
                TD('',INPUT(_class='button_command',_type='submit',_value=groups_btn.replace('_',' '),_id=groups_btn,_name=groups_btn,_style='background-color:#339FFF')),
                TD('',INPUT(_class='button_command',_type='submit',_value='par ressources',_id='par_ressources',_name='par_ressources',_style='background-color:#339FFF')),
            ),
            #TR(''),
            ))    
    msg=""

    #if form.accepts(request.vars,session):
    if True:

        tb=db.capacity_report
        date_begin=datetime.datetime.strptime(request.vars.date_begin, '%Y-%m-%d')#.date()
        date_end=datetime.datetime.strptime(request.vars.date_end, '%Y-%m-%d')#.date()
        
        if request.vars.has_key(groups_btn):
            this_groupby=groups_key
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
                this_groupby=groups_key
                this_search_group=None
                this_search_resource=None
        
        
        rs_list=[]
        #this_end=date_begin
        #while this_end<=date_end:
        if True:
            #this_begin=this_end
            this_begin=datetime.datetime(2015, 1, 1, 0, 0)
            #ds=6-this_begin.weekday()
            #m,t,w,t,f,s,su
            #if not ds:ds=7
            this_end=this_begin+datetime.timedelta(days=3650)
            
            #qry=(tb.estimated_begin>=this_begin)&(tb.estimated_end<this_end)&(tb.group_id!=0)&(tb.group_id!=97)&(tb.resources_id!=1342) #for all
            #qry=(tb.estimated_begin>=this_begin)&(tb.estimated_end<this_end)&(tb.group_id!=0)&(tb.group_id!=97)&(tb.resources_id!=1342) #&(tb.project==1)
            qry=(tb.estimated_begin>=this_begin)&(tb.estimated_end<this_end)&(tb.group_id!=0)&(tb.group_id!=97)&(tb.resources_id!=44488) #&(tb.project==1)
            if request.vars.search_project:
                qry=qry&(tb.task_parent==request.vars.search_project)
                request.vars.search_project=None
                

            if this_search_group:
                qry=qry&(tb[groups_key]==this_search_group)
            elif this_search_resource:
                qry=qry&(tb.resources==this_search_resource)
            task_parent = tb.task_parent.max()                  
            sum_available = tb.available_time.sum()
            sum_full = tb.total_time.sum()
            sum_effort = tb.estimated_effort.sum()
            sum_effort2 = tb.estimated_effort2.sum()
            sum_no_effort = tb.estimated_no_effort.sum()
            sum_no_effort2 = tb.estimated_no_effort2.sum()
            #
            sum_available_total = tb.available_time.sum()
            sum_effort_total = tb.estimated_effort.sum()

            #rs=db(qry).select(tb[this_groupby],sum_available,sum_full,sum_effort,sum_effort2,sum_no_effort,sum_no_effort2,groupby=tb[this_groupby])
            #if request.vars.has_key("par_ressources"):
            #    rs=db(qry).select(tb[this_groupby],task_parent,sum_available,sum_full,sum_effort,sum_effort2,sum_no_effort,sum_no_effort2,groupby=tb[this_groupby])
            #else:
            rs=db(qry).select(tb[this_groupby],task_parent,sum_available,sum_full,sum_effort,sum_effort2,sum_no_effort,sum_no_effort2,groupby=tb[this_groupby],orderby=tb[this_groupby])#orderby=~tb[this_groupby]
            #
            rs_sum_total=db(qry).select(tb["resources_id"],sum_available_total,sum_effort_total,groupby=tb["resources_id"])
            if rs_sum_total:
                rs_list+=[(this_begin,list(rs),rs_sum_total[0],1,)]
            else:
                rs_list+=[(this_begin,list(rs),0,0,)]

        grid='<body class="web2py_htmltable" style="width:100%;overflow-x:auto;-ms-overflow-x:scroll"><table>'
        if (this_groupby=='task_number')|(this_groupby=='task_parent')|(this_groupby=='resources'):
            #grid+="<tr><td class='head1'>Semain du:</td><td class='head1'>Heures totals</td><td class='head2'>Projet</td><td class='head2'>Heures planifiées</td><td class='head2'>Tâches sans effort</td><td class='head3'>Infra</td><td class='head3'>Heures planifiées</td><td class='head3'>Tâches sans effort</td></tr>"              
            grid+="<tr><td class='head1'>#</td><td class='head1'></td><td class='head2'></td><td class='head2'>Heures planifiées</td><td class='head2'>Tâches sans effort</td><td class='head3'>Infra</td><td class='head3'>Heures planifiées</td><td class='head3'>Tâches sans effort</td></tr>"              
        else:
            #grid+="<tr><td class='head1'>Semain du:</td><td class='head1'>Heures totals</td><td class='head2'>Projet</td><td class='head2'>Pourcentage utilisé</td><td class='head2'>Heures disponibles</td><td class='head2'>Tâches sans effort</td><td class='head3'>Infra</td><td class='head3'>Pourcentage utilisé</td><td class='head3'>Heures disponibles</td><td class='head3'>Tâches sans effort</td></tr>"
            grid+="<tr><td class='head1'>#</td><td class='head1'></td><td class='head2'></td><td class='head2'>Pourcentage utilisé</td><td class='head2'>Heures disponibles</td><td class='head2'>Tâches sans effort</td><td class='head3'>Infra</td><td class='head3'>Pourcentage utilisé</td><td class='head3'>Heures disponibles</td><td class='head3'>Tâches sans effort</td></tr>"
        #total=(0,0,0)
        for i in rs_list:
            if len(i[1]):
                #date head
                #week_begin=str(i[0].date())
                week_begin=""
                if (this_groupby=='task_number')|(this_groupby=='task_parent')|(this_groupby=='resources'):
                    grid+="<tr><th class='date_group1'>"+week_begin+"</th><th class='date_group1'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group3'></th><th class='date_group3'></th><th class='date_group3'></th></tr>"
                else:
                    grid+="<tr><th class='date_group1'>"+week_begin+"</th><th class='date_group1'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group2'></th><th class='date_group3'></th><th class='date_group3'></th><th class='date_group3'></th><th class='date_group3'></th></tr>"
                    
                #rows rs
                for j in i[1]:
                    this_task_parent=j[task_parent]
                    this_sum_available=j[sum_available]
                    this_sum_full=j[sum_full]
                    this_sum_effort=j[sum_effort]#projet affaire
                    this_sum_effort2=j[sum_effort2]#infra
                    this_sum_no_effort=j[sum_no_effort]
                    this_sum_no_effort2=j[sum_no_effort2]
                    
                    this_groups=j['capacity_report'][this_groupby]
                    this_title=this_groups

                    #create these links
                    
                    if this_groupby==groups_key:
                        #this_groups='<a href="./index/?search_group='+this_groups+'">'+this_groups+'</a>'
                        this_groups='<a href="https://'+request.env.http_host+'/init/gestion_ressources/report_project/'+groups_btn+'?search_group='+this_groups+'">'+this_groups+'</a>'
                        #this_groups='<a href="https://'+request.env.http_host+'/init/gestion_ressources/index/'+groups_btn+'?search_group='+this_groups+'&date_begin='+request.vars.date_begin+'">'+this_groups+'</a>'  
                    elif this_groupby=='resources':
                        search_project=request._get_vars.search_group
                        if search_project:
                            this_groups='<a href="https://'+request.env.http_host+'/init/gestion_ressources/report_project/'+groups_btn+'?search_resource='+this_groups+'&search_project='+search_project+'">'+this_groups+'</a>'
                        else:
                            this_groups='<a href="https://'+request.env.http_host+'/init/gestion_ressources/report_project/'+groups_btn+'?search_resource='+this_groups+'">'+this_groups+'</a>'
                    if this_sum_available:
                        #35h to 28h availablity
                        #not change is in gestion_absence
                        #if (this_groupby=='task_number')|(this_groupby=='resources'):
                        #    this_sum_available=this_sum_available-420
                        #    if this_sum_available<0:this_sum_available=0
                        #
                        this_sum_total="{:5.2f}".format(this_sum_available/60.)
                    else:
                        #this_sum_total="0.00"
                        this_sum_total=""

                    #definition portion de projets
                    #hours2=this_sum_full/2.#infra priority
                    hours2=0#no infra
                    hours=this_sum_available-hours2#for proj
                    #definition available/available2
                    this_sum_available=(hours-this_sum_effort)/60.#infra
                    this_sum_available2=(hours2-this_sum_effort2)/60.#proj

                    #if this_sum_available<0:
                    if this_sum_available<0:
                        #red_class="class='red_class'"
                        red_class="red_class"
                        #
                        this_sum_available=0
                    else:
                        red_class=""
                    #2
                    if this_sum_available2<0:
                        #red_class="class='red_class'"
                        red_class2="red_class"
                    else:
                        red_class2=""  

                    #if this_sum_available>0:
                    if hours:
                        percents=int(float(this_sum_effort)/float(hours)*100)
                    else:
                        percents=100000
                    #2
                    #if this_sum_available2>0:
                    if hours2:
                        percents2=int(float(this_sum_effort2)/float(hours2)*100)
                    else:
                        percents2=100000

                    if this_sum_available:
                        this_sum_available="{:5.2f}".format(this_sum_available)
                    else:
                        this_sum_available="0.00"
                        #this_sum_available=""
                    #2
                    if this_sum_available2:
                        this_sum_available2="{:5.2f}".format(this_sum_available2)
                    else:
                        this_sum_available2=""

                    if this_sum_effort:
                        this_sum_effort="{:5.2f}".format(this_sum_effort/60.)
                    else:
                        this_sum_effort=""
                    #2
                    if this_sum_effort2:
                        this_sum_effort2="{:5.2f}".format(this_sum_effort2/60.)
                    else:
                        this_sum_effort2=""

                    if this_sum_no_effort:
                        this_sum_no_effort="{:5d}".format(this_sum_no_effort)
                    else:
                        this_sum_no_effort=""
                    #2
                    if this_sum_no_effort2:
                        this_sum_no_effort2="{:5d}".format(this_sum_no_effort2)
                    else:
                        this_sum_no_effort2=""

                    if percents==100000:
                        percents_text=''
                    else:
                        percents_text=str(percents)
                    percents=str(percents)
                    percents='<div class="progress"><div class="progress-bar progress-bar-animated" role="progressbar" aria-valuenow="'+percents+'"aria-valuemin="0" aria-valuemax="100" style="width:'+percents+'%;"><div align="left" style="margin-left: 20px;">'+percents_text+'%</div></div></div>'

                    if percents2==100000:
                        percents2_text=''
                    else:
                        percents2_text=str(percents2)
                    percents2=str(percents2)
                    percents2='<div class="progress"><div class="progress-bar progress-bar-animated" role="progressbar" aria-valuenow="'+percents2+'"aria-valuemin="0" aria-valuemax="100" style="width:'+percents2+'%;"><div align="left" style="margin-left: 20px;">'+percents2_text+'%</div></div></div>'

                    if (this_groupby=='task_number')|(this_groupby=='task_parent')|(this_groupby=='resources'):
                        if this_groups=="":
                            this_groups='<i>'+this_search_resource+'</i>'
                            this_sum_total="<b>"+this_sum_total+"</b>"
                            if (this_groupby=='task_number')|i[3]:
                                #total effort by resource 
                                this_sum_effort="{:5.2f}".format(i[2][sum_effort_total]/60.)
                                this_sum_effort="<b>"+this_sum_effort+"</b>"
                                
                        else:
                            #this_groups=this_groups+' - '+this_task_parent.split('|')[0]+''
                            this_groups=this_groups
                        
                        ####
                        if (this_groupby=='task_parent'):
                            #if ("DRT-" in this_groups)|("DRI-" in this_groups):
                            if (this_title[:3]=="DRT")|(this_title[:3]=="DRI"):                       
                                grid+="<tr><td class='details1'>"+this_groups+"</td><td class='details1'>"+this_sum_total+"</td><td class='details2'></td><td class='details2'>"+this_sum_effort+"</td><td class='details2'>"+this_sum_no_effort+"</td><td class='details3'></td><td class='details3'>"+this_sum_effort2+"</td><td class='details3'>"+this_sum_no_effort2+"</td></tr>"
                        else:
                            grid+="<tr><td class='details1'>"+this_groups+"</td><td class='details1'>"+this_sum_total+"</td><td class='details2'></td><td class='details2'>"+this_sum_effort+"</td><td class='details2'>"+this_sum_no_effort+"</td><td class='details3'></td><td class='details3'>"+this_sum_effort2+"</td><td class='details3'>"+this_sum_no_effort2+"</td></tr>"

                    else:
                        #if ("DRT-" in this_groups)|("DRI-" in this_groups):
                        grid+="<tr><td class='details1'>"+this_groups+"</td><td class='details1'>"+this_sum_total+"</td><td class='details2'></td><td class='details2'>"+percents+"</td><td class="+"'details2 "+red_class+"'>"+this_sum_available+"</td><td class='details2'>"+this_sum_no_effort+"</td><td class='details3'></td><td class='details3'>"+percents2+"</td><td class='details3 "+red_class2+"'>"+this_sum_available2+"</td><td class='details3'>"+this_sum_no_effort2+"</td></tr>"




        grid+="</table></body>"

    #response.flash = request.vars.search_project
    #request._get_vars.search_group
    #response.flash = request.vars.has_key("par_projets")
    #response.flash=request.env.http_host
    return dict(form=form,grid=grid)

#tranformation for rapport
def weeks_separation():
    tb=db.capacity_management
    tb2=db.capacity_report
    #delete again
    db(tb2.id>0).delete() #already deleted in python import script
    redo=True
    separated_list_sum=()
    errors=()
    while redo:
        #date_begin=datetime.datetime(2016, 1, 1, 0, 0)
        date_begin=datetime.datetime(2018, 1, 1, 0, 0)
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
                        r_end=datetime.datetime(b.year,b.month,b.day)+datetime.timedelta(days=ds)
                        if r_end<r.estimated_end:rec_end=r_end-datetime.timedelta(seconds=1)
                        else:rec_end=r.estimated_end
                        wd=working_days(r_begin,rec_end)

                        #effort=r.estimated_effort
                        effort=estimated_effort*wd
                        if r.estimated_effort:estimated_no_effort=0
                        else:estimated_no_effort=1

                        if r.project:
                            r_estimated_effort=effort
                            r_estimated_effort2=0

                            r_estimated_no_effort=estimated_no_effort
                            r_estimated_no_effort2=0
                        else:
                            r_estimated_effort=0
                            r_estimated_effort2=effort

                            r_estimated_no_effort=0
                            r_estimated_no_effort2=estimated_no_effort
                       
                        qry=(tb2.resources_id==r.resources_id)&\
                            (tb2.group_id==r.group_id)&\
                            (tb2.task_id==r.task_id)&\
                            (tb2.estimated_begin==r_begin)&\
                            (tb2.estimated_end==rec_end)

                        if not(db(qry).select(tb2.id)):
                            tb2.insert(
                                resources_id=r.resources_id,
                                resources=r.resources,
                                group_id=r.group_id,
                                groups=r.groups,
                                task_id=r.task_id,
                                task_parent=r.parent_subject,
                                task_number=r.task_number,
                                estimated_begin=r_begin,
                                estimated_end=rec_end,
                                estimated_effort=r_estimated_effort,
                                estimated_effort2=r_estimated_effort2,
                                estimated_no_effort=r_estimated_no_effort,
                                estimated_no_effort2=r_estimated_no_effort2,
                                available_time=0,
                                total_time=0,
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
                effort=r.estimated_effort
                if r.estimated_effort:estimated_no_effort=0
                else:estimated_no_effort=1

                if r.project:
                    r_estimated_effort=effort
                    r_estimated_effort2=0

                    r_estimated_no_effort=estimated_no_effort
                    r_estimated_no_effort2=0
                else:
                    r_estimated_effort=0
                    r_estimated_effort2=effort

                    r_estimated_no_effort=0
                    r_estimated_no_effort2=estimated_no_effort



                tb2.insert(
                            resources_id=r.resources_id,
                            resources=r.resources,
                            group_id=r.group_id,
                            groups=r.groups,
                            task_id=r.task_id,
                            task_parent=r.parent_subject,
                            task_number=r.task_number,
                            estimated_begin=r.estimated_begin,
                            estimated_end=r.estimated_end,
                            estimated_effort=r_estimated_effort,
                            estimated_effort2=r_estimated_effort2,
                            estimated_no_effort=r_estimated_no_effort,
                            estimated_no_effort2=r_estimated_no_effort2,
                            available_time=0,
                            total_time=0,
                            status_id=r.status_id,
                            status=r.status,
                )

    #insert available_time for all ressources by week
    date_begin=datetime.datetime(2018, 1, 1, 0, 0)    
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
            #calcule available_time
            #time_reserved=0 #35h by week for project and else
            time_reserved=420 #28h by week for project and else
            if available_time:
                available_time=available_time[0].bank-time_reserved
            else:
                ##### condition for available need remove in record too
                #if r.id in (27,36,31):available_time=600
                #else:available_time=1050
                #available_time=1050 #35*60=2100 good line original
                available_time=2100-time_reserved #full availablity in one week
            if available_time<0:
                available_time=0
                            
            tb2.insert(
                resources_id=r.resources_id,
                resources=r.title,
                group_id=r_groups_id,
                groups=r_groups_title,
                task_id=0,
                task_parent='',
                task_number='',
                estimated_begin=this_begin,
                estimated_end=this_end,
                estimated_effort=0,
                estimated_effort2=0,
                estimated_no_effort=0,
                estimated_no_effort2=0,
                available_time=available_time,
                total_time=2100,
                status_id=0,
                status='',
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
    script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ressources\read_octopus_projet_affaires.py'
    p1 = subprocess.Popen([r'C:\python27\python.exe',script],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,error = p1.communicate()
    msg=weeks_separation()
            
    redirect(URL('index'))

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources'))
auth.settings.allow_basic_login = True
@auth.requires_login()
@request.restful()
def project_update_by_request():
    def GET(input):
        output="have no access"
        start=str(now)
        if (auth.has_membership(role='gestion_ressources_update'))&(input=="project_update_by_request"):
            #if True:
            import subprocess 
            script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ressources\read_octopus_projet_affaires.py'
            p1 = subprocess.Popen([r'C:\python27\python.exe',script],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output,error = p1.communicate()
            msg=weeks_separation()
            output=start+";erorrs: "+msg+";"+str(datetime.datetime.now())+'\r\n'
        script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ressources\log.txt'
        f=open(script,"a")
        f.write(output)
        f.close()                
        return output
        session.forget()
    return locals()

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ressources'))
def tables():
    menu_url=[]
    tables=["resources","groups","resource_group","capacity_availability","capacity_management","capacity_report","capacity_reports_created"]

    for table in tables:
    #    if '_' not in table: # tables will be in menu
    #        menu_url+=[(T(table), False, URL(c='manage',f='manage',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[table])),]

    response.menu += [(T("Tables"), False, '#', menu_url)]

    table = request.args(0) or 'capacity_management'
    if not table in db.tables(): redirect(URL('error'))

    grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

 
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


