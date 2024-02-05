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

    (T("Gestion des courriels"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T('Entrepôt des fichiers de courriels'), False, URL( f='import_file'),[]),
        (T("Entrepôt des fichiers d'attachement"), False, URL( f='email_attachment'),[]), 
        (T('Importation'), False, URL( f='importation'),[]),
        (T('Validation'), False, URL( f='validation'),[]),
        (T('Expédition'), False, URL( f='send_emails'),[]),
        (T('Expédition par bcc'), False, URL( f='send_emails_by_bcc'),[]),
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        ]),
    
    ]


if auth.is_logged_in():
    if (auth.has_membership(role='admin')): #auth.has_membership(role='gestion_courriels_edit_add')
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_courriels')): #auth.has_membership(role='gestion_courriels_edit_add')
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_courriels_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_courriels_edit')):
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
@auth.requires_login()
def index():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        ]
    grid=""
    """
    #good
    from gluon.tools import Mail
    mail = Mail()
    mail.settings.server = 'smtp.rtss.qc.ca:25'
    mail.settings.sender = 'vphanalasy@ssss.gouv.qc.ca'
    msg=mail.send(
        #to=['vphanalasy@gmail.com'],subject='hello',
        to=['vphanalasy@ssss.gouv.qc.ca','vphanalasy@gmail.com'],subject='hello_test',
        # If reply_to is omitted, then mail.settings.sender is used
        #reply_to='vphanalasy@ssss.gouv.qc.ca',
        reply_to='vphanalasy@ssss.gouv.qc.ca',
        message='Bonjour my test'
        )
    response.flash = msg
    """
    #db(db.emails_records.id>0).delete()

    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels'))
