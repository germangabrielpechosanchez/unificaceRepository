# -*- coding: utf-8 -*-
import os,subprocess 
import datetime



now=datetime.datetime.now();today=datetime.date.today()
response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Gestion des absences"), False, '#', [
        (T('Calendrier'), False, URL( f='index'),[]),
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        ]),
    
    ]



###################################
#test pour hover

"""
<!DOCTYPE html>
<html>
<style>
#tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black;
}

#tooltip #tooltiptext {
    visibility: hidden;
    width: 220px;
    background-color: #004080;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px 0;

    /* Position the tooltip */
    position: absolute;
    z-index: 1;
}

#tooltip:hover #tooltiptext {
    visibility: visible;
}
</style>
<body style="text-align:center;">

<p>Move the mouse over the text below:</p>

<div id="tooltip">Hover over me
  <span id="tooltiptext"><p>Note that the position of the tooltip text isn't very good. Go back to the tutorial and continue reading on how to position the tooltip in a desirable way.</p></span>
</div>

<p>Note that the position of the tooltip text isn't very good. Go back to the tutorial and continue reading on how to position the tooltip in a desirable way.</p>

</body>
</html>

"""

###################################
    

#parameters

#this_object_group="INFRA"
#this_write_role='gestion_temps'

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_absence'))
#@auth.requires_login()


