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

    (T("Gestion des serveurs"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T("Création de serveur"), False, URL( f='server_management',vars={'type':'VW'}),[]),
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
    #db(db.app2app.id>0).delete()
    #db(db.mappage.oldDomaine.like('hsco',case_sensitive=False)).update(oldDomaine="hsco.net")

    #db(db.app2app.status=="donne").delete()
    #rs=db(db.pdfs_printers.is_active==True).select(db.pdfs_printers.pdf_folder,db.pdfs_printers.url_printer,groupby=db.pdfs_printers.pdf_folder)
    #rs=db(db.pdfs_printers.is_active==True).select(db.pdfs_printers.ALL)
    #response.flash=rs
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')|auth.has_membership(role='gestion_vms_read'))
def server_management():
    msg=""
    form=""
    args_view=request.args(0) or 'simple'
    if args_view=='simple':
        args_view_next='ctrlf'
    else:
        args_view_next='simple'

    #display response

    if False: #request.vars.folder_id:#creation of server
        r=db(db.vms_folders.id==int(request.vars.folder_id)).select().first()
        if r:
            if request.vars.type[:1]=='P':
                session.data=dict(
                    command='gestion_vms_creation_serveur_physique',
                    folder_id=r.folder_id.replace('|','!'),
                    type_os=request.vars.type
                )
                #call_background_task().response
                import json
                response_data=call_background_task()
                response_dict=json.loads(response_data.response)
                if response_dict["status"]!="Il faut reajouter cette solution!":
                    form="<h3>Nom du server: "+response_dict["server_name"]+"</h3>"
                    form+="<h3>Domaine: "+response_dict["domain"]+"</h3>"
                    form+="<h3>Solution: "+response_dict["solution"]+"</h3>"
                    form+="<h3>Datacenter: "+response_dict["datacenter"]+"</h3>"
                    form+="<h3>JSON: </h3>"
                    form+=XML(""+str(response_dict)+"<br><br>")
                else:
                    msg=response_dict["status"]
       

    menu_v=[
        (T('Windows'), False, URL( f='server_management',args=[args_view],vars={'type':'VW'})),
        (T('Linux'), False, URL( f='server_management',args=[args_view],vars={'type':'VL'})),
        (T('Solaris'), False, URL( f='server_management',args=[args_view],vars={'type':'VS'})),
        (T('Citrix'), False, URL( f='server_management',args=[args_view],vars={'type':'VX'})),
        ]
    menu_p=[
        (T('Windows'), False, URL( f='server_management',args=[args_view],vars={'type':'PW'})),
        (T('Linux'), False, URL( f='server_management',args=[args_view],vars={'type':'PL'})),
        (T('Solaris'), False, URL( f='server_management',args=[args_view],vars={'type':'PS'})),
        (T('Hyperviseur'), False, URL( f='server_management',args=[args_view],vars={'type':'PH'})),
        ]
    this_menu={
        'VW':'Serveur virtuel Windows',
        'VL':'Serveur virtuel Linux',
        'VS':'Serveur virtuel Solaris',
        'VX':'Serveur virtuel Citrix',
        'PW':'Serveur physique Windows',
        'PL':'Serveur physique Linux',
        'PS':'Serveur physique Solaris',
        'PH':'Serveur physique Hyperviseur',
    }
    response.menu+=[
        (T('Création de '), False, '#',''),
        (T('Serveur virtuel'), False, '#',menu_v),
        (T('Serveur physique'), False, '#',menu_p),
        (T('Changement de vu'), False, URL( f='server_management',args=[args_view_next],vars={'type':request.vars.type})),
        #(T(this_menu[request.vars.type]), False, '#',[]),
    ]

    goto_folder_path=""
    ctrlf=False
    if args_view=="ctrlf":
        ctrlf=True
        checked_enabled="checked enabled"
    if request.vars.goto_folder_id:
        goto_folder_id=int(request.vars.goto_folder_id)
        rs=db(db.vms_folders.id==goto_folder_id).select()
        if rs:
            goto_folder_path=rs[0].paths.split("|")
            goto_folder_path.remove("VM")
            goto_folder_path="|".join(goto_folder_path)
            #msg+=goto_folder_path

    grid='<h4>Selectionner un emplacement pour : '+(this_menu[request.vars.type]).upper()+'</h4><br><br><br><body><table><ol class="tree">'
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
                    if path_current in goto_folder_path:
                        checked_enabled="checked enabled"
                    if goto_folder_path==path_current:
                        folders_display="<u><i>"+folders[i]+"</i></u>"
                    else:
                        folders_display=folders[i]
                else:
                    folders_display=folders[i]
                #
                args_vars=args_view+'/?type='+request.vars.type+'&folder_id='+r.folder_id
                #
                if (level==solution_level)&(r.types=="Folder"):
                    grid+='<div class="dropdown"><label class="dropbtn" for="'+id_folder+'">'+folders_display+'</label><div class="dropdown-content"><a href="https://'+request.env.http_host+'/init/gestion_vms/add_solution/'+args_vars+'">Ajouter une solution</a></div></div><input type="checkbox" '+checked_enabled+' id="'+id_folder+'" />'
                elif (level==solution_level+1)&(r.types=="Folder"):
                    if request.vars.type:
                        if request.vars.type[:1]=='V':
                            grid+='<div class="dropdown"><label class="dropbtn1" for="'+id_folder+'">'+folders_display+'</label><div class="dropdown-content"><a href="https://'+request.env.http_host+'/init/gestion_vms/add_server_virtual/'+args_vars+'">Créer un serveur virtuel</a></div></div><input type="checkbox" '+checked_enabled+' id="'+id_folder+'" />'
                        else:
                            grid+='<div class="dropdown"><label class="dropbtn1" for="'+id_folder+'">'+folders_display+'</label><div class="dropdown-content"><a href="https://'+request.env.http_host+'/init/gestion_vms/add_server_physical/'+args_vars+'">Créer un serveur physique</a></div></div><input type="checkbox" '+checked_enabled+' id="'+id_folder+'" />'
                elif r.types=="Folder":
                    grid+='<label for="'+id_folder+'">'+folders_display+'</label> <input type="checkbox" '+checked_enabled+' id="'+id_folder+'" />'
                else:
                    grid+='<li><div class="dropdown"><div class="dropbtn2">'+folders_display+'</div><div class="dropdown-content"><a href="https://'+request.env.http_host+'/init/actualisation_inventaires/cis_listing?request_ci_name='+folders[i]+'">Décommissionner: '+folders_display+'</a></div></div></li>'

                    
    while (path_current <> ""):
        path_current="|".join((path_current.split("|"))[:-1])
        grid+="</li></ol>"

    grid+='</ol></table></body>'
    grid=grid.replace("</ol><ol>","")


    #response.flash=response_dict
    #response.flash=msg
    response.flash=session.msg
    session.msg=None
    return dict(form=XML(form),grid=grid)

def call_background_task():
    import json,uuid,time
    publish_id=uuid.uuid4().hex
    db.app2app.insert(
        publish_id=publish_id,
        subscribe_id='',
        app='gestion_vms',
        status='new',
        command=json.dumps(session.data),
        response='',
        )
    db.commit()
    qry=(db.app2app.publish_id==publish_id)&(db.app2app.status=="donne")
    waiting=True
    i=0
    while(waiting):
        r=db(qry).select().first()
        if r:
            waiting=False
        else:
            time.sleep(1)
            if(i>240):
                waiting=False
                r="waiting too long"
            else:
                i+=1
    return r    

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')|auth.has_membership(role='gestion_vms_read'))
def add_solution():
    args_view=request.args(0) or 'simple'
    vcenter_folder=request.vars.folder_id
    rs=db(db.vms_folders.folder_id==vcenter_folder).select()
    if rs:
        this_paths=rs[0].paths
        path_folder=this_paths.replace('|',' - ').replace(' - VM - ',' - ')
        parent_id=rs[0].id
    else:
        this_paths=""
        path_folder=""
        parent_id=0
    fields=[
        Field('path_folder',label=T('Emplacement'),default=path_folder,writable=False),
        Field('solution',type='input',requires=IS_NOT_EMPTY(),label=T('Solution'),default="",comment=T("Ajouter une solution")),
    ]
    url=""
    form = SQLFORM.factory(*fields)
    if form.accepts(request.vars,session,keepvalues=True):
        solution=request.vars.solution
        r=db(db.vms_folders.folder_id==vcenter_folder).select().first()
        if r:
            session.data=dict(
                command='gestion_vms_add_solution',
                folder_id=r.folder_id.replace('|','!'),
                solution=request.vars.solution
            )
            import json
            response_data=call_background_task()
            response_dict=json.loads(response_data.response)
            #{u'status': u'created', u'new_folder_id': u's03vwpr00002.cemtl.rtss.qc.ca|group-v296392', u'solution': u'VPTEST', u'old_folder_id': u's03vwpr00002.cemtl.rtss.qc.ca|group-v117'} × 
            this_path=db(db.vms_folders.folder_id==response_dict['old_folder_id']).select().first().paths+"|"+response_dict['solution']
            if response_dict['new_folder_id']:
                this_folder=db(db.vms_folders.paths==this_path).select().first()
                if this_folder:
                    this_folder=this_folder.id
                    db(db.vms_folders.paths==this_path).update(folder_id=response_dict['new_folder_id'],types="Folder")
                else:           
                    this_folder=db.vms_folders.insert(paths=this_path,folder_id=response_dict['new_folder_id'],types="Folder")
                goto_folder_id=str(int(this_folder))        
                #redirect(URL( f='server_management',args=[args_view],vars={'type':request.vars.type,'source':'add_solution','goto_folder_id':goto_folder_id,'parent_id':str(parent_id),'solution':solution,}))
                redirect(URL( f='server_management',args=[args_view],vars={'type':request.vars.type,'source':'add_solution','goto_folder_id':goto_folder_id}))
    return dict(form =form,grid= "")

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')|auth.has_membership(role='gestion_vms_read'))
def add_server_physical():
    args_view=request.args(0) or 'simple'
    vcenter_folder=request.vars.folder_id
    session.data=dict(
        command='gestion_vms_creation_serveur_physique',
        folder_id=vcenter_folder.replace('|','!'),
        type_os=request.vars.type
        )
    import json
    response_data=call_background_task()
    response_dict=json.loads(response_data.response)
    session.msg=response_dict["status"]
    
    folder_id=response_dict["folder_id"].replace('!','|')
    this_path=db(db.vms_folders.folder_id==folder_id).select().first().paths+"|"+response_dict['server_name']
    this_folder=db(db.vms_folders.paths==this_path).select().first()
    if this_folder:
        this_folder=this_folder.id
        db(db.vms_folders.id==this_folder).update(folder_id=folder_id,types="PhisicalMachine")
    else:           
        this_folder=db.vms_folders.insert(paths=this_path,folder_id=folder_id,types="PhisicalMachine")
    goto_folder_id=str(int(this_folder))
    
    #goto_folder_id='39441'
    #session.msg=response_dict      
    redirect(URL( f='server_management',args=[args_view],vars={'type':request.vars.type,'source':'add_server_physical','goto_folder_id':goto_folder_id}))                        
    return 1

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_vms')|auth.has_membership(role='gestion_vms_read'))
def add_server_virtual():
    form=""
    grid=""
    args_view=request.args(0) or 'simple'
    vcenter_folder=request.vars.folder_id
    session.data=dict(
        command='gestion_vms_get_data_vcenter',
        folder_id=vcenter_folder.replace('|','!'),
        type_os=request.vars.type
        )
    import json
    response_data=call_background_task()
    response_dict=json.loads(response_data.response)
    session.msg=response_dict['status']
    templates=[("windows_no_template","Windows sans template"),("linux_no_template","Linux sans template")]
    for i in range(len(response_dict["template_id"])):
        templates+=[(response_dict["template_id"][i],response_dict["template_name"][i]),] 
    templates_name=dict((i,j) for i,j in templates)
    vlans=[("no_vlan","Sans VLAN")]
    for i in range(len(response_dict["vlan_id"])):
        vlans+=[(response_dict["vlan_id"][i],response_dict["vlan_name"][i]),]
    vlans_name=dict((i,j) for i,j in vlans)
   
    datacenter_solution=(response_dict["vcenter"]+" - "+response_dict["domain"]+" - "+response_dict["environment_name"]+" - "+response_dict["solution"]).upper()
    fields=[
        Field('datacenter_solution',label=T('Datacenter - Domaine - Environnement - Solution'),default=datacenter_solution,writable=False,comment=T("Valider les données sélectionnées")),
        Field('template',type='text',label=T('Template'),default="",requires=IS_IN_SET(templates),comment=T("Selectionner un template")),
        Field('vlan',type='text',label=T('VLAN'),default="",requires=IS_IN_SET(vlans),comment=T("Selectionner un VLAN")),
    ]
    buttons=[
        TD(INPUT(_type="submit",_value="Créer un serveur",_id="Créer un serveur",_name="Créer un serveur",_style="background-color:#0066ff")),
    ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(9,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        session.data=dict(
            command='gestion_vms_creation_serveur_virtual',
            folder_id=response_dict["folder"],
            vcenter=response_dict["vcenter"],
            type_os=response_dict["type_os"],
            datacenter=response_dict["datacenter"],
            template_id=request.vars.template,
            template_name=templates_name[request.vars.template],
            datastore=response_dict["datastore"],
            vlan_id=request.vars.vlan,
            vlan_name=vlans_name[request.vars.vlan],
            resourcepool=response_dict["resourcepool"],
            domain=response_dict["domain"],
            env=response_dict["env"],
            env2=response_dict["env2"],
            environment_name=response_dict["environment_name"],
            solution=response_dict["solution"],
        )
        import json
        response_data=call_background_task()

        response_dict=json.loads(response_data.response)
        session.msg=response_dict['status']

        if response_dict["status"]<>"Il faut reajouter cette solution!":
            #$VM.id="VirtualMachine-vm-287223"
            folder_id=response_dict["vcenter"]+'|'+response_dict["folder_id"].replace('Folder-','')
            this_path=db((db.vms_folders.folder_id==folder_id)).select().first().paths+"|"+response_dict['server_name']#&(db.vms_folders.types=="VirtualMachine")
            this_folder=db(db.vms_folders.paths==this_path).select().first()
            folder_id=response_dict["vcenter"]+'|'+response_dict["vm_id"].replace('VirtualMachine-','')
            if this_folder:
                this_folder=this_folder.id
                db(db.vms_folders.id==this_folder).update(folder_id=folder_id,types="VirtualMachine")
            else:           
                this_folder=db.vms_folders.insert(paths=this_path,folder_id=folder_id,types="VirtualMachine")
            goto_folder_id=str(int(this_folder))
        else:
            folder_id=response_dict["vcenter"]+'|'+response_dict["folder_id"].replace('Folder-','')
            goto_folder_id=str(db(db.vms_folders.folder_id==folder_id).select().first().id) 
        redirect(URL( f='server_management',args=[args_view],vars={'type':request.vars.type,'source':'add_server_virtual','goto_folder_id':goto_folder_id}))                        

    response.flash=session.msg
    session.msg=None
    return dict(form=form,grid=grid)

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
    
    return dict(form="",grid=grid)

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