def import_file():
    response.menu+=[
        (T('Entrepôt des fichiers de courriels'), False, URL( f='import_file'),[]),
        ]
    grid = SQLFORM.grid(db.emails_file,orderby=~db.emails_file.dates,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels'))
def email_attachment():
    response.menu+=[
        (T("Entrepôt des fichiers d'attachement"), False, URL( f='email_attachment'),[]),
        ]
    grid = SQLFORM.grid(db.emails_attachments,orderby=~db.emails_attachments.dates,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels')|auth.has_membership(role='gestion_courriels_edit')|auth.has_membership(role='gestion_courriels_edit_add'))
def importation():
    response.menu+=[
        (T('Importation'), False, URL( f='importation'),[]),
        ]
    fs=db(db.emails_file.imported==False).select(db.emails_file.id,db.emails_file.file_data)
    msg=""
    i=0
    for f in fs:
        #db(db.emails_file.id==f.id).update(imported=True)
        ls=f.file_data.split('\r\n')
        ls0=ls[0].split('\t')
        ls=ls[1:]
        #check invoice# date and lenght>53
        can_import=False
        if len(ls0)>=7:
            if ls0[6]=='messages':
                can_import=True
        if can_import:
            db(db.emails_file.id==f.id).update(dates=now,imported=True)
            #Cleaning this invoice
            db((db.emails_records.emails_file==f.id)).delete()
            #db.commit()
            for l in ls:
                if l<>"":
                    cs=l.split('\t')

                    recipient=cs[0]
                    cc=cs[1]
                    bcc=cs[2]
                    subject=cs[3]
                    attachments=cs[4]
                    reply_to=cs[5]
                    messages=cs[6]
                    created=now
                    sent=datetime.datetime(3000,1,1)
                    emails_file=f.id

                    db.emails_records.insert(
                        recipient=recipient,
                        cc=cc,
                        bcc=bcc,
                        subject=subject,
                        attachments=attachments,
                        reply_to=reply_to,
                        messages=messages,
                        created=created,
                        sent=sent,
                        emails_file=emails_file,
                    )

                    #response.flash = len(cs)
               

    redirect(URL('validation'))
    #response.flash = ls0[6]
    return dict()
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels')|auth.has_membership(role='gestion_courriels_edit')|auth.has_membership(role='gestion_courriels_edit_add'))
def validation():
    response.menu+=[
        (T('Validation'), False, URL( f='validation'),[]),
        ]
    qry=db.emails_records
    orderby=~db.emails_records.sent
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels'))
def send_emails():
    response.menu+=[
        (T('Expédition'), False, URL( f='send_emails'),[]),
        ]
    import os
    from gluon.tools import Mail
    mail = Mail()
    mail.settings.server = 'smtp.rtss.qc.ca:25'
    #mail.settings.sender = 'vphanalasy@ssss.gouv.qc.ca'
    mail.settings.sender = 'migration.outlook.cemtl@ssss.gouv.qc.ca'
    fs=db(db.emails_attachments.to_send==True).select()

    attachments=[]
    attachments_string=[]
    path=r'\\S03VWPR00031\Users\unificace\unificace\web2py\applications\init\uploads\\'
    for f in fs:
        attachments_name=escape(f.description)
        attachments+=[mail.Attachment(path+str(f.files)),]
        attachments_string+=[attachments_name,]

    rs=db(db.emails_records.sent==datetime.datetime(3000,1,1)).select()
    for r in rs:
        recipient=[str(r.recipient)]
        cc=[r.cc]
        bcc=[r.bcc]
        subject=str(r.subject)
        #attachments=[r.attachments]
        reply_to=str(r.reply_to)
        messages=str(r.messages).replace('"','')
        resend=True
        i=0
        while resend:
            i+=1       
            status=mail.send(
                to=recipient,
                #to=['vphanalasy@ssss.gouv.qc.ca'],
                #cc=cc,
                #bcc=bcc,
                subject=subject,
                attachments=attachments,
                #reply_to='vphanalasy@ssss.gouv.qc.ca',
                reply_to=reply_to,
                message=messages
            )
            if status:
                resend=False
                db(db.emails_records.id==r.id).update(sent=now,attachments=str(attachments_string))
            elif i>5:
                resend=False                
    #response.flash = str(attachments)
    redirect(URL('validation'))    
    return dict(grid="")

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels'))
def send_emails_by_bcc():
    response.menu+=[
        (T('Expédition'), False, URL( f='send_emails'),[]),
        ]
    import os
    from gluon.tools import Mail
    mail = Mail()
    mail.settings.server = 'smtp.rtss.qc.ca:25'
    #mail.settings.sender = 'vphanalasy@ssss.gouv.qc.ca'
    mail.settings.sender = 'migration.outlook.cemtl@ssss.gouv.qc.ca'
    fs=db(db.emails_attachments.to_send==True).select()

    attachments=[]
    attachments_string=[]
    path=r'\\S03VWPR00031\Users\unificace\unificace\web2py\applications\init\uploads\\'
    for f in fs:
        attachments_name=escape(f.description)
        attachments+=[mail.Attachment(path+str(f.files)),]
        attachments_string+=[attachments_name,]

    rs=db(db.emails_records.sent==datetime.datetime(3000,1,1)).select()
    bcc=[]
    c=0
    for r in rs:
        if c==0:
            recipient=[str(r.recipient)]
            #recipient=[]
            #bcc+=[str(r.recipient),]
            #cc=[r.cc]
            #bcc=[r.bcc]
            subject=str(r.subject)
            reply_to=str(r.reply_to)
            messages=str(r.messages).replace('"','')
            resend=True
        else:
            bcc+=[str(r.recipient),]
        c+=1
    if True:
        i=0
        while resend:
            i+=1       
            status=mail.send(
                to=recipient,
                bcc=bcc,
                subject=subject,
                attachments=attachments,
                reply_to=reply_to,
                message=messages
            )
            if status:
                resend=False
                db(db.emails_records.sent==datetime.datetime(3000,1,1)).update(sent=now,attachments=str(attachments_string))
            elif i>5:
                resend=False                
    #response.flash = str(attachments)
    redirect(URL('validation'))    
    return dict(grid="")
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
    return arg1
    
#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_courriels')|auth.has_membership(role='gestion_courriels_edit')|auth.has_membership(role='gestion_courriels_edit_add'))
def tables():
    menu_url=[]
    #tables=["account_department","client_departments","manager_to_account","emails_file","invoices"]
    #tables={"Départements":"account_department","Clients":"client_departments","Gestionaires":"managers_to_account","Fichiers de facture":"emails_file","Factures":"invoices"}
    tables={"Fichiers des courriels":"emails_file","Fichiers d'attachements":"emails_attachments","Historique des courriets":"emails_records"}

    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    #table = request.args(0) or 'emails_file'
    table = request.args(0) or 'emails_records'
    if not table in db.tables(): redirect(URL('error'))
    grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    #response.flash = T(u'terminé')
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