def index():
    #update_capacity_availability(int(request.vars.resource),begin.date())
    #rs=db(db.reservation.id>0).select(db.reservation.resources,db.reservation.time_begin)
    #for r in rs:
    #    update_capacity_availability(r.resources,r.time_begin)

    
    response.menu+=[
        (T('Calendrier'), False, URL( f='index'),[]),
        ]


    #this_object_group="OPERA ABSENCE"

    this_object_group=request.args(0) or "INFRA ABSENCE"
    if request.args(0):
        this_object_group=request.args(0).replace('_',' ')
    else:
        this_object_group="INFRA ABSENCE"

    ######################
    if (this_object_group=="INFRA ABSENCE"):
        has_acces=True
    elif (this_object_group=="OPERA ABSENCE")&(auth.has_membership(role='gestion_absence')|auth.has_membership(role='gestion_absence_read')):
        has_acces=True
    else:
        has_acces=False
    
    if has_acces:

        object_group_ids={"INFRA ABSENCE":1,"OPERA ABSENCE":2}
        
        #this_write_role='gestion_absence'
        
        #tbl_object=db((db.rs_object.is_active==True)).select(db.rs_object.id,db.rs_object.title)
        tbl_object=db((db.rs_object.object_group==this_object_group)).select(db.rs_object.id,db.rs_object.title)
        object_items=[]
        object_list=()
        for i in tbl_object:
            object_items+=[(i.title.upper(),i.id),]
            object_list+=(i.id,)
        #tbl_resources
        #tbl_resources=db(db.resources.is_active==True).select(db.resources.id,db.resources.title,orderby=db.resources.title)
        resources_ids=db(db.resource_group.team_id==object_group_ids[this_object_group])._select(db.resource_group.resources_id)
        tbl_resources=db((db.resources.is_active==True)&(db.resources.resources_id.belongs(resources_ids))).select(db.resources.id,db.resources.title,orderby=db.resources.title)
        resources_items=[("SELECTIONNER UN RESSOURCE",-2),("TOUS",-1)]
        for i in tbl_resources:
            resources_items+=[(i.title.upper(),i.id),]
        #rs_type
        tbl_type=db((db.rs_type.object_group==this_object_group)).select(db.rs_type.id,db.rs_type.title,db.rs_type.color)
        type_items=[]
        color_items={}
        for i in tbl_type:
            type_items+=[(i.id,i.title.upper()),]
            color_items[i.id]=i.color.lower()

            
        #msg=str(color_items)
        

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
                TD('',INPUT(_class='button_command',_type='submit',_value='actualiser',_id='actualiser',_name='actualiser',_style='background-color:#339FFF')),#green
                TD('',INPUT(_class='button_command',_type='submit',_value='aujourd\'hui',_id='aujourd\'hui',_name='aujourd\'hui',_style='background-color:#339FFF')),#green
                TD(LABEL("VUE GLOBALE ",INPUT(_type='checkbox',_class='my_label',_name='all_view',value=all_view_checked))),#all_view_checked
                TD(LABEL("VUE DÉTAILLÉE ",INPUT(_type='checkbox',_class='my_label',_name='detail_view',_value=False))),
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
        #autopostback():
        script = SCRIPT("""
                        $('document').ready(function(){
                            $('.to_submit').change(function(){
                                $('#this_form').append('<input type="hidden" name="load" value="on" />');
                                $('#this_form').submit();
                            });     
                        });
                        
                        """)
        form.attributes['_id'] = 'this_form'
        
        

        if form.accepts(request.vars,session):
            
            qdb=db.reservation
            
            #time=datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),int(time[11:13]),int(time[14:16]),0,0)
            #if not request.vars.date: request.vars.date=str(today)
            #date=request.vars.date
            #date=datetime.datetime(int(date[0:4]),int(date[5:7]),int(date[8:10]),0,0,0,0)


            if not request.vars.object: request.vars.object='1'
            if not request.vars.resource: request.vars.resource='-2'
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
            value_resource=request.vars.resource
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
                value_resource=1
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

            #if request.vars.has_key('actualiser')|request.vars.has_key('aujourd\'hui'):
            if request.vars.has_key('actualiser')|request.vars.has_key('aujourd\'hui')|(request.vars.load=="on"):
                if request.vars.has_key('aujourd\'hui'):
                    date=today
                    value_date=str(date)
                this_id=0
                value_resource=1
                #value_rs_type=1
                if (request.vars.resource=="-2")|(request.vars.resource=="-1"):
                    if request.vars.resource=="-1":
                        value_title='TOUS'
                        value_resource=-1
                    else:
                        value_title='BESOIN UN RESSOURCE'
                        value_resource=-2
                    value_description=''
                    value_hour_begin=9
                    value_minute_begin=0
                    value_hour_end=15
                    value_minute_end=0
                else:
                    r=db(db.resources.id==int(request.vars.resource)).select(db.resources.id,db.resources.title,db.resources.start_time,db.resources.end_time)[0]
                    value_resource=r.id
                    value_title=r.title
                    value_description=''
                    value_hour_begin=r.start_time.hour
                    value_minute_begin=r.start_time.minute
                    value_hour_end=r.end_time.hour
                    value_minute_end=r.end_time.minute
                    #msg=str(dir(r.start_time))
                    
                
            elif request.vars.has_key('créer'):
                #if ((begin>=now)&(begin<end))|auth.has_membership(role='gestion_absence'):
                if auth.has_membership(role='gestion_absence'):
                    absence=(end-begin).seconds/60
                    if absence>420:absence=420
                    rs=db.reservation.insert(\
                    rs_object=request.vars.object,\
                    resources=request.vars.resource,\
                    rs_type=request.vars.rs_type,\
                    title=request.vars.title[:999],\
                    description=request.vars.description[:3999],\
                    time_begin=begin,\
                    time_end=end,\
                    absence=absence,\
                    replace_id=0,\
                    edit_by=auth.user_id,\
                    edit_time=now,\
                    )
                    if rs:
                        have_new_record=True
                        this_record=rs
                        this_id=rs
                        #update_resources_availability
                        update_record_to_azure('reservation','azure_update','update',this_id)
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
                    #if (rs[0].time_begin>=now)&(begin>=now)&(begin<end)&(rs[0].replace_id==0)|auth.has_membership(role=this_write_role):
                    #if (rs[0].replace_id==0)|auth.has_membership(role=this_write_role):
                    if (rs[0].replace_id==0):
                        if (rs[0].edit_by==auth.user_id): #auth.has_membership(role='users_rs')|(rs[0].edit_by==auth.user_id)
                            absence=(end-begin).seconds/60
                            if absence>420:absence=420
                            rs=db.reservation.insert(\
                            rs_object=request.vars.object,\
                            resources=request.vars.resource,\
                            rs_type=request.vars.rs_type,\
                            title=request.vars.title[:999],\
                            description=request.vars.description[:3999],\
                            time_begin=begin,\
                            time_end=end,\
                            absence=absence,\
                            replace_id=0,\
                            edit_by=auth.user_id,\
                            edit_time=now,\
                            )
                            if rs:
                                have_new_record=True
                                update_record_to_azure('reservation','azure_update','update',rs)#update new
                                this_record=rs
                                old_id=this_id
                                rs=db(qdb.id==this_id).update(\
                                replace_id=rs,\
                                )
                                this_id=this_record
                                update_record_to_azure('reservation','azure_update','update',old_id)#update old
                                load=True
                                #msg+=str(this_id)
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
                    #if (rs[0].time_begin>=now)&(rs[0].replace_id==0)|auth.has_membership(role=this_write_role):
                    #if (rs[0].replace_id==0)|auth.has_membership(role=this_write_role):
                    if (rs[0].replace_id==0):
                        #if (rs[0].edit_by==auth.user_id): #auth.has_membership(role='users_rs')|(rs[0].edit_by==auth.user_id):
                        if True: #auth.has_membership(role='users_rs')|(rs[0].edit_by==auth.user_id):
                            this_record=this_id
                            rs=db(qdb.id==this_id).update(\
                                replace_id=-auth.user_id,\
                                )
                            update_record_to_azure('reservation','azure_update','update',this_id)
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
                            update_record_to_azure('reservation','azure_update','delete',this_id)
                            rs=db(qdb.id==this_id).delete()
                            if rs: msg+='One record has been deleted'
                        else:
                            msg+='Cannot delete a record that is older than 15 minutes or created by another user , Please use Cancel button!'
                    else:
                        msg+="To delete a record  the time must be in the future, Please use Cancel button!"
                else:
                    msg+="This record does not exist!"

            if request.vars.has_key('créer')|request.vars.has_key('modifier')|request.vars.has_key('annuler')|request.vars.has_key('supprimer'):
                update_resources_availability(int(request.vars.resource),begin.date())
                update_capacity_availability(int(request.vars.resource),begin.date())
                    
            if load:
                rs=db((qdb.id==this_id)).select(qdb.rs_object,\
                qdb.resources,\
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
                value_resource=str(rs[0].resources)
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

            #111 qdb=db.reservation
            this_month=date.month
            this_year=date.year
            if this_month==12:
                next_month=1
                next_year=this_year+1
            else:
                next_month=this_month+1
                next_year=this_year
            first_date=datetime.date(this_year,this_month,1)
            last_day=(datetime.date(next_year,next_month, 1)-first_date).days
            first_date=datetime.datetime(this_year,this_month,1,0,0,0)
            last_date=datetime.datetime(this_year,this_month,last_day,23,59,59)
            #(date(2012, 3, 1) - date(2012, 2, 1)).days
            #response.flash=first_date
            tqry=(qdb.time_begin>=first_date)&(qdb.time_end<=last_date)
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
            #tdb_set=tdb_set&(qry_view)&(qdb.rs_object==db.rs_object.id)&(qdb.edit_by==db.auth_user.id) #original
            tdb_set=tdb_set&(qry_view)&(qdb.rs_object==db.rs_object.id)&(qdb.edit_by==db.auth_user.id)&tqry
            #tdb_set=tdb_set&(qry_view)&(qdb.rs_object==db.rs_object.id)


                
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
                i=rs.reservation.time_begin.date()
                #strike_record
                if rs.reservation.replace_id<>0:
                    strike_record=True
                    #pdf_strike+=(rs.reservation.id,)
                    red_record=False
                else:
                    strike_record=False
                #red_record
                if not strike_record:
                    time_min=rs.reservation.time_begin
                    time_max=rs.reservation.time_end
                    red_rs=db((((qdb.time_begin>=time_min)&(qdb.time_begin<=time_max))|\
                                ((qdb.time_end>=time_min)&(qdb.time_end<=time_max))|\
                                ((qdb.time_begin<=time_min)&(qdb.time_end>=time_max)))&\
                                (qdb.replace_id==0)&(qdb.rs_object==int(request.vars.object))).count()
                    if red_rs>1:
                        red_record=True
                        #pdf_red+=(row['reservation']['id'],)
                    else:
                        red_record=False
                #end red record
                j=(rs.reservation.id,rs.reservation.time_begin,rs.reservation.time_end,rs.reservation.title,rs.auth_user.last_name,red_record,strike_record,rs.reservation.rs_type,)
                if dic.has_key(i):
                    dic[i]+=(j,)
                else:
                    dic[i]=(j,)
            #msg+=str(dic)
            #msg+=str(date)
            #msg+=str(begin)
            #msg+=str(end)
            
            st={'RESERVATION.ID':'#',\
                'RESERVATION.RS_TYPE':'TYPE',\
                'RESERVATION.TITLE':'AFFICHAGE',\
                'RESERVATION.DESCRIPTION':'DESCRIPTION',\
                'RESERVATION.TIME_BEGIN':'DÉBUT',\
                'RESERVATION.TIME_END':'FIN',\
                'RESERVATION.REPLACE_ID':'REF.',\
                'AUTH_USER.LAST_NAME':'UTILISATEUR',\
                'RESERVATION.EDIT_TIME':'MODIFIÉ',\
                }
            #TD(LABEL("VUE PAR ",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (k,v) in view.items()],_class='class_input',_name='view_by',_value=request.vars.view_by)),
            ##form[0][0].insert(6,TD(T('Begin:'),INPUT(_type='text',_class='date',_name='begin',_id='begin',value=value_begin,_size=10,requires=IS_DATE())))
            #form[0][0].insert(1,DIV(LABEL("DATE ",_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date',_id='date',value=value_date,_size=10,requires=IS_DATE())))#2 class _class="date input"
            #month_disp
            month_lst = ('	janvier', '	février', 'mars', 'avril', 'mai', 'juin', 'juillet','août', 'septembre', 'octobre', 'novembre', 'décembre')
            month_disp=(month_lst[date.month-1].upper())+" / "+str(date.year)
            #TD(LABEL("GROUPE DE CALENDRIER ",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (v,k) in object_items],_class='class_input',_name='object',_value=request.vars.object)),
            form[0][0].insert(0,TD(LABEL("GROUPE DE CALENDRIER",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (v,k) in object_items],_class='class_input',_name='object',value=request.vars.object)))#value_object
            form[0][0].insert(1,TD(LABEL(month_disp,_class='my_label'),INPUT(_type='text',_class='date class_input',_name='date',_id='date',value=value_date,_size=10,requires=IS_DATE())))#2 class _class="date input"
            form[0][0].insert(2,TD(LABEL("RESSOURCE",_class='my_label'),SELECT(*[OPTION(v,_value=k) for (v,k) in resources_items],_class='class_input',_name='resource',value=value_resource)))#value_resource request.vars.resource
            if form.element('select',_name='resource'):
                form.element('select',_name='resource').attributes['_class'] = 'to_submit'

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
                                    form_details[i].insert(j,TD(TEXTAREA(_type='text',_class='class_input',_name='title',value=value_title,_rows=1,_cols=30,_readonly='on')))
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
                                    #if (auth.has_membership(role='admin')|auth.has_membership(role='gestion_absence')):
                                    if (request.vars.resource<>'-2')&((auth.has_membership(role='admin')|auth.has_membership(role='gestion_absence'))):
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
                                    #valdis='{:02d}:{:02d}-{:02d}:{:02d}'.format(dic[this_day][m][1].hour,dic[this_day][m][1].minute,dic[this_day][m][2].hour,dic[this_day][m][2].minute)+"-"+str(dic[this_day][m][4])+""+str(dic[this_day][m][3])+". #"+str(dic[this_day][m][0])
                                    valdis='{:02d}:{:02d}-{:02d}:{:02d}'.format(dic[this_day][m][1].hour,dic[this_day][m][1].minute,dic[this_day][m][2].hour,dic[this_day][m][2].minute)+"-"+str(dic[this_day][m][3])+". #"+str(dic[this_day][m][0])

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
            #response.flash=str(len(rc))
            #response.flash=(first_date,last_date)

        else:
            #response.flash=T('Please Do Just One Click!')
            response.flash=T('Bienvenu!')
        
        

        #response.flash=str(update_record_to_azure('reservation','azure_update','update',3305))
        #response.flash=str(update_record_to_azure('reservation','azure_update','delete',3305))
        #response.flash=str(update_record_to_azure('reservation','azure_update','update',3304))
        """
        #tbl='rs_type' #for web azure has no problem
        #tbl='resources' #for web azure has no problem
        #tbl='rs_object' #for web azure has no problem
        tbl='reservation' #for web azure work 450/600
        rs=db(db[tbl]['id']>0).select(db[tbl].ALL,orderby=db[tbl]['id'])
        for r in rs:
            update_record_to_azure(tbl,'azure_update','update',r['id'])
        #response.flash=str(rs)
        """

        #rs=db((db.reservation.time_begin>datetime.datetime(2017,8,23))&(db.reservation.replace_id==0)).select()
        #response.flash=str(len(rc))
        #db(db.reservation.id>-100000).update(edit_by=1) #for azure edit_by=1 for all reservation
    
        #response.flash=date
        #response.flash=request.args(0)
    else:
        #no access
        #script=""
        #form="<h2> Vous avez"
        #https://unificace.cemtl.rtss.qc.ca/init/default/user/not_authorized
        #https://unificace.cemtl.rtss.qc.ca/init/default/user/login?_next=/init/gestion_affichage/index
        #https://unificace.cemtl.rtss.qc.ca/init/gestion_absence/index/OPERA%20ABSENCE# 
        #redirect(URL('default','user',args=["not_authorized",])) 
        redirect(URL(c='default',f='user',args=['login'],vars={"_next":"/init/gestion_absence/index/OPERA%20ABSENCE"}))

    return dict(script=script,form=form,request=request,response=response)

