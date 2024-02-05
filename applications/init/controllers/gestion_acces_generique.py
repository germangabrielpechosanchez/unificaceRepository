# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


response.menu += [
    (T("Gestion des accès générique"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]), 
        (T("Accès générique"), False, URL( f='account_generique'),[]),
        (T("Mise à jour manuel"), False, URL( f='status_update'),[]),
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
    elif (auth.has_membership(role='gestion_acces_generique')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_acces_generique_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_acces_generique_edit')):
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
    session.this_manager=False
    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_acces_generique')|auth.has_membership(role='gestion_acces_generique_edit')|auth.has_membership(role='gestion_acces_generique_edit_add'))
def account_generique():
    response.menu+=[
        (T("Accès générique"), False, URL( f='account_generique'),[]),
    ]
    qry=(db.account_generique.id>0)
    orderby=db.account_generique.name
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=140,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_acces_generique')|auth.has_membership(role='gestion_acces_generique_edit')|auth.has_membership(role='gestion_acces_generique_edit_add'))
def status_update():
    response.menu+=[
        (T("Mise à jour manuel"), False, URL( f='status_update'),[]),
    ]
    import subprocess 
    grid=""
    script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_acces_generique\reset_auto_password.ps1'
    p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,error = p1.communicate()
    redirect(URL('account_generique')) 


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
