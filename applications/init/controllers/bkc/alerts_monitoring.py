# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


response.menu += [
    (T("Surveillance des alertes"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]), 
        (T("Surveillance GetDB - Octopus"), False, URL( f='alerts_octopus_bkc_by_request', args=['alerts_octopus_bkc_by_request',]),[]),
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        ]),    
    ]
import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()

if auth.is_logged_in():
    if (auth.has_membership(role='admin')):
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_alerts')):
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_alerts_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_alerts_edit')):
        create=False
        deletable=False
        editable=True
        user_signature=False
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
#@auth.requires_login()
def index():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        ]
    grid=""
    session.this_manager=False
    
    return dict(grid=grid)


#restfull api
auth.settings.allow_basic_login = True
@auth.requires_login()
@request.restful()
def alerts_octopus_bkc_by_request():
    def GET(input):
        output="have no access"
        start=str(now)
        if (auth.has_membership(role='gestion_alerts_monitoring'))&(input=="alerts_octopus_bkc_by_request"):
            file_name=r'\\s03VWPR00035.cemtl.rtss.qc.ca\GetDB\log2.txt'
            this_file=open(file_name, 'r')
            this_txt=this_file.read()
            this_file.close()
            filter_txt=str(today.month)+'/'+str(today.day)+'/'+str(today.year)
            #filter_txt=str(today.month)+'/30/'+str(today.year)
            this_txt=this_txt[this_txt.find(filter_txt):]
            find_txt="err"
            #find_txt="Completed"
            if (find_txt in this_txt)|(this_txt.find(filter_txt)==-1):#this_txt.find(filter_txt)==-1# can not found the date
                #send email
                if (now.hour==9)&(now.minute<6): #only after 5am
                    from gluon.tools import Mail
                    mail = Mail()
                    mail.settings.server = 'smtp.rtss.qc.ca:25'
                    mail.settings.sender = 'unificace@ssss.gouv.qc.ca'
                    #send_to="vphanalasy@ssss.gouv.qc.ca;kbellafrouh.hmr@ssss.gouv.qc.ca;axel.vercnocke.pdi@ssss.gouv.qc.ca"
                    #send_to="vphanalasy@ssss.gouv.qc.ca;vphanalasy@gmail.com"
                    #send_to="vphanalasy@ssss.gouv.qc.ca;kbellafrouh.hmr@ssss.gouv.qc.ca;axel.vercnocke.pdi@ssss.gouv.qc.ca;acamacho.hmr@ssss.gouv.qc.ca"
                    send_to="vphanalasy@ssss.gouv.qc.ca;vphanalasy@gmail.com"
                    send_to=send_to.split(';')
                    this_txt=this_txt.replace('octsys01','')
                    this_txt=this_txt.replace('Bonjour02','')
                    #message="Voici message erreurs sur "+file_name+" :"+this_txt
                    message="Voici message erreurs (test) sur "+file_name+" :"+this_txt
                    status=mail_send(
                        to=send_to,
                        subject='Alerts octopus GetDB',
                        reply_to='unificace@ssss.gouv.qc.ca',
                        message=message
                    )
                    if status:
                        actions=str(send_to)+" :"+message
                        db.ads_actions_tracking.insert(edit_by=1072,edit_time=now,actions=actions)#by unificace
                        msg=actions
                    output="2-CRITICAL"#CRITICAL	DOWN/UNREACHABLE
                else:
                    output="1-WARNING"
            else:
                output="0-OK"#OK	UP
                #https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/pluginapi.html

        script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\alerts_monitoring\log.txt'
        f=open(script,"a")
        f.write('\r\n'+start+"---"+str(output))
        f.close()                   
        return output
        session.forget()
    return locals()

