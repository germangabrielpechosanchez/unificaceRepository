# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

response.menu += [
    (T("Nomenclature pour des alias"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]), 
        (T("Alias des systèmes d’information"), False, URL( f='alias_si'),[]),
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
    elif (auth.has_membership(role='gestion_nomenclature')):
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_nomenclature_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_nomenclature_edit')):
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

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_nomenclature')|auth.has_membership(role='gestion_nomenclature_edit')|auth.has_membership(role='gestion_nomenclature_edit_add'))
def alias_si():
    response.menu+=[
        (T("Alias des systèmes d’information"), False, URL( f='alias_si'),[]),
        ]
    msg=""
    grid=""
    fields=[
        Field('system',label=T("Nom de l'application / SI"),requires=[IS_NOT_EMPTY(),IS_LOWER()],comment=T("Exemple: eclinibase. Identifie le système visé par cette alias, le simple nom du système, il peux être un système d'information client mais peux aussi être une système de gestion ou équipements interne à nos équipes.")),
        Field('role',label=T('Rôle'),default="app",requires=IS_IN_SET(["app","bd","int",])),
        #Field('role',label=T('Rôle'),comment=T("Juste deux premières lettres"),default="ap",requires=IS_IN_SET(["ap","bd","in",])),
        #Field('role_ext',label=T('##'),default="",requires=IS_IN_SET(["","01","02","03","05","06","07","08","09","10",])),
        Field('site',label=T('Site desservi'),default="cemtl",requires=IS_IN_SET(["hlhl","cemtl","hsco","pdi","hmr","lteas","icp","slsm",])),
        #Field('site',label=T('Site'),comment=T(""),default="ce",requires=IS_IN_SET(["hl","ce","hs","pd","hm","lt","ic","sl",])),
        Field('vocation',label=T('Vocation'),default="prod",requires=IS_IN_SET(["prod","ppro","dev","form","rel"])),
        Field('role_ext',label=T('##'),default="sans numéro",requires=IS_IN_SET(["sans numéro","01","02","03","05","06","07","08","09","10","11","12","13","14","15",]),comment=T("Si un serveur unique ne pas mettre de numéro")),
        #Field('vocation',label=T('Vocation'),comment=T(""),default="pr",requires=IS_IN_SET(["pr","pp","de","fo","te",])),
        Field('server_dns',label=T('Serveur DNS'),comment=T(""),default="cemtl.rtss.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",])),
        Field('host',label=T('Hôte cible'),comment=T("Par exemple: s03vwpr00088"),default="",requires=[IS_NOT_EMPTY(),IS_LOWER()]),
        Field('domain_target',label=T('Domaine cible'),default="cemtl.rtss.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",])),
    ]
    buttons=[
        TD(INPUT(_type="submit",_value="aperçu",_id="aperçu",_name="aperçu",_style="background-color:#0066ff")),
        TD(INPUT(_type="submit",_value="créer l'alias dans DNS",_id="créer l'alias dans DNS",_name="créer l'alias dans DNS",_style="background-color:#0066ff")),
    ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(9,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        if request.vars.role_ext<>"sans numéro":
            role_ext=request.vars.role_ext
        else:
            role_ext=""
        alias=(request.vars.system+"_"+request.vars.role+"_"+request.vars.site+"_"+request.vars.vocation+role_ext).lower()
        #alias2=(request.vars.system+"_"+request.vars.role[:2]+role_ext+"_"+request.vars.site[:2]+"_"+request.vars.vocation[:2]).lower()
        alias2=""
        host=(request.vars.host+"."+request.vars.domain_target).lower()

        if request.vars.has_key("créer l'alias dans DNS"):
            if (auth.has_membership(role='admin'))|(auth.has_membership(role='gestion_nomenclature')):
                import subprocess
                arg1=alias+"*"+host+"*"+request.vars.server_dns
                msg+=arg1

                ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_nomenclature\create_alias_si.ps1'
                p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output,error = p1.communicate()
                output=output.decode('utf-8', 'ignore')        
                db.ads_actions_tracking.insert(edit_by=auth_id,edit_time=now,actions=output)
                qry=(db.ads_actions_tracking.edit_by==session.auth.user.id)
                fields=[db.ads_actions_tracking.edit_time,db.ads_actions_tracking.actions]
                grid = SQLFORM.grid(qry,fields=fields,orderby=~db.ads_actions_tracking.id,maxtextlength=250,deletable=False,editable=False,create=False,details=False)

            else:
                msg+="Besoin votre login!"
                
        grid=XML("<h2>"+alias+"</br>"+alias2+"</br>"+host+"</h2>"+str(grid))
    response.flash=msg
    return dict(form=form,grid=grid)


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