# update_record_to_azure('reservation','azure_update',110)
def update_record_to_azure(this_table,this_operation,this_oper_type,this_record_id):
    this_record=db(db[this_table].id==this_record_id).select()
    to_send=''
    if this_record:
        this_record=this_record[0].as_dict()
        if this_oper_type<>'delete':
            for i in this_record:
                this_field=this_record[str(i)]
                this_type=(str(type(this_field)).replace("<type '","")).replace("'>","")
                to_send+=str(i)+","+str(this_field)+","+this_type+";"
        else:
            to_send+="id,"+str(this_record['id'])+",long;"
    to_send+=this_table+","+this_operation+","+this_oper_type
    #arg1='number1,111111111111;reservation,azure_update,'
    #"""
    arg1= s=escape(to_send)
    ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_absence\unificace_to_azure.ps1'
    p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #output,error = p1.communicate()
    #output=descape(output)
    #"""

    #return output#arg1

def escape(arg1):
    #arg1=arg1.upper()
    arg1=arg1.replace("à","a")
    arg1=arg1.replace("â","a")
    arg1=arg1.replace("é","e")
    arg1=arg1.replace("ê","e")
    arg1=arg1.replace("è","e")
    arg1=arg1.replace("À","A")
    arg1=arg1.replace("Â","A")
    arg1=arg1.replace("É","E")
    arg1=arg1.replace("Ê","E")
    arg1=arg1.replace("È","E")
    arg1=arg1.replace(".","0_")
    arg1=arg1.replace(",","1_")
    arg1=arg1.replace(";","2_")
    arg1=arg1.replace('(',"3_")
    arg1=arg1.replace(')',"4_")
    arg1=arg1.replace(' ',"5_")
    arg1=arg1.replace('{',"6_")
    arg1=arg1.replace('}',"7_")
    arg1=arg1.replace("'","8_")
    arg1=arg1.replace(":","9_")
    arg1=arg1.replace("#","0-_")
    arg1=arg1.replace("@","1-_")
    return arg1
