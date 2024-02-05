# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

response.menu = [
    (response.menu[0]),
    #(T('Accueil'), False, URL('default', 'index'), []),
    #(T('Octopus'), False, URL('gestion_octopus', 'index'), []),
    #(T('9 Domaines'), False, URL('gestion_ads', 'index'), []),
    #(T('Serveurs'), False, URL('gestion_serveurs', 'index'), []),
    #(T('Proxy'), False, URL('gestion_proxy', 'index'), []), 
    #(T('ADs-Mot de passe'), False, URL('gestion_mdp', 'index'), []),
    #(T('Gestion-Identité'), False, URL('gestion_identite', 'index'), []),
    #(T('Base de données'), False, URL('database', 'index'), []),
    #(T('About'), False, URL('about', 'index'), []),
]


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Bienvenue")
    return dict(message=T('Bienvenue CEMTL!'))

#auth.settings.allow_basic_login = True
#@auth.requires_login()
@request.restful()
def api():
    #session.forget()
    def GET(input):
        output=""
        #if auth.has_membership(role='group_api'):
        if True:
            input=input.replace('---','|')
            input=input.split('|')
            #upload ip---h---w---command---messages
            if len(input)>3:
                ip=input[0].replace("-",".")
                #lien_folder="file://"+ip+"\\pi\\tools"
                lien_folder="file://"+ip
                found=db(db.computer.ip==ip).select(db.computer.id,db.computer.command,db.computer.messages)
                if found:
                    #read command
                    output+=found[0].command+"***"
                    if input[3]!="":
                        new_message=input[3]+"_"+found[0].messages 
                    else:
                        new_message=found[0].messages
                    new_message=new_message[:1022]
                    db(db.computer.id==found[0].id).update(screen_height=int(input[1]),screen_width=int(input[2]),sync=request.now,command="",messages=new_message,links=lien_folder)
                else:
                    db.computer.insert(ip=ip,screen_height=int(input[1]),screen_width=int(input[2]),sync=request.now,command="",messages="",links=lien_folder)
            
        return output
        session.forget()
    return locals()


def api_org():
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


