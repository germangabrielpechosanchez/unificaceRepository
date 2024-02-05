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

    (T("À propos"), False, '#', [
        (T('À propos'), False, URL( f='index'),[]),
        (T("Guide d’introduction"), False, URL( f='guide'),[]),
        ("Serveur # "+request.env.local_hosts[0][-2:], False, URL( f='index'),[]),        
        ]),
    
    ]


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.menu+=[
        (T(''), False, URL( f='index'),[]),
        ] 
    #response.flash = request.env.local_hosts[0][-2:]
    return dict(message=T('Bienvenue CEMTL!'))
def guide():
    response.menu+=[
        (T("Guide d’introduction"), False, URL( f='guide'),[]),
        ] 
    return dict(message=T('Bienvenue CEMTL!'))


def  test():    
    content = """

        # My slides title
        ## Slide One
        this allows you to create slides using markmin
        ## Slide Two
        + you can use lists
        + you can use [[links http://www.google.com]]
        + you can use images [[image http://image.example.com center]]
    """
    import time
    t=9
    time.sleep(t)

    return content




auth.settings.allow_basic_login = True
@auth.requires_login()
@request.restful()
def api():
    def GET(s):
        return 'access granted, you said %s' % s
    return locals()


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


