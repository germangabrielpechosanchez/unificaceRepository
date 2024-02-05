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

    (T("Gestion d'impression"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( 'index'), []),
        (T('Configuration'), False, URL( 'configuration'), []),
        (T('Gestion des accès au module'), False, URL( f='module_access_create'),[]),
        ]),    
    ]

groups_access=(1051,1051)
if auth.is_logged_in():
    if (auth.has_membership(role='admin')):
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_impression')):
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

try: 
    auth_id=session.auth.user.id
except:
    auth_id=1

def index():

    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( 'index'), []),
        ]
    #\\HLHL-apps.hlhl.rtss.qc.ca\Apps\Commun\echange\unificace_gestion_impression
    #\\s-print2\la-507-16-060020;\\s-print2\LA-507-00-054056
    #\\s-print2\LA-103-37-CIM00181;\\s-print2\CL-004-10-PRET

    return dict(grid="")

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_impression'))
#@auth.requires_login()
def configuration():
    response.menu+=[
        (T('Configuration'), False, URL( 'configuration'), []),
        ]

    grid = SQLFORM.grid(db.pdfs_printers,deletable=deletable,editable=editable,create=create,user_signature=user_signature,
                        maxtextlength=70,searchable=searchable,details=details,csv=False,buttons_placement = 'left',paginate=20,
                        )

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_impression_admin'))
def module_access_create():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Créer un accès'), False, URL(f='module_access_create'),[]),
    ]    
    grid=""    
    qry=(db.pre_user_to_group.group_id.belongs(groups_access))
    #qry=(db.auth_membership.group_id.belongs(groups_access))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_impression_admin'))
def module_access_edit():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
    ]    
    grid=""    
    #qry=(db.pre_user_to_group.group_id.belongs(groups_access))
    qry=(db.auth_membership.group_id.belongs(groups_access))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

def access_onvalidation(form):
    #form.vars.group_id
    if form.vars.group_id not in groups_access:
        rs=db(db.auth_group.id.belongs(groups_access)).select(db.auth_group.role)
        form.errors.group_id="Le groupe doit être dans cette liste: "+((str(rs).replace("auth_group.role","")).replace("gestion_impression",", gestion_impression"))
        form.errors= True
    return

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



