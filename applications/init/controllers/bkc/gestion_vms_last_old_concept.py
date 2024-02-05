# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
############################################### TEST DB TABLE ###############################################

############################################### TEST DB TABLE ###############################################
response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Gestion des VMs"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T("Gestion des VMs"), False, URL( f='vms_management'),[]),
        (T('TABLES DE CONFIGURATION'), False, URL( f='tables'),[]),
        (T('SYCHRONISATION MANUELLE AVEC VCENTER'), False, URL( f='tables_update'),[]),
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

@auth.requires_login()
def index():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        ]
    grid=""
    session.this_manager=False
    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')|auth.has_membership(role='gestion_vms_read'))
def vms_management():
    response.menu+=[
        (T("Vu standard"), False, URL( f='vms_management'),[]),
        (T("Vu CTRL+F"), False, URL( f='vms_management',args=["ctrlf",]),[]),
        ]
    msg=""
    first_arg=request.args(0) or None
    ctrlf=False
    goto_folder_path=""
    if first_arg:
        if first_arg=="ctrlf":
            ctrlf=True
            checked_enabled="checked enabled"
        elif first_arg[:11]=="gotofolderx":
            goto_folder_id=int(first_arg[11:])
            rs=db(db.vms_folders.id==goto_folder_id).select()
            if rs:
                goto_folder_path=rs[0].paths.split("|")
                goto_folder_path.remove("VM")
                goto_folder_path="|".join(goto_folder_path)
                msg+=goto_folder_path               
    grid=""       
    grid='<body><table><ol class="tree">'
    import time
    start_time = time.time()
    rs=db(db.vms_folders.id>0).select(db.vms_folders.ALL,orderby=db.vms_folders.paths)#<8839
    root=""
    level=0
    for r in rs:
        r_paths=r.paths.split("|")
        if r_paths[1]=="VCENTER CITRIX":solution_level=6
        else:solution_level=4
        r_paths.remove("VM")
        r_paths="|".join(r_paths)
        while (root not in r_paths):
            root="|".join((root.split("|"))[:-1])
            grid+="</li></ol>"
            level-=1
        
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
            level+=1
            if path_current not in root:
                root+="|"+folders[i]
                grid+="<ol><li>"
                id_folder=str(r.id)+'_'+str(level)
                if not ctrlf:
                    if (level==1):
                        checked_enabled="checked enabled"
                    else:
                        checked_enabled=""
                    #open goto_folder_path
                    if path_current in goto_folder_path:
                        checked_enabled="checked enabled"
                    if goto_folder_path==path_current:
                        folders_display="<u><i>"+folders[i]+"</i></u>"
                    else:
                        folders_display=folders[i]
                else:
                    folders_display=folders[i]
                                                        
                if (level==solution_level)&(r.types=="Folder"):
                    grid+='<div class="dropdown"><label class="dropbtn" for="'+id_folder+'">'+folders_display+'</label><div class="dropdown-content"><a href="https://'+request.env.http_host+'/init/gestion_vms/add_solution/'+r.folder_id+'">Ajouter solution</a></div></div><input type="checkbox" '+checked_enabled+' id="'+id_folder+'" />'
                elif (level==solution_level+1)&(r.types=="Folder"):
                    grid+='<div class="dropdown"><label class="dropbtn1" for="'+id_folder+'">'+folders_display+'</label><div class="dropdown-content"><a href="https://'+request.env.http_host+'/init/gestion_vms/get_vm_data/'+r.folder_id+'">Créer serveur</a></div></div><input type="checkbox" '+checked_enabled+' id="'+id_folder+'" />'
                elif r.types=="Folder":
                    grid+='<label for="'+id_folder+'">'+folders_display+'</label> <input type="checkbox" '+checked_enabled+' id="'+id_folder+'" />'
                else:
                    #<li class="file"><a href="">File 1</a></li>
                    grid+='<li><div class="dropdown"><div class="dropbtn2">'+folders_display+'</div><div class="dropdown-content"><a href="https://'+request.env.http_host+'/init/gestion_vms/modify_vm/'+r.folder_id+'">Modifier ce VM</a></div></div></li>'

                    
    while (path_current <> ""):
        path_current="|".join((path_current.split("|"))[:-1])
        grid+="</li></ol>"

    grid+='</ol></table></body>'
    grid=grid.replace("</ol><ol>","")

    response.flash=msg
    return dict(form="",grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')|auth.has_membership(role='gestion_vms_read'))
def get_vm_data():
    import requests,random
    api_port=str(random.randint(8811,8813))
    vcenter_folder=request.args(0) or '_'
    vcenter_folder=vcenter_folder.split('_')
    vcenter=vcenter_folder[0]
    folder=vcenter_folder[1]
    #
    rs=db(db.vms_folders.folder_id==vcenter+"|"+folder).select()
    if rs:
        this_paths=rs[0].paths
    else:
        this_paths=""

    #url="http://'+request.env.http_host+':8080/gestion_vms_api.ps1?command=get_vm_data&vcenter="+vcenter+"&folder="+folder #with PoSHServer not solide
    #http://'+request.env.http_host+':8080/gestion_vms_api.ps1?command=get_vm_data&vcenter=s03vwpr00002.cemtl.rtss.qc.ca&folder=group-v113748

    url="http://"+request.env.http_host+":"+api_port+"/get_vm_data/"+vcenter+"/"+folder
    #http://'+request.env.http_host+':"+api_port+"/get_vm_data/s03vwpr00002.cemtl.rtss.qc.ca/group-v182596
    #outs=requests.get(url ,auth=(username, password),stream=True).content
    outs=requests.get(url,stream=True).content
    outs=outs.split("|")
    templates_id=outs[3].split(";")
    templates_name=outs[4].split(";")
    templates=[("windows_no_template","Windows sans template"),("linux_no_template","Linux sans template")]
    #for i in range(len(templates_id)):templates+=[(templates_id[i],templates_name[i]),]
    for i in range(len(templates_id)):templates+=[(templates_name[i],templates_name[i]),]
    vlans_id=outs[5].split(";")
    vlans_name=outs[6].split(";")  
    vlans=[("no_vlan","Sans VLAN")]
    #for i in range(len(vlans_id)):vlans+=[(vlans_id[i],vlans_name[i]),]
    for i in range(len(vlans_id)):vlans+=[(vlans_name[i],vlans_name[i]),]
    datacenter_id=outs[7]
    datacenter=outs[8]
    domain=outs[1]
    environment=outs[9] 
    solution=outs[2]
    datacenter_solution=datacenter+" - "+domain+" - "+environment+" - "+solution
    fields=[
        Field('datacenter_solution',label=T('Datacenter - Domaine - Environnement - Solution'),default=datacenter_solution,writable=False),
        Field('template',type='text',label=T('Template'),default="",requires=IS_IN_SET(templates),comment=T("Selectionner un template")),#,comment=T("Selectionner un template")
        Field('vlan',type='text',label=T('VLAN'),default="",requires=IS_IN_SET(vlans),comment=T("Selectionner un VLAN")),#,comment=T("Selectionner un VLAN"))]
    ]

    form = SQLFORM.factory(*fields)
    vm_input=()
    if form.accepts(request.vars,session,keepvalues=True):
        #url="http://'+request.env.http_host+':"+api_port+"/create_vm_server/"+vcenter+"/"+datacenter_id+"/"+folder+"/"+request.vars.template+"/"+request.vars.vlan+"/"+domain+"/"+environment+"/"+solution
        #vm_input=("vcenter,datacenter_id,folder,request.vars.template,request.vars.vlan,domain,environment,solution: --->",vcenter,datacenter_id,folder,request.vars.template,request.vars.vlan,domain,environment,solution)
        #vm_input=("datacenter,domain,environment,solution,template,vlan ***",datacenter,domain,environment,solution,request.vars.template,request.vars.vlan)
        #"""
        url="http://"+request.env.http_host+":"+api_port+"/create_vm_server/"+vcenter+"/"+datacenter_id+"/"+folder+"/"+request.vars.template+"/"+request.vars.vlan+"/"+domain+"/"+environment+"/"+solution
        outs=requests.get(url,stream=True).content
        if outs:
            f=outs.split(";")
            if len(f)==5:
                if f[2]<>"":
                    server_name=f[1]
                    folder=f[2]
                    folder_id=vcenter+"|"+("-".join(folder.split("-")[1:3]))
                    db(db.vms_folders.paths==this_paths+"|"+server_name).delete()
                    this_paths_id=db.vms_folders.insert(paths=this_paths+"|"+server_name,folder_id=folder_id,types="VirtualMachine")
                    #gotofolderx URL( f='vms_management',args=["ctrlf",])
                    redirect(URL( f='vms_management',args=["gotofolderx"+str(this_paths_id),]))
        response.flash =  "Ne peut pas créer ce server  "+outs
        #"""
        #response.flash = vm_input
    return dict(form =form,grid=str(vm_input))

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')|auth.has_membership(role='gestion_vms_read'))
def add_solution():
    import requests,random
    api_port=str(random.randint(8811,8813))
    vcenter_folder=request.args(0) or '_'
    vcenter_folder=vcenter_folder.split('_')
    vcenter=vcenter_folder[0]
    folder=vcenter_folder[1]
    rs=db(db.vms_folders.folder_id==vcenter+"|"+folder).select()
    if rs:
        this_paths=rs[0].paths
        path_folder=this_paths.replace('|',' - ').replace(' - VM - ',' - ')
    else:
        this_paths=""
        path_folder=""
    fields=[
        Field('path_folder',label=T('Emplacement'),default=path_folder,writable=False),
        Field('solution',type='input',requires=IS_NOT_EMPTY(),label=T('Solution'),default="",comment=T("Ajouter une solution")),
    ]
    url=""
    form = SQLFORM.factory(*fields)
    if form.accepts(request.vars,session,keepvalues=True):
        solution=request.vars.solution
        #url="http://'+request.env.http_host+':8080/gestion_vms_api.ps1?command=add_solution&vcenter="+vcenter+"&folder="+folder+"&solution="+solution
        url="http://'+request.env.http_host+':"+api_port+"/add_solution/"+vcenter+"/"+folder+"/"+solution
        outs=requests.get(url,stream=True).content
        if outs:
            #";$folder;$new_folder;"
            f=outs.split(";")
            if len(f)==4:
                if f[2]<>"":
                    folder=f[2]
                    folder_id=vcenter+"|"+("-".join(folder.split("-")[1:3]))
                    this_paths=this_paths+"|"+solution.upper()
                    db(db.vms_folders.paths==this_paths).delete()
                    this_paths_id=db.vms_folders.insert(paths=this_paths,folder_id=folder_id,types="Folder")
                    #gotofolderx URL( f='vms_management',args=["ctrlf",])
                    redirect(URL( f='vms_management',args=["gotofolderx"+str(this_paths_id),]))
        response.flash =  "Ne peut pas ajouter cette solution"
        #response.flash =  url
    #response.flash = outs
    #return dict(form =form,grid= url)
    return dict(form =form,grid= "")

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
    import subprocess
    script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_vms\gestion_vms_folders_vms_to_unificace.ps1'
    p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,error = p1.communicate()
    msg=(output,error)
    return dict(form="",grid=str(msg))

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
