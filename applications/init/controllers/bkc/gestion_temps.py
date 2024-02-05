# -*- coding: utf-8 -*-
import os
import datetime



now=datetime.datetime.now();today=datetime.date.today()
response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Gestion des changements"), False, '#', [
        (T('Calendrier'), False, URL( f='index'),[]),
        (T('Tables'), False, URL( f='tables'),[]),
        ]),
    
    ]
    

#parameters
#this_object_group="INFRA ABSENCE"
#this_write_role='gestion_absence'
this_object_group="INFRA"
this_write_role='gestion_temps'

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role=this_write_role))

def index():
    response.menu+=[
        (T('Calendrier'), False, URL( f='index'),[]),
        ]
    #tbl_object=db((db.rs_object.is_active==True)).select(db.rs_object.id,db.rs_object.title)
    tbl_object=db((db.rs_object.object_group==this_object_group)).select(db.rs_object.id,db.rs_object.title)
    object_items=[]
    object_list=()
    for i in tbl_object:
        object_items+=[(i.title.upper(),i.id),]
        object_list+=(i.id,)
    #rs_type
    tbl_type=db((db.rs_type.object_group==this_object_group)).select(db.rs_type.id,db.rs_type.title,db.rs_type.color)
    type_items=[]
    color_items={}
    for i in tbl_type:
        type_items+=[(i.id,i.title.upper()),]
        color_items[i.id]=i.color.lower()

        
    #msg=str(color_items)
    #db(db.rs_details.id>0).update(task_id=0)
    #db(db.rs_details.id>=1249).delete()
    
    


    if not request.vars.object:
        request.vars.object=object_list[0]
    #msg=request.vars.object +"su"
    #msg=request.vars

    
    view={
        0: 'mois',\
        #1: 'jour',\
        2: 'avec enregistements annulés',\
        }
    if ('all_view' in request.vars):
        all_view_checked=True
    else:
        all_view_checked=False
        

    form=FORM(
        TABLE(
            TR(
            #TD(LABEL("GROUPE DE CALENDRIER ",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (v,k) in object_items],_class='class_input',_name='object',_value=request.vars.object)),
            #TD(T('Design Mode'),INPUT(_type='checkbox',_name='design',_value=False,value=design_checked)))
            TD(LABEL("VUE GLOBALE ",INPUT(_type='checkbox',_class='my_label',_name='all_view',value=all_view_checked))),#all_view_checked
            TD(LABEL("VUE DÉTAILLÉE ",INPUT(_type='checkbox',_class='my_label',_name='detail_view',_value=False))),
            TD('',INPUT(_class='button_command',_type='submit',_value='actualiser',_id='actualiser',_name='actualiser',_style='background-color:#339FFF')),#green
            TD('',INPUT(_class='button_command',_type='submit',_value='aujourd\'hui',_id='aujourd\'hui',_name='aujourd\'hui',_style='background-color:#339FFF')),#green
            TD(LABEL("VUE PAR ",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (k,v) in view.items()],_class='class_input',_name='view_by',_value=request.vars.view_by)),
            ),
            TR(''),
            TR(''),
            TR(
            )))
    tm_id=0
    msg=''
    form.vars.view_by='0'
    #test

    

    """

    if (auth.has_membership(role='admin')|auth.has_membership(role=this_write_role)):
        action_button='submit'
    else:
        action_button='hidden'

    """
    if form.accepts(request.vars,session):
        
        qdb=db.rs_details
        
        #time=datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),int(time[11:13]),int(time[14:16]),0,0)
        #if not request.vars.date: request.vars.date=str(today)
        #date=request.vars.date
        #date=datetime.datetime(int(date[0:4]),int(date[5:7]),int(date[8:10]),0,0,0,0)


        if not request.vars.object: request.vars.object='1'
        if not request.vars.rs_type: request.vars.rs_type='1'
        if not request.vars.title: request.vars.title=''
        if not request.vars.description: request.vars.description=''
        if not request.vars.date: request.vars.date=str(today)
        if not request.vars.hour_begin: request.vars.hour_begin=9
        if not request.vars.minute_begin: request.vars.minute_begin=0
        if not request.vars.hour_end: request.vars.hour_end=12
        if not request.vars.minute_end: request.vars.minute_end=30


        value_replace_id=''
        value_user=''
        value_edit_time=''


        value_object=request.vars.object
        value_rs_type=request.vars.rs_type
        value_title=request.vars.title
        value_description=request.vars.description
        #value_preparation=time-datetime.timedelta(minutes=preparation)
        value_hour_begin=request.vars.hour_begin
        value_minute_begin=request.vars.minute_begin
        value_hour_end=request.vars.hour_end
        value_minute_end=request.vars.minute_end
        date=str(request.vars.date)
        value_date=date
        time=str(request.vars.date)
        begin=datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),int(value_hour_begin),int(value_minute_begin),0,0)
        end=datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),int(value_hour_end),int(value_minute_end),0,0)
        date=datetime.datetime(int(date[0:4]),int(date[5:7]),int(date[8:10]),0,0,0,0)
       
        have_new_record=False
        this_record=0
        load=False

        try:
            submit_index=(request.vars.values()).index('Working...')
            s=request.vars.keys()[submit_index]
        except:
            s=''
            #str(today.day)


        if s.isdigit():
            #date=datetime.datetime(int(date[0:4]),int(date[5:7]),int(date[8:10]),0,0,0,0)
            date=datetime.date(date.year,date.month,int(s))
            value_date=str(date)
            this_id=0
            value_rs_type=1
            value_title=''
            value_description=''
            value_hour_begin=9
            value_minute_begin=0
            value_hour_end=12
            value_minute_end=30

            
        else:
            s=s[s.find('#')+1:]
            if s.isdigit():
                this_id=int(s)
                load=True
            else:
                if request.vars.this_id:
                    #pass
                    this_id=(request.vars.this_id)
                    rs=db(qdb.id==this_id).select(qdb.id)
                    if len(rs)<1:
                        this_id=0
                else:
                    this_id=0

        if request.vars.has_key('actualiser'):
            value_title=''
            value_rs_type=1
            value_description=''
            value_hour_begin=9
            value_minute_begin=0
            value_hour_end=12
            value_minute_end=30
            #if (request.vars.submit=='aujourd\'hui'):
        elif request.vars.has_key('aujourd\'hui'):
            #msg+='aujourd\'hui'
            date=today
            value_date=str(date)
            this_id=0
            value_rs_type=1
            value_title=''
            value_description=''
            value_hour_begin=9
            value_minute_begin=0
            value_hour_end=12
            value_minute_end=30
        elif request.vars.has_key('créer'):
            if ((begin>=now)&(begin<end))|auth.has_membership(role=this_write_role):
                rs=db.rs_details.insert(\
                   rs_object=request.vars.object,\
                   rs_type=request.vars.rs_type,\
                   title=request.vars.title[:999],\
                   description=request.vars.description[:3999],\
                   time_begin=begin,\
                   time_end=end,\
                   replace_id=0,\
                   edit_by=auth.user_id,\
                   edit_time=now,\
                   )
                if rs:
                    have_new_record=True
                    this_record=rs
                    this_id=rs
                    msg+='New record has been added'
                else:
                    msg+='Cannot add!'

            else:
                msg+="To create new record  the time must be in the future!"
        #elif (request.vars.submit=='modifier'):
        elif request.vars.has_key('modifier'):
            rs=db(qdb.id==this_id).select(qdb.rs_object,qdb.rs_type,qdb.title,\
                                          qdb.description,qdb.time_begin,qdb.time_end,qdb.replace_id,qdb.edit_by,qdb.edit_time)
            if (len(rs)==1):
                if (rs[0].time_begin>=now)&(begin>=now)&(begin<end)&(rs[0].replace_id==0)|auth.has_membership(role=this_write_role):
                    if (rs[0].edit_by==auth.user_id): #auth.has_membership(role='users_rs')|(rs[0].edit_by==auth.user_id)
                        
                        rs=db.rs_details.insert(\
                           rs_object=request.vars.object,\
                           rs_type=request.vars.rs_type,\
                           title=request.vars.title[:999],\
                           description=request.vars.description[:3999],\
                           time_begin=begin,\
                           time_end=end,\
                           replace_id=0,\
                           edit_by=auth.user_id,\
                           edit_time=now,\
                           )
                        if rs:
                            have_new_record=True
                            this_record=rs
                            rs=db(qdb.id==this_id).update(\
                               replace_id=rs,\
                               )
                            this_id=this_record
                            load=True
                            msg+='A new record has been created and old record is cancelled!'
                    else:
                        msg+='Cannot modify a record that created by another user!'
                        

                elif (begin<now)|(rs[0].time_begin<now):
                    msg+="To modify this record  the time must be in the future!"
                    #msg+=str(begin)
                elif (rs[0].replace_id<>0):
                    msg+="This record was already cancelled and cannot modify"
            else:
                msg+="This record does not exist!"
        #elif (request.vars.submit=='annuler'):#auth.has_membership(role='users_tr') auth_membership.group_id
        elif request.vars.has_key('annuler'):
            rs=db(qdb.id==this_id).select(qdb.time_begin,qdb.edit_time,qdb.edit_by,qdb.replace_id)
            if (len(rs)==1):
                if (rs[0].time_begin>=now)&(rs[0].replace_id==0)|auth.has_membership(role=this_write_role):
                    if (rs[0].edit_by==auth.user_id): #auth.has_membership(role='users_rs')|(rs[0].edit_by==auth.user_id):
                        this_record=this_id
                        rs=db(qdb.id==this_id).update(\
                            replace_id=-auth.user_id,\
                            )
                        msg+='This record has been cancelled'
                        load==True
                    else:
                        msg+='Cannot cancel a record that created by another user!'
                elif (rs[0].time_begin<now):
                    msg+="To create a new record  the time must be in the future!"
                elif (rs[0].replace_id<>0):
                    msg+="This record was already cancelled"

            else:
                msg+="This record does not exist!"
        #elif (request.vars.submit=='supprimer'):
        elif request.vars.has_key('supprimer'):
            rs=db(qdb.id==this_id).select(qdb.time_begin,qdb.edit_time,qdb.edit_by)
            if (len(rs)==1):
                if(rs[0].time_begin>now):
                    if ((now-rs[0].edit_time).seconds<=900)&(rs[0].edit_by==auth.user_id):#15 minutes
                        rs=db(qdb.id==this_id).delete()
                        if rs: msg+='One record has been deleted'
                    else:
                        msg+='Cannot delete a record that is older than 15 minutes or created by another user!'
                else:
                    msg+="To delete a record  the time must be in the future!"
            else:
                msg+="This record does not exist!"
                    
        if load:
            rs=db((qdb.id==this_id)).select(qdb.rs_object,\
            qdb.rs_type,\
            qdb.title,\
            qdb.description,\
            qdb.time_begin,\
            qdb.time_end,\
            qdb.replace_id,\
            qdb.edit_by,\
            qdb.edit_time,\
            )
                                          
            value_object=str(rs[0].rs_object)
            request.vars.object=value_object
            #msg+="this load"+str(request.vars.object)
            value_rs_type=str(rs[0].rs_type)
            value_title=str(rs[0].title)
            value_description=str(rs[0].description)
            value_date=str(rs[0].time_begin)[0:10]
            value_hour_begin=str(rs[0].time_begin)[11:13]
            value_minute_begin=str(rs[0].time_begin)[14:16]
            value_hour_end=str(rs[0].time_end)[11:13]
            value_minute_end=str(rs[0].time_end)[14:16]
            
            value_replace_id=str(rs[0].replace_id)
            value_user=str(rs[0].edit_by)
            value_edit_time=str(rs[0].edit_time)
            #msg+=value_edit_time


        #form[0][0].insert(6,TD(T('Begin:'),INPUT(_type='text',_class='date',_name='begin',_id='begin',value=value_begin,_size=10,requires=IS_DATE())))
        #form[0][0].insert(7,TD(T('End:'),INPUT(_type='text',_name='end',_class='date',_id='end',value=value_end,_size=10,requires=IS_DATE())))

        tdb_set=(qdb.replace_id==0)
        if int(request.vars.view_by)==0:
           tdb_set=(qdb.replace_id==0)
        elif int(request.vars.view_by)==1:
            tdb_set=(qdb.replace_id==0)
        elif int(request.vars.view_by)==2:
            tdb_set=((qdb.replace_id>=0)|(qdb.replace_id<0))

        if ('all_view' in request.vars):
            qry_view=qdb.rs_object.belongs(object_list)
            #msg+=str(object_list)
        else:
            qry_view=qdb.rs_object==int(request.vars.object)

        tdb_set=tdb_set&(qry_view)&(qdb.rs_object==db.rs_object.id)&(qdb.edit_by==db.auth_user.id)


            
        #records
        rc=db(tdb_set).select(\
            qdb.id,\
            qdb.rs_type,\
            qdb.title,\
            qdb.description,\
            qdb.time_begin,\
            qdb.time_end,\
            qdb.replace_id,\
            #qdb.edit_by,\
            db.auth_user.last_name,\
            qdb.edit_time,\
            orderby=qdb.time_begin,\
            )
        dic={}
        red_record=False
        strike_record=False
        for rs in rc:
            #red_record=False
            i=rs.rs_details.time_begin.date()
            #strike_record
            if rs.rs_details.replace_id<>0:
                strike_record=True
                #pdf_strike+=(rs.rs_details.id,)
                red_record=False
            else:
                strike_record=False
            #red_record
            if not strike_record:
                time_min=rs.rs_details.time_begin
                time_max=rs.rs_details.time_end
                red_rs=db((((qdb.time_begin>=time_min)&(qdb.time_begin<=time_max))|\
                            ((qdb.time_end>=time_min)&(qdb.time_end<=time_max))|\
                            ((qdb.time_begin<=time_min)&(qdb.time_end>=time_max)))&\
                            (qdb.replace_id==0)&(qdb.rs_object==int(request.vars.object))).count()
                if red_rs>1:
                    red_record=True
                    #pdf_red+=(row['rs_details']['id'],)
                else:
                    red_record=False
            #end red record
            j=(rs.rs_details.id,rs.rs_details.time_begin,rs.rs_details.time_end,rs.rs_details.title,rs.auth_user.last_name,red_record,strike_record,rs.rs_details.rs_type,)
            if dic.has_key(i):
                dic[i]+=(j,)
            else:
                dic[i]=(j,)
        #msg+=str(dic)
        #msg+=str(date)
        #msg+=str(begin)
        #msg+=str(end)
        
        st={'RS_DETAILS.ID':'#',\
            'RS_DETAILS.RS_TYPE':'TYPE',\
            'RS_DETAILS.TITLE':'AFFICHAGE',\
            'RS_DETAILS.DESCRIPTION':'DESCRIPTION',\
            'RS_DETAILS.TIME_BEGIN':'DÉBUT',\
            'RS_DETAILS.TIME_END':'FIN',\
            'RS_DETAILS.REPLACE_ID':'REF.',\
            'AUTH_USER.LAST_NAME':'UTILISATEUR',\
            'RS_DETAILS.EDIT_TIME':'MODIFIÉ',\
            }
        #TD(LABEL("VUE PAR ",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (k,v) in view.items()],_class='class_input',_name='view_by',_value=request.vars.view_by)),
        ##form[0][0].insert(6,TD(T('Begin:'),INPUT(_type='text',_class='date',_name='begin',_id='begin',value=value_begin,_size=10,requires=IS_DATE())))
        #form[0][0].insert(1,DIV(LABEL("DATE ",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date',_id='date',value=value_date,_size=10,requires=IS_DATE())))#2 class _class="date input"
        #month_disp
        month_lst = ('	janvier', '	février', 'mars', 'avril', 'mai', 'juin', 'juillet','août', 'septembre', 'octobre', 'novembre', 'décembre')
        month_disp=(month_lst[date.month-1].upper())+" / "+str(date.year)
        #TD(LABEL("GROUPE DE CALENDRIER ",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (v,k) in object_items],_class='class_input',_name='object',_value=request.vars.object)),
        form[0][0].insert(0,TD(LABEL("GROUPE DE CALENDRIER ",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (v,k) in object_items],_class='class_input',_name='object',value=request.vars.object)))#value_object
        form[0][0].insert(1,TD(LABEL(month_disp,_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date',_id='date',value=value_date,_size=10,requires=IS_DATE())))#2 class _class="date input"
        
        #form.insert(len(form),TABLE(INPUT(_type='hidden'))) #form_details #000AAA #_border=1,_style='background-color:#FFF8C6;border-color: #D8D8D8;'
        form.insert(len(form),TABLE()) #form_details #000AAA #_border=1,_style='background-color:#FFF8C6;border-color: #D8D8D8;'
       
        d1=len(form)-1
        form_dts=(form[d1],)
        rs=()
        rs+=(rc,)
        k=0
        #msg+=str(rc)
        for  rcs in rs:
            form_details=form_dts[k]
            if len(rcs)>=0:
                for i in range(len(rcs)+2):
                    form_details.insert(i,TR())
                #last_time=datetime.datetime(2000, 10, 12, 11, 40, 23, 542000)
                red_record=False
                #shift_disp='<strike>'+r.shift.disp+'</strike>'
                strike_record=False
                imax=len(rcs)+2
                pdf_red=()
                pdf_strike=()
                for i in range(2):#for i in range(imax):
                                
                    for j in range(len(rcs.colnames)):
                        if i==1:
                            #request.vars.
                            if j==0:
                                if (this_id<>0):#&(load)
                                    disp_this_id=str(this_id)
                                else:
                                    disp_this_id='---'
                                disp_this_id=XML("<b><font color='green'>"+disp_this_id+"</font>")
                                form_details[i].insert(j,TD(TABLE(
                                    TR(TD(INPUT(_type='hidden',_name='this_id',_value=this_id,_readonly='on'),disp_this_id)),
                                    )))
                            if j==1:
                                form_details[i].insert(j,TABLE(
                                    TR(TABLE(TR(\
                                    TD(SELECT(*[OPTION(v,_value=k) for (k,v) in type_items],_class='class_input',_name='rs_type',value=value_rs_type)),\
                                ))))),
                                                               
                            elif j==2:
                                #TD(LABEL("VUE PAR ",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (k,v) in view.items()],_class='class_input',_name='view_by',_value=request.vars.view_by)),
                                form_details[i].insert(j,TD(TEXTAREA(_type='text',_class='class_input',_name='title',value=value_title,_rows=2,_cols=30)))
                                #form_details[i].insert(j,TD(TEXTAREA(_type='hidden',_readonly='on',_name='title',value=value_title,_rows=1,_cols=20)))
                            elif j==3:
                                #form_details[i].insert(j,TD(TEXTAREA(_type='text',_class='class_input',_name='description',value=value_description,_rows=2,_cols=60)))
                                if ('detail_view' in request.vars):
                                    deltail_col=150
                                    deltail_row=(len(value_description)/deltail_col)+value_description.count('\r')
                                else:
                                    deltail_row=2;deltail_col=60
                                form_details[i].insert(j,TD(TEXTAREA(_type='text',_class='class_input',_name='description',value=value_description,_rows=deltail_row,_cols=deltail_col)))
                            elif j==4:
                                form_details[i].insert(j,TABLE(\
                                    TR(TABLE(TR(\
                                        TD(SELECT(*[OPTION(v,_value=k) for (k,v) in \
                                                    [(0, '00'), (1, '01'), (2, '02'), (3, '03'),(4, '04'), (5, '05'),(6, '06'), (7, '07'), (8, '08'), (9, '09'),(10, '10'), (11, '11'), (12, '12'),\
                                                     (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23')]\
                                                    ],_class='class_input',_name='hour_begin',value=int(value_hour_begin))),\
                                        TD(SELECT(*[OPTION(v,_value=k) for (k,v) in \
                                                    [(0, '00'),(5, '05'), (10, '10'), (15, '15'), (20, '20'),(25, '25'), (30, '30'), (35, '35'), (40, '40'), (45, '45'), (50, '50'), (55, '55'), (59, '59')]\
                                                    ],_class='class_input',_name='minute_begin',value=int(value_minute_begin))),\

                                        ))),
                                    ))
                            
                            elif j==5:
                                if (auth.has_membership(role='admin')|auth.has_membership(role=this_write_role)):
                                    form_details[i].insert(j,TABLE(\
                                        TR(TABLE(TR(\
                                            TD(SELECT(*[OPTION(v,_value=k) for (k,v) in \
                                                        [(0, '00'), (1, '01'), (2, '02'), (3, '03'),(4, '04'), (5, '05'),(6, '06'), (7, '07'), (8, '08'), (9, '09'),(10, '10'), (11, '11'), (12, '12'),\
                                                        (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23')]\
                                                        ],_class='class_input',_name='hour_end',value=int(value_hour_end))),\
                                            TD(SELECT(*[OPTION(v,_value=k) for (k,v) in \
                                                        [(0, '00'),(5, '05'), (10, '10'), (15, '15'), (20, '20'),(25, '25'), (30, '30'), (35, '35'), (40, '40'), (45, '45'), (50, '50'), (55, '55'), (59, '59')]\
                                                        ],_class='class_input',_name='minute_end',value=int(value_minute_end))),\
                                            TD(TABLE(\
                                        TR(TD('',INPUT(_class='button_command',_type='submit',_value='créer',_id='créer',_name='créer',_style='background-color:green')),\
                                        TD('',INPUT(_class='button_command',_type='submit',_value='modifier',_id='modifier',_name='modifier',_style='background-color:pink')),\
                                        TD('',INPUT(_class='button_command',_type='submit',_value='annuler',_id='annuler',_name='annuler',_style='background-color:pink')),\
                                        TD('',INPUT(_class='button_command',_type='submit',_value='supprimer',_id='supprimer',_name='supprimer',_style='background-color:red')),\
                                        ),\
                                        )),\

                                        ))),\
                                        ))
                                else:
                                    form_details[i].insert(j,TABLE(\
                                        TR(TABLE(TR(\
                                            TD(SELECT(*[OPTION(v,_value=k) for (k,v) in \
                                                        [(0, '00'), (1, '01'), (2, '02'), (3, '03'),(4, '04'), (5, '05'),(6, '06'), (7, '07'), (8, '08'), (9, '09'),(10, '10'), (11, '11'), (12, '12'),\
                                                        (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23')]\
                                                        ],_class='class_input',_name='hour_end',value=int(value_hour_end))),\
                                            TD(SELECT(*[OPTION(v,_value=k) for (k,v) in \
                                                        [(0, '00'),(5, '05'), (10, '10'), (15, '15'), (20, '20'),(25, '25'), (30, '30'), (35, '35'), (40, '40'), (45, '45'), (50, '50'), (55, '55'), (59, '59')]\
                                                        ],_class='class_input',_name='minute_end',value=int(value_minute_end))),\
                                            

                                        ))),\
                                        ))                                    
                            
                            elif j==6:
                                form_details[i].insert(j,TD(value_replace_id))
                            elif j==7:
                                form_details[i].insert(j,TD(value_user))
                            elif j==8:
                                form_details[i].insert(j,TD(DIV(value_edit_time)))
                            

                        elif i==0: #<font color='green'>Sat</font>
                            #st="<b><font color='blue'>"+(rcs.colnames[j].split('.')[1])+'</b></font>'
                            stt="<b><font color='blue'>"+st[(rcs.colnames[j]).upper()]+'</b></font>'
                            form_details[i].insert(j,TD(XML(stt)))#TH
        #calendar

        #form.insert(len(form),TABLE(_border=1,_style='background-color:#CFF8C5;border-color: #000AAC;')) #form_details #000AAA
        form.insert(len(form),TABLE()) #form_details #000AAA

       
        #d1=len(form)-1
        #form_dts=(form[d1],)
        #month_lst = ('January', 'Feburary', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December')
        #month_lst = ('	janvier', '	février', 'mars', 'avril', 'mai', 'juin', 'juillet','août', 'septembre', 'octobre', 'novembre', 'décembre')
        #color='blue'
        #stt="<b><font color='"+color+"'>"+(month_lst[date.month-1].upper())+" / "+str(date.year)+"</b></font>"
        #month_disp=(month_lst[date.month-1].upper())+" / "+str(date.year)
        #form_details=form_dts[0]

        #form_details.insert(0,TR(XML(stt),_style='text-align:center;background-color:lightyellow;'))#TH ;width:30em

        #LABEL("VUE PAR ",_class='my_label')
        #form_details.insert(0,TR(LABEL(stt,_class='my_label'),_style='text-align:center;'))#TH ; MARCH / 2017
        #form_details.insert(0,TR(LABEL(stt,_class='my_label'),_style='text-align:center;'))#TH ; MARCH / 2017


        #form.insert(len(form),TABLE(_border=1,_style='background-color:#CFF8C5;border-color: #000AAC;')) #form_details #000AAA
        form.insert(len(form),TABLE()) #form_details #000AAA

       
        d1=len(form)-1
        form_dts=(form[d1],)
        rs=()
        rs+=(rc,)
        k=0
        
        fday=datetime.date (date.year, date.month, 1)
        if date.month>11:
            lday=datetime.date (date.year+1, 1, 1)- datetime.timedelta (days = 1)
        else:
            lday=datetime.date (date.year,date.month+1, 1)- datetime.timedelta (days = 1)
        #msg+=str(fday)
        #msg+=str(lday)
        form_details=form_dts[k]
        week_days=("DIM","LUN","MAR","MER","JEU","VEN","SAM")
        k=0
        fisowd=fday.isoweekday()%7-1
        ldaym=lday.day
        #msg+=str(fday)
        #msg+=str(lday)
        #msg+=str(fisowd)
        t=0
        #h_hight=26
        h_hight=26

        for i in range(7):
            form_details.insert(i,TR())
            for j in range(7):
                if i==0:
                    if (j==0)|(j==6):
                        color='red'
                    else: color='blue'
                    stt="<b><font color='"+color+"'>"+week_days[j]+"</b></font>"
                    #stt=week_days[j]
                    #form_details[i].insert(j,TD(XML(stt),_style='text-align:center;background-color:lightyellow'))#TH ;width:8em
                    #LABEL(stt,_class='my_label')
                    form_details[i].insert(j,TD(XML(stt),_style='text-align:center'))#TH ;width:8em
                    #form_details[i].insert(j,TD(LABEL(stt,_class='my_label'),_style='text-align:center'))#TH ;width:8em
                else:
                    td_h= h_hight
                    bt_h= h_hight
                    day=k-fisowd
                    #TD for square
                    if str(today.day)==str(day):
                        background_color='#08088A'
                    else:
                        background_color='white'
                    #form_details[i].insert(j,TD('',_style='background-color:yellow'))#height:'+str(bt_h)+'em
                    td_style='background-color:'+background_color
                    #td_style='background-color:'+background_color+';height:100%'
                    form_details[i].insert(j,TD('',_style=td_style))
                    if (j==0)|(j==6):
                        bt_c='lightblue'
                        td_c='lightorange'
                    else:
                        #bt_c='lightgreen'
                        bt_c='lightyellow'
                        #td_c='lightyellow'
                        td_c='yellow'
                    
                    if (day<1)|(day>ldaym):
                        day=''
                        display=''
                    else:
                        #msg+=str(date.year)+'/'+str(date.month)+'/'+str(day)
                        this_day=datetime.date (date.year,date.month,day)

                        if dic.has_key(this_day):
                            lend=len(dic[this_day])
                                                                        
                            #bt_h= h_hight/(lend+1)
                            bt_h= h_hight/(lend+1)
                            
                            for m in range(lend):
                                #text-align: left|right|center|justify
                                #msg+=color_items[int(request.vars.rs_type)]
                                #msg+=color_items[1]
                                if dic[this_day][m][5]:
                                    #bt_c1='red' #c_one#dans cas overlap   color_items[value_rs_type]
                                    bt_c1=color_items[dic[this_day][m][7]]
                                else:
                                    #bt_c1='orange'
                                    bt_c1=color_items[dic[this_day][m][7]]
                                if dic[this_day][m][6]:
                                    ft_c1='gray'
                                else:
                                    ft_c1='black'
                                #color: red
                                #style_bt='color: '+str(ft_c1)+';text-align: left;background-color:'+str(bt_c1)+';border-color: white;height:'+str(bt_h)+'em;'#;width:30em
                                style_bt='color: '+str(ft_c1)+';text-align: left;background-color:'+str(bt_c1)+';border-color: white;height:'+str(bt_h)+'em;'#;width:30em
                                style_td='background-color:'+str(td_c)+';height:'+str(bt_h)+'em;'#;width:30em
                                #'{:02d}:{:02d}-{:02d}:{:02d}'.format(1,2,3,4)
                                #valdis=str(dic[this_day][m][1].hour)+":"+str(dic[this_day][m][1].minute)+" - "+str(dic[this_day][m][2].hour)+":"+str(dic[this_day][m][2].minute)+".."+str(dic[this_day][m][4])+"."+str(dic[this_day][m][3])+". #"+str(dic[this_day][m][0])
                                #valdis=str(dic[this_day][m][1].hour)+":"+str(dic[this_day][m][1].minute)+"-"+str(dic[this_day][m][4])+""+str(dic[this_day][m][3])+". #"+str(dic[this_day][m][0])
                                #with username
                                #valdis='{:02d}:{:02d}-{:02d}:{:02d}'.format(dic[this_day][m][1].hour,dic[this_day][m][1].minute,dic[this_day][m][2].hour,dic[this_day][m][2].minute)+"-"+str(dic[this_day][m][4])+""+str(dic[this_day][m][3])+". #"+str(dic[this_day][m][0])

                                valdis='{:02d}:{:02d}-{:02d}:{:02d}'.format(dic[this_day][m][1].hour,dic[this_day][m][1].minute,dic[this_day][m][2].hour,dic[this_day][m][2].minute)+" "+str(dic[this_day][m][3])+". #"+str(dic[this_day][m][0])

                                #<input name="submitButton" id="submitButton" type="submit" value="Submit" onclick="this.disabled=true;this.form.submit();" />
                                #,_onDoubleClick="this.disabled = true" not work
                                #,_onClick="this.disabled = true" work
                                form_details[i][j].append((INPUT(_class='button_calendar',_type='submit' ,\
                                _value=valdis,_id=valdis,_name=valdis,_style=style_bt)))
                            #bt_h+= 10%(lend+1)
                            bt_h+= h_hight%(lend+1)
                                       
                            
                            #display=str(len(dic[this_day]))
                            #msg+=str(valdis)
                        else:
                            bt_h= h_hight
                        display=str(day)
                    
                    if str(today.day)==str(day):
                        font_color='red'
                    else:
                        font_color='blue'#white

                    #style_bt='background-color:'+str(bt_c)+';border-color:white;height:'+str(bt_h)+'em;'

                    style_bt='background-color:'+str(bt_c)+';border-color:white;color:'+font_color+';height:'+str(bt_h)+'em;'
                    #style_td='background-color:'+str(td_c)+';height:'+str(bt_h)+'em;'
                    #style_td='background-color:'+str(td_c)+';border-color:red;height:'+str(bt_h)+'em;'

                    #form_details[i][j].append(DIV(INPUT(_class='button_calendar',_type='submit',_value=display,_id=display,_name=display,_style=style_bt)))
                    form_details[i][j].append(DIV(INPUT(_class='button_calendar',_type='submit',_value=display,_id=display,_name=display,_style=style_bt)))


                    
                    k+=1 #for i>0
                    
        response.flash=msg
        #response.flash="12"

    else:
        response.flash=T('Please Do Just One Click!')
    response.flash=msg

    return dict(form=form,request=request,response=response)

@auth.requires(auth.has_membership(role='admin'))
def tables():
    menu_url=[]
    tables=["rs_object","rs_type","rs_details",]
    tables_title=["Groupe de calendrier","Type de calendrier","Calendrier",]
    i=0
    for table in tables:
        menu_url+=[(T(tables_title[i]), False, URL(f='tables',args=[table])),]
        i+=1

    response.menu += [(T("Tables"), False, '#', menu_url)]

    table = request.args(0) or 'rs_object'
    if not table in db.tables(): redirect(URL('error'))

    grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)
    response.flash = T(u'terminé')
    return dict(grid=grid)




def download():
    import os
    path=os.path.join(request.folder,'uploads',request.args[0])
    return response.stream(path)

