# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
############################################### TEST DB TABLE ###############################################
"""
db.define_table('domains_security_group',
                Field('domain_id',db.domains,requires=IS_IN_DB(db,'domains.id','domains.fqdn'),label=T('Domaine'),default=2),
                Field('group_name',label=T('Nom de groupe de securité'),requires = IS_UPPER()),
                Field('description',label=T('Description de groupe de securité'),requires = IS_UPPER()),
               )
"""
############################################### TEST DB TABLE ###############################################
response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Gestion des VMs"), False, '#', [
        (T("Index"), False, URL( f='index'),[]),
        (T("CRÉATION D'UN SERVEUR"), False, URL( f='create_vm'),[]),
        (T('TABLES DE CONFIGURATION'), False, URL( f='tables'),[]),
        (T('SYCHRONISATION AVEC VCENTER'), False, URL( f='tables_update'),[]),
        ]),
    
    ]
if auth.is_logged_in():
    if (auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')):
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
        (T('Gestion des VMs'), False, URL( f='index'),[]),
        ]
    grid=""

    #response.flash = T(u'Bievenue au module de gestion des inventaires')

    grid="""
    <body>
    <table>	
        <ol class="tree">
            <li>
                <label for="folder1">Folder 1</label> <input type="checkbox" checked enabled id="folder1" /> 
                <ol>
                    <li class="file"><a href="document.html.pdf">File 1</a></li>
                    <li>
                        <label for="subfolder1">Subfolder 1</label> <input type="checkbox" id="subfolder1" /> 
                        <ol>
                            <li class="file"><a href="">Filey 1</a></li>
                            <li>
                                <label for="subsubfolder1">Subfolder 1</label> <input type="checkbox" id="subsubfolder1" /> 
                                <ol>
                                    <li class="file"><a href="">File 1</a></li>
                                    <li>
                                        <label for="subsubfolder2">Subfolder 1</label> <input type="checkbox" id="subsubfolder2" /> 
                                        <ol>
                                            <li class="file"><a href="">Subfile 1</a></li>
                                            <li class="file"><a href="">Subfile 2</a></li>
                                            <li class="file"><a href="">Subfile 3</a></li>
                                            <li class="file"><a href="">Subfile 4</a></li>
                                            <li class="file"><a href="">Subfile 5</a></li>
                                            <li class="file"><a href="">Subfile 6</a></li>
                                        </ol>
                                    </li>
                                </ol>
                            </li>
                            <li class="file"><a href="">File 3</a></li>
                            <li class="file"><a href="">File 4</a></li>
                            <li class="file"><a href="">File 5</a></li>
                            <li class="file"><a href="">File 6</a></li>
                        </ol>
                    </li>
                </ol>
            </li>
            <li>
                <label for="folder2">Folder 2</label> <input type="checkbox" id="folder2" /> 
                <ol>
                    <li class="file"><a href="">File 1</a></li>
                    <li>
                        <label for="subfolder2">Subfolder 1</label> <input type="checkbox" id="subfolder2" /> 
                        <ol>
                            <li class="file"><a href="">Subfile 1</a></li>
                            <li class="file"><a href="">Subfile 2</a></li>
                            <li class="file"><a href="">Subfile 3</a></li>
                            <li class="file"><a href="">Subfile 4</a></li>
                            <li class="file"><a href="">Subfile 5</a></li>
                            <li class="file"><a href="">Subfile 6</a></li>
                        </ol>
                    </li>
                </ol>
            </li>
            <li>
                <label for="folder3">Folder 3</label> <input type="checkbox" id="folder3" /> 
                <ol>
                    <li class="file"><a href="">File 1</a></li>
                    <li>
                        <label for="subfolder3">Subfolder 1</label> <input type="checkbox" id="subfolder3" /> 
                        <ol>
                            <li class="file"><a href="">Subfile 1</a></li>
                            <li class="file"><a href="">Subfile 2</a></li>
                            <li class="file"><a href="">Subfile 3</a></li>
                            <li class="file"><a href="">Subfile 4</a></li>
                            <li class="file"><a href="">Subfile 5</a></li>
                            <li class="file"><a href="">Subfile 6</a></li>
                        </ol>
                    </li>
                </ol>
            </li>
            <li>
                <label for="folder4">Folder 4</label> <input type="checkbox" id="folder4" /> 
                <ol>
                    <li class="file"><a href="">File 1</a></li>
                    <li>
                        <label for="subfolder4">Subfolder 1</label> <input type="checkbox" id="subfolder4" /> 
                        <ol>
                            <li class="file"><a href="">Subfile 1</a></li>
                            <li class="file"><a href="">Subfile 2</a></li>
                            <li class="file"><a href="">Subfile 3</a></li>
                            <li class="file"><a href="">Subfile 4</a></li>
                            <li class="file"><a href="">Subfile 5</a></li>
                            <li class="file"><a href="">Subfile 6</a></li>
                        </ol>
                    </li>
                </ol>
            </li>
            <li>
                <label for="folder5">Folder 5</label> <input type="checkbox" id="folder5" /> 
                <ol>
                    <li class="file"><a href="">File 1</a></li>
                    <li>
                        <label for="subfolder5">Subfolder 1</label> <input type="checkbox" id="subfolder5" /> 
                        <ol>
                            <li class="file"><a href="">Subfile 1</a></li>
                            <li class="file"><a href="">Subfile 2</a></li>
                            <li class="file"><a href="">Subfile 3</a></li>
                            <li class="file"><a href="">Subfile 4</a></li>
                            <li class="file"><a href="">Subfile 5</a></li>
                            <li class="file"><a href="">Subfile 6</a></li>
                        </ol>
                    </li>
                </ol>
            </li>
        </ol>
    </table>	
    </body>
    """
    
    grid='<body><table><ol class="tree">'
    #db(db.vms_folders.id>8416).delete()
    import time
    start_time = time.time()
    rs=db(db.vms_folders.id<8839).select(db.vms_folders.ALL,orderby=db.vms_folders.paths)#8839
    root=""
    roots=[]
    for r in rs:
        #r_paths=r.paths#.replace("|VM","")
        r_paths=r.paths.split("|")
        r_paths.remove("VM")
        r_paths="|".join(r_paths)
        while (root not in r_paths):
            root="|".join((root.split("|"))[:-1])
            roots+=[root,]
            grid+="</li></ol>"            
        if root=="":
            folders=r_paths.split("|")
            path_current=""
        else:
            folders=r_paths.split(root)[1].split("|")
            path_current=root
        count_folders=len(folders)
        last_folder=count_folders-1
        for i in range(1,count_folders):
            path_current+="|"+folders[i]
            if path_current not in root:
                root+="|"+folders[i]
                grid+="<ol><li>"
                id_folder=str(r.id)+'_'+str(i)
                grid+='<label for="'+id_folder+'">'+folders[i]+'</label> <input type="checkbox" checked enabled id="'+id_folder+'" />'
        grid+="<ol><li>"



    grid+='</ol></table></body>'
    
    response.flash=roots
    return dict(form="",grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')|auth.has_membership(role='gestion_vms_read'))
def create_vm():
    import random
    response.menu+=[
        (T("CRÉATION D'UN SERVEUR"), False, URL( f='create_vm'),[]),
        ]
    mac="52:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))    

    response.flash = mac
    return dict(grid="")

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms'))
def tables():
    menu_url=[]
    tables={"VMs dossiers":"vms_folders"}

    for table in tables.keys():
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    table = request.args(0) or 'vms_folders'
    if not table in db.tables(): redirect(URL('error'))
    grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=160,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms'))
def tables_update():
    grid =""
    #\\s03vwpr00031\Users\unificace\unificace\web2py\applications\init\scripts\gestion_vms\gestion_vms_folders_to_unificace.ps1
    # need to be on scheduled task 
    """
    import requests
    #http://unificace.cemtl.rtss.qc.ca:8080/gestion_vms_api.ps1?command=get_db&vcenter=s01vwpr00073.cemtl.rtss.qc.ca
    url="http://unificace.cemtl.rtss.qc.ca:8080/gestion_vms_api.ps1?command=get_vcenter_to_unificace"
    #url="http://unificace.cemtl.rtss.qc.ca:8080/gestion_vms_api.ps1"
    #outs=requests.get(url ,auth=(username, password),stream=True).content
    outs=(requests.get(url ,stream=True).content).decode('utf-8')
    #$out+="$path;$name;$id£"
    ins=outs.split('%')[1:]
    db(db.vms_folders.id>0).delete()
    for i in ins:
        c=i.split(';')
        if len(c)>=2:
            paths=c[0][:1023]
            folder_id=c[1]
            #datacenter_id=str(c[2])
            #try:
            rs=db(db.vms_folders.folder_id==c[1]).select(db.vms_folders.id)
            if rs:
                db(db.vms_folders.id==rs[0].id).update(paths=paths)
            else:
                db.vms_folders.insert(paths=paths,folder_id=folder_id)
            #except:
            #    pass
    response.flash = outs
    """
     
    return dict(form="",grid=grid)


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
