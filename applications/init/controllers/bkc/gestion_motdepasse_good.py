# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()
######################################

######################################

response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Libre-service - Réinitialiser mon mot de passe"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        ]),
    
    ]


if auth.is_logged_in():
    if (auth.has_membership(role='admin')): #auth.has_membership(role='gestion_motdepasse_edit_add')
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_motdepasse')): #auth.has_membership(role='gestion_motdepasse_edit_add')
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_motdepasse_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_motdepasse_edit')):
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

#@auth.requires_login()
def index():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    grid=""

    rs=db(db.employees.email<>"").select()
    #db(db.employees.id>0).delete()
    #elimine 2016 doublon w/o email
    """
    i=0
    for r in rs:
        #fs=db((db.employees.email=="")&((db.employees.full_name==r.full_name)|((db.employees.first_name==r.first_name)&(db.employees.last_name==r.last_name)))).select()
        fs=db((db.employees.email=="")&((db.employees.full_name.like(r.full_name))|((db.employees.first_name.like(r.first_name))&(db.employees.last_name.like(r.last_name))))).select()
        for f in fs:
            db(db.employees.id==r.id).update(logon=r.logon+';'+f.logon)
            db(db.employees.id==f.id).delete()
            i+=1
    
    #elimine 4127 doublons w email
    i=0
    for r in rs:
        #fs=db((db.employees.email=="")&((db.employees.full_name==r.full_name)|((db.employees.first_name==r.first_name)&(db.employees.last_name==r.last_name)))).select()
        fs=db((db.employees.id<>r.id)&((db.employees.full_name.like(r.full_name))|((db.employees.first_name.like(r.first_name))&(db.employees.last_name.like(r.last_name))))).select()
        for f in fs:
            if r.email<>f.email:
                db(db.employees.id==r.id).update(email=r.email+';'+f.email,logon=r.logon+';'+f.logon)
            else:
                if f.employee_number<>"":employee_number=';'+f.employee_number
                else:employee_number=''
                if f.job_title<>"":job_title=';'+f.job_title
                else:job_title=''
                if f.phone_extesion<>"":phone_extesion=';'+f.phone_extesion
                else:phone_extesion=''
                if f.mobile_phone<>"":mobile_phone=';'+f.mobile_phone
                else:mobile_phone=''
                if f.office<>"":office=';'+f.office
                else:office=''
                db(db.employees.id==r.id).update(logon=r.logon+';'+f.logon,employee_number=r.employee_number+employee_number,job_title=r.job_title+job_title,phone_extesion=r.phone_extesion+phone_extesion,mobile_phone=r.mobile_phone+mobile_phone,office=r.office+office)
                i+=1
            db(db.employees.id==f.id).delete()
    
    i=0
    for r in rs:
        fs=db((db.employees.email=="")&((db.employees.full_name==r.full_name)|((db.employees.first_name==r.first_name)&(db.employees.last_name==r.last_name)))).select()
        #fs=db((db.employees.email=="")&((db.employees.full_name.like(r.full_name))|((db.employees.first_name.like(r.first_name))&(db.employees.last_name.like(r.last_name))))).select()
        for f in fs:
            if f.employee_number<>"":employee_number=';'+f.employee_number
            else:employee_number=''
            if f.job_title<>"":job_title=';'+f.job_title
            else:job_title=''
            if f.phone_extesion<>"":phone_extesion=';'+f.phone_extesion
            else:phone_extesion=''
            if f.mobile_phone<>"":mobile_phone=';'+f.mobile_phone
            else:mobile_phone=''
            if f.office<>"":office=';'+f.office
            else:office=''
            db(db.employees.id==r.id).update(logon=r.logon+';'+f.logon,employee_number=r.employee_number+employee_number,job_title=r.job_title+job_title,phone_extesion=r.phone_extesion+phone_extesion,mobile_phone=r.mobile_phone+mobile_phone,office=r.office+office)
            db(db.employees.id==f.id).delete()
            i+=1
    """
    

    
        
    #response.flash=i#len(rs)


    
    return dict(grid=grid)

