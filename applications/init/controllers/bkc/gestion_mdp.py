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
    #vp add
    #(T('Profil et Accès'), False, URL('default', 'index'), []),
    #(T('Profil'), False, URL('default', 'index'), []),
    #(T('Accès'), False, URL('default', 'index'), []),
    #(T('Base de données'), False, URL('default', 'index'), []),
    (T('Gestion mot de passe'), False, URL('gestion_mdp', 'index'), []),
    #(T('Octopus - Paramètres'), False, URL('default', 'index'), []),


]

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_mdp'))
def index():
    import subprocess 
    #from subprocess import Popen
    import os

    try: auth_id=session.auth.user.id
    except: auth_id=20
    
    ad_account=db(db.auth_user.id==auth_id).select()
    domain_user=(ad_account[0].username).split("@")
    arg1=domain_user[1]
    arg2=domain_user[0]
    if arg1=="hsco.net":
        groups={
            "Profil CEMTL":"g_proxy_toutouvert",
            "Profil Université de Montréal":"g_proxy_toutouvert_udm",
            }
    elif arg1=="hmr.hmr.qc.ca":
        groups={
            "Profil CEMTL":"g_proxy_toutouvert",
            "Profil Université de Montréal":"g_proxy_universitedemontreal",
            }
    elif arg1=="hlhl.rtss.qc.ca":
        groups={
            "Profil CEMTL":"g_proxy_toutouvert",
            "Profil Université de Montréal":"fortigate-udem",
            "Profil Université du Québec à Montréal":"fortigate-uqam",       
            }
    else:
        groups={}

    form = SQLFORM.factory(
        Field('prenom',label="Nom d'utilisateur : "+ad_account[0].username,default='',writable=False),#,writable=False
        buttons = []#[INPUT(_type='Submit', _name='submit1', _value='Submit1'),INPUT(_type='Submit', _name='submit2', _value='Submit2')]
        )
            


    for profil in groups: #(j,TD('',INPUT(_type='submit',_value='reset',_name='submit',_style='background-color:red')),)
        element=TR(TD(INPUT(_type='submit',_value=profil,_id=profil,_name=profil,_style='background-color:#339FFF')))#,_style='background-color:red'
        form[0].insert(5,element)
        
    if form.process().accepted:
        for profil in groups:
            if request.vars.has_key(profil):
                arg3=groups[profil]

        #arg3=groups[profil]
        script=r'C:\Users\admphav\unificatex\web2py\applications\init\scripts\gestion_proxy\gestion_proxy.ps1'#gestion_proxy.ps1
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1, arg2, arg3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p1.communicate()
        outputs=output.split("***")
        msg=""
        for out in outputs:
            msg+=out+"<br/><br/>"
        response.flash = XML(msg)
    elif form.errors:
        response.flash = 'form has errors'

    #response.flash = str(form)

    
    return dict(form=form,request=request)


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