def descape(arg1):
    arg1=arg1.replace("0_",".")
    arg1=arg1.replace("1_",",")
    arg1=arg1.replace("2_",";")
    arg1=arg1.replace("3_",'(')
    arg1=arg1.replace("4_",')')
    arg1=arg1.replace("5_",' ')
    arg1=arg1.replace("6_",'{')
    arg1=arg1.replace("7_",'}')
    arg1=arg1.replace("8_","'")
    arg1=arg1.replace("9_",":")
    arg1=arg1.replace("0-_","#")
    arg1=arg1.replace("1-_","@")
    return arg1
    
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_absence'))
def tables():
    menu_url=[]
    tables=["rs_object","rs_type","reservation","resources",]
    tables_title=["Groupe de calendrier","Type de calendrier","Calendrier","Ressources",]
    i=0
    for table in tables:
        menu_url+=[(T(tables_title[i]), False, URL(f='tables',args=[table])),]
        i+=1

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    table = request.args(0) or 'rs_object'
    if not table in db.tables(): redirect(URL('error'))

    #grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,)
    grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=False)


    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)
    response.flash = T(u'terminé')
    return dict(grid=grid)

def update_resources_availability(this_resource,this_day):
    #no update for Didier et Marie-Claude
    if (this_resource<>48)&(this_resource<>52): #48=DG;52=MGR
        #fp,ma,sm
        if this_resource in (27,36,31):availability=600
        else:availability=1050

        ds=6-this_day.weekday()
        if not ds:ds=7
        this_end=this_day+datetime.timedelta(days=ds-1)
        this_begin=this_end-datetime.timedelta(days=6)
        this_begin=datetime.datetime(this_begin.year,this_begin.month,this_begin.day,0,0,0)
        this_end=datetime.datetime(this_end.year,this_end.month,this_end.day,23,59,59)
        qry=(db.reservation.resources==this_resource)&(db.reservation.time_begin>=this_begin)&(db.reservation.time_end<=this_end)&(db.reservation.replace_id==0)
        sum_absence=db.reservation.absence.sum()
        rs=db(qry).select(db.reservation.resources,sum_absence,groupby=db.reservation.resources)
        if rs:
            this_absence=rs[0][sum_absence]
            this_absence=availability-this_absence
        else:this_absence=0
        qry=(db.resources_availability.resources==this_resource)&(db.resources_availability.time_begin==this_begin)&(db.resources_availability.time_end==this_end)
        rs=db(qry).select(db.resources_availability.id)
        if this_absence:
            if rs:
                db(db.resources_availability.id==rs[0].id).update(bank=this_absence)
            else:
                db.resources_availability.insert(
                    resources=this_resource,
                    time_begin=this_begin,
                    time_end=this_end,
                    bank=this_absence,
                    )
        else:
            if rs:
                db(db.resources_availability.id==rs[0].id).delete()
    
        #return (this_begin,this_end,rs)
        #return (this_resource,this_begin,this_end)
        #return (this_resource,this_begin,this_absence)
    else:
        this_begin=this_day #just for return no error
    return (this_resource,this_begin)