@auth.requires_login()
def inscription():
    msg=""
    response.menu+=[
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    username=db(db.auth_user.id==auth_id).select()[0].username
    fields=[
        Field('account',label=T('Compte Windows'),default=username,writable=False),
        Field('domain',type='text',label=T('Domaine'),comment=T("Selectioner le domaine de ce compte"),default="hmr.hmr.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",],multiple=False)),
        Field('email',label=T('Courriel'),default='@ssss.gouv.qc.ca',requires = IS_EMAIL(error_message='Doit etre un courriel valide!'),comment=T("Ce corriel sera utiliser pour envoyer le mot de passe")),
    ]
    if session.confirmation_code:
        fields.insert(3,Field('confirmation_code',label=T('Code de confirmation'),comment=T("Entrer le code de confirmation que vous avez recu par ce courreil"),default=""))
    buttons=[
        TD(INPUT(_type='submit',_value='Inscrire au Libre-service',_id='Inscrire au Libre-service',_name='Inscrire au Libre-service',_style='background-color:#0066ff')),
    ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(5,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        #generate code
        if not session.confirmation_code:
            import random
            session.confirmation_code=random.randint(1001,9999)
        #send email
        if (not session.last_email_sent)|(session.last_email_sent<>request.vars.email):
            from gluon.tools import Mail
            mail = Mail()
            mail.settings.server = 'smtp.rtss.qc.ca:25'
            mail.settings.sender = 'unificace@ssss.gouv.qc.ca'
            status=mail_send(
                to=[request.vars.email,],
                subject='Code de confirmation du "Libre-service - Réinitialiser mon mot de passe"',
                reply_to='unificace@ssss.gouv.qc.ca',
                message='Utiliser ce code de confirmation de quatres chiffres pour finaliser votre inscription de inscrire votre compte au Libre-service - Code de confirmation: '+str(session.confirmation_code)
                )
            if status:
                msg+="Le code de confirmation a été envoyé. SVP consultez votre courriel pour finaliser votre inscription"
                session.last_email_sent=request.vars.email

        else:
            msg+="Le code de confirmation a deja envoyé. SVP consultez votre courriel pour finaliser votre inscription"
            #validation in AD


    response.flash =  msg
    return dict(form=form,grid="")

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse'))
def password_reset():
    response.menu+=[
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    grid=""
    msg=""
    fields=[
            Field('account',label=T('Compte Windows'),default="",requires=IS_NOT_EMPTY(),writable=True),
            Field('domain',type='text',label=T('Domaine'),comment=T("Selectioner le domaine de ce compte"),default="hlhl.rtss.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",],multiple=False)),
            Field('email',label=T('Courriel'),default='@ssss.gouv.qc.ca',requires = IS_EMAIL(error_message='Doit etre un courriel valide!'),comment=T("Ce corriel sera utiliser pour envoyer le mot de passe")),
    ]

    buttons=[
        TD(INPUT(_type='submit',_value='Recevoir mon mot de passe par couriel',_id='Recevoir mon mot de passe par couriel',_name='Recevoir mon mot de passe par couriel',_style='background-color:#0066ff')),
    ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(5,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        rs=db((db.employees.email.like('%'+request.vars.email+'%'))&(db.employees.logon.like('%'+request.vars.account+"@"+request.vars.domain+'%'))).select(db.employees.logon,db.employees.first_name,db.employees.last_name)
        if rs:
            import subprocess
            arg1=request.vars.account+"*"+request.vars.domain+"*"+request.vars.email

            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_motdepasse\gestion_motdepasse.ps1'
            p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output,error = p1.communicate()
            output=output.decode('utf-8', 'ignore')
            client_email=request.vars.email
            #save action      
            db.ads_actions_tracking.insert(edit_by=1072,edit_time=now,actions=client_email+";"+output)#by unificace
            #dispaly action
            qry=(db.ads_actions_tracking.actions.like('%'+client_email+'%'))
            fields=[db.ads_actions_tracking.edit_time,db.ads_actions_tracking.actions]
            grid = SQLFORM.grid(qry,fields=fields,orderby=~db.ads_actions_tracking.id,maxtextlength=250,deletable=False,editable=False,create=False,details=False)
            #send email
            output=output.split(';')
            status=False
            if output[2]=='done':
                status=mail_send(
                    to=[request.vars.email,],
                    subject='Libre-service - mon mot de passe',
                    reply_to='unificace@ssss.gouv.qc.ca',
                    message='Voici le mot de passe temporaire: '+str(output[1])
                )
            if status:
                msg+="Le mot de passe temporaire a été envoyé. SVP consultez votre courriel!"
        else:
            msg+="to do"
       
        
        response.flash =msg
    return dict(form=form,grid=grid)

def mail_send(to,subject,reply_to,message):
    from gluon.tools import Mail
    mail = Mail()
    mail.settings.server = 'smtp.rtss.qc.ca:25'
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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse'))
def tables():
    menu_url=[]
    tables={"Courriel -> Accès":"employees"}
    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]
    if request.args(0):
        table = request.args(0)
        grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    else:
        grid = ""
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
