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

    (T("Mappage lecteur réseau"), False, '#', [
        (T('Mappage executable'), False, URL( 'index'), []),
        (T('Mappage configuration'), False, URL( 'mappage_config'), []),
        (T("Historique"), False, URL( f='log_file'),[]),
        (T('Exporter au fichier CSV'), False, URL( 'mappage_export'), []),
        (T('Gestion des accès au module'), False, URL( f='module_access_create'),[]),
        ]),
    
    ]

groups_access=(5,1050)
#@auth.requires(auth.has_membership(role='admin'))
#@auth.requires_login()
def index():

    response.menu+=[
        (T('Mappage executable'), False, URL( 'index'), []),
        ]
    #https://unificace/init/database/index/archives/archives/download/archives.files.ad318c5e477bf178.6d6170706167652e657865.exe?_signature=d6df283ab55a0ab81af88f44838bf864b118d42b
    #redirect(URL('index', args=(1,2,3), vars=dict(a='b')))
    

    if auth.has_membership(role='admin'):
        create=True
        deletable=True
        editable=True
        user_signature=True
        searchable=True
        details=True
    else:
        create=False
        deletable=False
        editable=False
        user_signature=False
        searchable=False
        details=False
        

    grid = SQLFORM.grid(db.archives,deletable=deletable,editable=editable,create=create,user_signature=user_signature,maxtextlength=150,searchable=searchable,details=details,
    #showbuttontext=False,
    #fields = [db.auth_user.first_name,db.auth_user.last_name,db.archives.descriptions,db.archives.publishing,db.archives.contents,],
    fields = [db.archives.archives,db.archives.files],#db.archives.user_id,
    csv=False,field_id=db.archives.id,
    )
    #response.flash = str(grid)
    #response.flash = str(auth.has_membership(role='user'))
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_mappage'))
#@auth.requires_login()
def mappage_config():
    response.menu+=[
        (T('Mappage configuration'), False, URL( 'mappage_config'), []),
        ]
    #https://unificace/init/database/index/archives/archives/download/archives.files.ad318c5e477bf178.6d6170706167652e657865.exe?_signature=d6df283ab55a0ab81af88f44838bf864b118d42b
    #redirect(URL('index', args=(1,2,3), vars=dict(a='b')))
    

    if auth.has_membership(role='admin'):
        create=True
        deletable=True
        editable=True
        user_signature=True
        searchable=True
        details=True
    else:
        create=True
        deletable=False
        editable=True
        user_signature=True
        searchable=True
        details=False
        
        
    #links = [lambda row: A('CLONE',_href=URL(f="mappage_clone",args=[row.id])),]
    #links =links,
    grid = SQLFORM.grid(db.mappage,deletable=deletable,editable=editable,create=create,user_signature=user_signature,
                        maxtextlength=70,searchable=searchable,details=details,csv=False,buttons_placement = 'left',paginate=400,
                        )
    #response.flash = str(auth.has_membership(role='user'))
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_mappage'))
#@auth.requires_login()
def mappage_export():
    #import codecs
    response.menu+=[
        (T('Exporter au fichier CSV'), False, URL( 'mappage_export'), []),
        ]
    maps=db(db.mappage.id>0).select()
    this_file=r'\\hlhl-apps.hlhl.rtss.qc.ca\Apps\Commun\echange\logonPE162\logonPE16.txt'
    #this_file=r'\\10.129.64.58\Apps\Commun\echange\logonPE162\logonPE16.txt'
    #.decode('utf-8', 'ignore')
    #f=codecs.open(this_file,'w',encoding='utf8') #f=open(this_file,'w')
    #f=open(this_file,'r+')
    f=open(this_file,'w')#w
    line="newDomaine"+','+"newUsername"+','+"oldDomaine"+','+"OldUsername"+','+"message"+','+"OldShare1"+','+"OldShare2"+','+"OldShare3"+','+"OldShare4"+','+"OldShare5"+','+"OldShare6"+','+"OldShare7"+'\n'
    #line=line.decode('utf-8', 'ignore')
    #f.write(line)
    for i in maps:
        #i.OldShare7=(i.OldShare7).replace("\n","")
        #i.OldShare7=(i.OldShare7).replace("\r","")
        #i.OldShare7=""
        line+=i.newDomaine+','+i.newUsername+','+i.oldDomaine+','+i.OldUsername+','+i.messages+','+i.OldShare1+','+i.OldShare2+','+i.OldShare3+','+i.OldShare4+','+i.OldShare5+','+i.OldShare6+','+i.OldShare7+'\n'
        #line=line.decode('utf-8', 'ignore')
        #f.write(line)<
    f.write(line)
    f.close()
    
    response.flash = T('Le fichier logonPE16.txt a été mis à jour')
    #response.flash = str(len(maps))
    return dict(grid='')

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_mappage'))
def log_file():
    response.menu+=[
    (T("Historique"), False, URL( f='log_file'),[]),
    ]       
    #import codecs
    path=r'\\hlhl-apps.hlhl.rtss.qc.ca\Apps\Commun\echange\logonPE162'
    file_name= path+r'\EventLog.txt'
    #this_file=codecs.open(file_name, 'w',"utf-8")
    this_file=open(file_name, 'rb')
    grid=this_file.read()
    this_file.close()
    grid=grid.replace("\n","<br>")
    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_mappage_admin'))
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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_mappage_admin'))
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
        form.errors.group_id="Le groupe doit être dans cette liste: "+((str(rs).replace("auth_group.role","")).replace("gestion_mappage",", gestion_mappage"))
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