def update_capacity_availability(this_resource,this_day):
    #no update for Didier et Marie-Claude
    if (this_resource<>48)&(this_resource<>52): #48=DG;52=MGR
        #fp,ma,sm
        #if this_resource in (27,36,31):availability=600
        #else:availability=1050
        availability=2100

        ds=6-this_day.weekday()
        if not ds:ds=7
        this_end=this_day+datetime.timedelta(days=ds-1)
        this_begin=this_end-datetime.timedelta(days=6)
        this_begin=datetime.datetime(this_begin.year,this_begin.month,this_begin.day,0,0,0)
        this_end=datetime.datetime(this_end.year,this_end.month,this_end.day,23,59,59)
        qry=(db.reservation.resources==this_resource)&(db.reservation.time_begin>=this_begin)&(db.reservation.time_end<=this_end)&(db.reservation.replace_id==0)
        sum_absence=db.reservation.absence.sum()
        rs=db(qry).select(db.reservation.resources,sum_absence,groupby=db.reservation.resources)
        if rs:
            this_absence=rs[0][sum_absence]
            this_absence=availability-this_absence
        else:this_absence=0
        qry=(db.capacity_availability.resources==this_resource)&(db.capacity_availability.time_begin==this_begin)&(db.capacity_availability.time_end==this_end)
        rs=db(qry).select(db.capacity_availability.id)
        if this_absence:
            if rs:
                db(db.capacity_availability.id==rs[0].id).update(bank=this_absence)
            else:
                db.capacity_availability.insert(
                    resources=this_resource,
                    time_begin=this_begin,
                    time_end=this_end,
                    bank=this_absence,
                    )
        else:
            if rs:
                db(db.capacity_availability.id==rs[0].id).delete()
    
        #return (this_begin,this_end,rs)
        #return (this_resource,this_begin,this_end)
        #return (this_resource,this_begin,this_absence)
    else:
        this_begin=this_day #just for return no error
    return (this_resource,this_begin)


      


    




def download():
    import os
    path=os.path.join(request.folder,'uploads',request.args[0])
    return response.stream(path)

