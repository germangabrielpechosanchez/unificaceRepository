## -*- coding: utf-8 -*-
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

    (T("Gestion RDM & RDP"), False, '#', [
        (T('Mettre à jour RDM & RDP'), False, URL( f='rdm_rdp_update'),[]),
        #(T('Mettre à jour RDM & RDP'), False, URL( f='rdm_rdp_update1'),[]),
        ]),
    
    ]

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_rdm_rdp')|auth.has_membership(role='gestion_rdm_rdp_read'))
@auth.requires_login()
def index():
    #response.flash = T(u'Bievenue au module de gestion RDM & RDP')
    return dict()

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_rdm_rdp'))
def rdm_rdp_update():
    import os,shutil,subprocess 
    path=r"\\cemtl.rtss.qc.ca\cemtl\Ressources\Applications\Public\RDP_Run_with_PowerShell\BASE_STORE"
    try:
        shutil.rmtree(path)#delete folder
    except:
        pass
    query=(db.inventaire.in_service==True)#(db.inventaire.types=='serveur')&
    rs=db(query).select()
    #rs=rs[300:305]
    to_send=''
    i=0
    for r in rs:
        if (r.canonical_name<>None)&(r.canonical_name<>""):
            canonical_name=r.canonical_name.split("/") 
            path_name='\\'.join(canonical_name[:-1])           
            this_path=os.path.join(path+"\BY_DOMAINS",path_name)
            file_name=canonical_name[-1]+".ps1"

            group_name=os.path.join("BASE_STORE\BY_DOMAINS",path_name)
            display_name=canonical_name[-1]
        else:
            this_path=path+"\TO_VERIFY"
            file_name=r.name+".ps1"

            group_name="BASE_STORE\TO_VERIFY"
            display_name=r.name
        if (r.full_name<>None)&(r.full_name<>""):
            host_name=r.full_name
        elif (r.ip<>None)&(r.ip<>""):
            host_name=r.ip
        else:
            host_name=r.name
        if not os.path.exists(this_path):
            os.makedirs(this_path)
        path_file= os.path.join(this_path,file_name)
        #"""
        if r.in_service:
            f=open(path_file,"w")
            arg="/v:"+host_name
            f.write("Start-Process "+'"$env:windir\system32\mstsc.exe"'+" -ArgumentList "+'" '+arg+'"')
            f.close()
        #"""
        #$session = New-RDMSession -Group $thisGroup -Host $thisHost -Kind "RDPConfigured" -Name $thisName
        to_send+=group_name+","+host_name+","+display_name+";"
        
        if i>100:
            arg1= s=escape(to_send)
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_rdm_rdp\rdm_store_creator.ps1'
            p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            i=0
            to_send=group_name+","+host_name+","+display_name+";"
        else:
            to_send+=group_name+","+host_name+","+display_name+";"
            i+=1
    arg1= s=escape(to_send)
    ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_rdm_rdp\rdm_store_creator.ps1'
    p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  
    #response.flash = to_send  
    return dict()

def escape(arg1):
    #arg1=arg1.upper()
    arg1=arg1.replace("à","a")
    arg1=arg1.replace("â","a")
    arg1=arg1.replace("é","e")
    arg1=arg1.replace("ê","e")
    arg1=arg1.replace("è","e")
    arg1=arg1.replace("À","A")
    arg1=arg1.replace("Â","A")
    arg1=arg1.replace("É","E")
    arg1=arg1.replace("Ê","E")
    arg1=arg1.replace("È","E")
    arg1=arg1.replace(".","0_")
    arg1=arg1.replace(",","1_")
    arg1=arg1.replace(";","2_")
    arg1=arg1.replace('(',"3_")
    arg1=arg1.replace(')',"4_")
    arg1=arg1.replace(' ',"5_")
    arg1=arg1.replace('{',"6_")
    arg1=arg1.replace('}',"7_")
    arg1=arg1.replace("'","8_")
    arg1=arg1.replace(":","9_")
    arg1=arg1.replace("#","0-_")
    arg1=arg1.replace("@","1-_")
    return arg1
def descape(arg1):
    arg1=arg1.replace("0_",".")
    arg1=arg1.replace("1_",",")
    arg1=arg1.replace("2_",";")
    arg1=arg1.replace("3_",'(')
    arg1=arg1.replace("4_",')')
    arg1=arg1.replace("5_",' ')
    arg1=arg1.replace("6_",'{')
    arg1=arg1.replace("7_",'}')
    arg1=arg1.replace("8_","'")
    arg1=arg1.replace("9_",":")
    arg1=arg1.replace("0-_","#")
    arg1=arg1.replace("1-_","@")
    return arg1

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_rdm_rdp'))
def rdm_rdp_update1():
    
       
    response.flash = "test"

    #response.flash = T(u'Bievenue au module de gestion RDM & RDP')
    #redirect(URL('index', args=(1,2,3), vars=dict(a='b')))
    redirect(URL('index'))
    #return dict()

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


