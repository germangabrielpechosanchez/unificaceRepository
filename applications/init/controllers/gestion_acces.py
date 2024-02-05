# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


@auth.requires(auth.has_membership(role='admin'))
def index():
    
    menu_url=[]    
    tables={"Utilisateurs":"auth_user","Groupes":"auth_group","Utilisateurs aux groupes":"auth_membership","Activités":"auth_event","Acces programmé":"pre_user_to_group"}

    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='index',args=[tables[table]])),]

    response.menu += [(T("Gestion des accès"), False, '#', menu_url)]

    #table = request.args(0) or 'invoice_file'
    table = request.args(0) or 'pre_user_to_group'
    if not table in db.tables(): redirect(URL('error'))

    #grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,)
    grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)

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