def mail_send(to,subject,reply_to,message):
    from gluon.tools import Mail
    mail = Mail()
    mail.settings.server = 'smtp.rtss.qc.ca:25'
    #mail.settings.sender = 'unificace@ssss.gouv.qc.ca'
    mail.settings.sender = 'unificace@ssss.gouv.qc.ca'
    resend=True
    i=0
    while resend:
        i+=1
        status=mail.send(
            to=to,
            subject=subject,
            reply_to=reply_to,
            message=message
            )
        if status:
            resend=False
        elif i>10:
            resend=False
    return status

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_alerts')|auth.has_membership(role='gestion_alerts_edit')|auth.has_membership(role='gestion_alerts_edit_add'))
def thins_locations():
    response.menu+=[
    (T("Assigner / Désassigner des clients légers"), False, URL( f='thins_locations'),[]),
    ]
    qry=(db.gmi_thin_location.thin==db.gmi_thins.id)&(db.gmi_thin_location.locations==db.gmi_locations.id)
    fields=[db.gmi_thins.name,db.gmi_locations.name]#,db.gmi_thin_location.is_active
    orderby=db.gmi_thins.name
    grid = SQLFORM.grid(qry,fields=fields,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_alerts')|auth.has_membership(role='gestion_alerts_edit')|auth.has_membership(role='gestion_alerts_edit_add'))
def printers_locations():
    response.menu+=[
    (T("Assigner / Désassigner des imprimants"), False, URL( f='printers_locations'),[]),
    ]
    qry=(db.gmi_printers_locations.printer==db.gmi_printers.id)&(db.gmi_printers_locations.locations==db.gmi_locations.id)
    fields=[db.gmi_printers.name,db.gmi_locations.name,db.gmi_printers_locations.default_printer]#,db.gmi_thin_location.is_active
    orderby=db.gmi_printers.name
    grid = SQLFORM.grid(qry,fields=fields,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_alerts')|auth.has_membership(role='gestion_alerts_edit')|auth.has_membership(role='gestion_alerts_edit_add'))
def printers():
    response.menu+=[
    (T("Ajouter / Activer / Désactiver des imprimantes"), False, URL( f='printers'),[]),
    ]
    qry=db.gmi_printers
    #(db.gmi_printers_locations.printer==db.gmi_printers.id)&\
    #(db.gmi_thin_location.locations==db.gmi_locations.id)&\
    orderby=db.gmi_printers.name
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_alerts')|auth.has_membership(role='gestion_alerts_edit')|auth.has_membership(role='gestion_alerts_edit_add'))
def thins():
    response.menu+=[
    (T("Ajouter / Activer / Désactiver des Clients légers"), False, URL( f='thins'),[]),
    ]
    qry=db.gmi_thins
    orderby=db.gmi_thins.name
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_alerts')|auth.has_membership(role='gestion_alerts_edit')|auth.has_membership(role='gestion_alerts_edit_add'))
def locations():
    response.menu+=[
    (T("Emplacements"), False, URL( f='locations'),[]),
    ]
    qry=db.gmi_locations
    orderby=db.gmi_locations.name
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_alerts')|auth.has_membership(role='gestion_alerts_edit')|auth.has_membership(role='gestion_alerts_edit_add'))
def thins_printers():
    response.menu+=[
    (T("Vue client légers - imprimantes"), False, URL( f='thins_printers'),[]),
    ]       

    file_name='mappage_imprimantes_'+str(now).replace('.','').replace(':','').replace(' ','')+'.csv'
    this_file=open(file_name, 'w')
    qry=(db.gmi_thin_location.locations==db.gmi_printers_locations.locations)&\
        (db.gmi_thin_location.thin==db.gmi_thins.id)&\
        (db.gmi_printers_locations.printer==db.gmi_printers.id)&\
        (db.gmi_thin_location.locations==db.gmi_locations.id)&\
        (db.gmi_thins.is_active==True)&\
        (db.gmi_printers.is_active==True)&\
        (db.gmi_locations.is_active==True)

    fields=[db.gmi_thins.name,db.gmi_locations.name,db.gmi_printers.name,db.gmi_printers.url,db.gmi_printers_locations.default_printer]
    orderby=db.gmi_thins.name

    grid = SQLFORM.grid(qry,fields=fields,orderby=orderby,maxtextlength=70,deletable=False,editable=False,create=False,user_signature=user_signature,searchable=searchable,details=False)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_alerts')|auth.has_membership(role='gestion_alerts_edit')|auth.has_membership(role='gestion_alerts_edit_add'))
#@auth.requires(auth.has_membership(role='admin'))
def exportation():
    response.menu+=[
    (T("Exporter au script"), False, URL( f='exportation'),[]),
    ]       
    #import codecs
    path=r'\\cemtl.rtss.qc.ca\SysVol\cemtl.rtss.qc.ca\Policies\thins_printers'
    file_name= path+r'\thins_printers.txt'
    #this_file=codecs.open(file_name, 'w',"utf-8")
    this_file=open(file_name, 'w')
    qry=(db.gmi_thin_location.locations==db.gmi_printers_locations.locations)&\
        (db.gmi_thin_location.thin==db.gmi_thins.id)&\
        (db.gmi_printers_locations.printer==db.gmi_printers.id)&\
        (db.gmi_thin_location.locations==db.gmi_locations.id)&\
        (db.gmi_thins.is_active==True)&\
        (db.gmi_printers.is_active==True)

    rs=db(qry).select(db.gmi_thins.name,db.gmi_printers.url,db.gmi_printers_locations.default_printer,orderby=db.gmi_thins.name)

    line="thin,printer,default\n"
    this_file.write(line)
    total=0
    for r in rs:
        line=r.gmi_thins.name+","+r.gmi_printers.url+","+str(r.gmi_printers_locations.default_printer)+"\n"
        this_file.write(line)
    this_file.close()
    response.flash="Exportation est terminé"
    #redirect(URL('thins_printers'))   
    return dict(grid="")
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_alerts')|auth.has_membership(role='gestion_alerts_edit')|auth.has_membership(role='gestion_alerts_edit_add'))
def log_file():
    response.menu+=[
    (T("Historique"), False, URL( f='log_file'),[]),
    ]       
    #import codecs
    path=r'\\cemtl.rtss.qc.ca\SysVol\cemtl.rtss.qc.ca\Policies\thins_printers'
    file_name= path+r'\log.txt'
    #this_file=codecs.open(file_name, 'w',"utf-8")
    this_file=open(file_name, 'rb')
    grid=this_file.read()
    this_file.close()
    grid=grid.replace("\n","<br>")
    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin'))
def data_import():
    
    f= open(r'\\S03VWPR00031\Users\unificace\unificace\web2py\applications\init\scripts\gestion_imprimant\import.txt',"r")
    t=f.read()
    ts=t.split("\n")
    """
    db(db.gmi_printers).delete()
    #db.gmi_printers.truncate()
    for t in ts:
        tt=t.split("\\")
        name=tt[3].upper()
        url=t.upper()
        r=db((db.gmi_printers.name==name)&(db.gmi_printers.url==url)).select()
        if not r:
            db.gmi_printers.insert(name=name,url=url,description='',is_active=True)
    ###########
    db(db.gmi_locations).delete()
    #db.gmi_printers.truncate()
    for t in ts:
        #tt=t.split("\\")
        name=t.upper()
        #url=t.upper()
        r=db((db.gmi_locations.name==name)).select()
        if not r:
            db.gmi_locations.insert(name=name,description='',is_active=True)
    ##################
    #db(db.gmi_thins).delete()
    #db.gmi_printers.truncate()
    for t in ts:
        #tt=t.split("\\")
        name=t.upper()
        url=name
        r=db((db.gmi_thins.name==name)).select()
        if not r:
            db.gmi_thins.insert(name=name,url=url,description='',is_active=True)

    ###############
    for t in ts:
        tt=t.split(";")
        printer=tt[1].upper()
        locations=tt[0].upper()
        printer=db(db.gmi_printers.url==printer).select(db.gmi_printers.id)[0].id
        locations=db(db.gmi_locations.name==locations).select(db.gmi_locations.id)[0].id

        r=db((db.gmi_printers_locations.printer==printer)&(db.gmi_printers_locations.locations==locations)).select()
        if not r:
            db.gmi_printers_locations.insert(printer=printer,locations=locations,default_printer=False,is_active=True)
    
    error=()
    for t in ts:
        tt=t.split(";")
        thin=tt[0].upper()
        thi=thin
        locations=tt[1].upper()
        loc=locations
        thin=db(db.gmi_thins.name==thin).select(db.gmi_thins.id)[0].id
        try:
            locations=db(db.gmi_locations.name==locations).select(db.gmi_locations.id)[0].id
            r=db((db.gmi_thin_location.thin==thin)&(db.gmi_thin_location.locations==locations)).select()
            if not r:
                db.gmi_thin_location.insert(thin=thin,locations=locations,is_active=True)
        except:
            error+=((thi,loc),)
    
    for t in ts:
        printer=t.upper()
        printer=db(db.gmi_printers.name==printer).select(db.gmi_printers.id)[0].id
        r=db((db.gmi_printers_locations.printer==printer)).select(db.gmi_printers_locations.id)
        if r:
            db((db.gmi_printers_locations.id==r[0].id)).update(default_printer=True)
    """

    


    #response.flash=error
    return dict(grid="") 
    #redirect(URL('index'))    
    #return dict()
    


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
