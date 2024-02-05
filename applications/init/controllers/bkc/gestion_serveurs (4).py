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

    (T("Gestion des inventaires"), False, '#', [
        (T('Vue-ADs-VMs-Hosts'), False, URL( f='PCs_VMs_Hosts'),[]),
        (T('Vue-VMs-Hosts-ADs'), False, URL( f='VMs_Hosts_PCs'),[]),
        (T('Vue-Hosts-ADs'), False, URL( f='Hosts_PCs'),[]),
        (T('Tables'), False, URL( f='tables'),[]),
        (T('Mettre à jour des tables'), False, URL( f='tables_update'),[]),
        ]),
    
    ]
if auth.is_logged_in():
    if (auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')):
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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read'))
def index():
    grid=""

    response.flash = T(u'Bievenue au module de gestion des seveurs')
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read'))
def tables():
    menu_url=[]
    servers_table=["ads_computer","vcenters_vm","vcenters_host","",""]

    for table in servers_table:
    #    if '_' not in table: # tables will be in menu
    #        menu_url+=[(T(table), False, URL(c='manage',f='manage',args=[table])),]
        menu_url+=[(T(table), False, URL(f='index',args=[table])),]

    response.menu += [(T("Tables"), False, '#', menu_url)]

    table = request.args(0) or 'vcenters_host'
    if not table in db.tables(): redirect(URL('error'))

    grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)
    response.flash = T(u'terminé')
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read'))
def PCs_VMs_Hosts():
    response.menu+=[
        (T('Vue-ADs-VMs-Hosts'), False, URL( f='PCs_VMs_Hosts'),[]),
        ]
    query=(db.ads_computer.id>0)
    #left=[db.section.on(db.department.id==db.section.department_id),
    #  db.department.on(db.division.id==db.department.division_id)]
    #left=db.vcenters_vm.on(db.ads_computer.DNSHostName == db.vcenters_vm.HostName)
    left=[db.vcenters_vm.on(db.ads_computer.DNSHostName == db.vcenters_vm.HostName), db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name)]
    fields=[db.ads_computer.DNSHostName,db.ads_computer.IPv4Address,db.ads_computer.LastLogonDate,db.ads_computer.whenCreated,db.ads_computer.OperatingSystem,\
    db.vcenters_vm.name,db.vcenters_vm.States,db.vcenters_vm.OSFullName,\
    db.vcenters_host.name,db.vcenters_host.versions,db.vcenters_host.LicenseKey]
    grid = SQLFORM.grid(query,left=left,fields=fields,user_signature=False,maxtextlength=50,\
    deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)

    response.flash = T(u'terminé')

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read'))
def VMs_Hosts_PCs():
    response.menu+=[
        (T('Vue-VMs-Hosts-ADs'), False, URL( f='VMs_Hosts_PCs'),[]),
        ]
    #query=(db.ads_computer.id>0)
    query=(db.vcenters_vm.id>0)
    #left=[db.vcenters_vm.on(db.ads_computer.DNSHostName == db.vcenters_vm.HostName), db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name)]
    left=[db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name), db.ads_computer.on(db.vcenters_vm.HostName==db.ads_computer.DNSHostName)]
    fields=[db.ads_computer.DNSHostName,db.ads_computer.IPv4Address,db.ads_computer.LastLogonDate,db.ads_computer.whenCreated,db.ads_computer.OperatingSystem,\
    db.vcenters_vm.name,db.vcenters_vm.States,db.vcenters_vm.OSFullName,\
    db.vcenters_host.name,db.vcenters_host.versions,db.vcenters_host.LicenseKey]
    grid = SQLFORM.grid(query,left=left,fields=fields,user_signature=False,maxtextlength=50,
    deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)

    response.flash = T(u'terminé')

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read'))
def Hosts_PCs():
    response.menu+=[
        (T('Vue-Hosts-ADs'), False, URL( f='Hosts_PCs'),[]),
        ]
    #query=(db.ads_computer.id>0)
    query=(db.ads_computer.id>0)
    #left=[db.vcenters_vm.on(db.ads_computer.DNSHostName == db.vcenters_vm.HostName), db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name)]
    left=[db.vcenters_host.on(db.ads_computer.DNSHostName == db.vcenters_host.name),]
    fields=[db.ads_computer.DNSHostName,db.ads_computer.IPv4Address,db.ads_computer.LastLogonDate,db.ads_computer.whenCreated,db.ads_computer.OperatingSystem,\
    #db.vcenters_vm.name,db.vcenters_vm.States,db.vcenters_vm.OSFullName,\
    db.vcenters_host.name,db.vcenters_host.versions,db.vcenters_host.LicenseKey]
    grid = SQLFORM.grid(query,left=left,fields=fields,user_signature=False,maxtextlength=50,
    deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)

    response.flash = T(u'terminé')

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def tables_update():
    grid =""

    #"""
    #update PCs
    this_file=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\ADs.txt'
    f=open(this_file,"r")
    lines=f.readlines()
    #lines=lines[10:30]

    this_table=db.ads_computer
   
    #db(this_table.id>0).delete() #to deable

    for line in lines:
        line=line.replace("\n","")
        line=line.replace("\r","")
        cols=line.split(';')
       
        if(len(cols)>=7): #secure with symbol ;

            DNSHostName=cols[0].lower()
            IPv4Address=cols[1]
            SamAccountName=cols[2].replace("$","").lower()
            LastLogonDate=cols[3]
            whenCreated=cols[4]
            OperatingSystem=cols[5]
            Enabled=cols[6]
            if  DNSHostName.strip()=="":
                DNSHostName=SamAccountName
            found=db(this_table.DNSHostName==DNSHostName).select()
            if found:
                this_rec=found[0]
                this_rec.update(
                    IPv4Address=IPv4Address,\
                    SamAccountName=SamAccountName,\
                    LastLogonDate=LastLogonDate,\
                    whenCreated=whenCreated,\
                    OperatingSystem=OperatingSystem,\
                    Enabled=Enabled,\
                )
            else:
                this_table.insert(
                    DNSHostName=DNSHostName,\
                    IPv4Address=IPv4Address,\
                    SamAccountName=SamAccountName,\
                    LastLogonDate=LastLogonDate,\
                    whenCreated=whenCreated,\
                    OperatingSystem=OperatingSystem,\
                    Enabled=Enabled,\
                )

    #update vcenters_vm

    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\vms.txt', r'\\HLHL-apps.hlhl.rtss.qc.ca\Apps\Commun\echange\vilounha\unificace\vms.txt']
    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        #lines=lines[0:40]
        this_table=db.vcenters_vm
    
        #db(this_table.id>0).delete()

        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')
        
            if(len(cols)>=6): #secure with symbol ;

                HostName=cols[0].lower()
                IPAddress=cols[1]
                name=cols[2].lower()
                OSFullName=cols[3]
                States=cols[4]
                VMHost=cols[5].lower()
                if  HostName.strip()=="":
                    HostName=name
                found=db(this_table.HostName==HostName).select()
                if found:
                    this_rec=found[0]
                    this_rec.update(
                        IPAddress=IPAddress,\
                        name=name,\
                        OSFullName=OSFullName,\
                        States=States,\
                        VMHost=VMHost,\
                        )
                else:
                    this_table.insert(
                        HostName=HostName,\
                        IPAddress=IPAddress,\
                        name=name,\
                        OSFullName=OSFullName,\
                        States=States,\
                        VMHost=VMHost,\
                        )
    #"""

    #update vcenters_host
    #this_file=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\hosts.txt'
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\hosts.txt', r'\\HLHL-apps.hlhl.rtss.qc.ca\Apps\Commun\echange\vilounha\unificace\hosts.txt']
    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        #lines=lines[0:40]
        this_table=db.vcenters_host
    
        #db(this_table.id>0).delete()

        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')
        
            if(len(cols)>=4): #secure with symbol ;

                name=cols[0].lower()
                versions=cols[1]
                PowerState=cols[2]
                LicenseKey=cols[3]

                found=db(this_table.name==name).select()
                if found:
                    this_rec=found[0]
                    this_rec.update(
                        versions=versions,\
                        LicenseKey=LicenseKey,\
                        PowerState=PowerState,\
                        )
                else:
                    this_table.insert(
                        name=name,\
                        versions=versions,\
                        LicenseKey=LicenseKey,\
                        PowerState=PowerState,\
                        )



    
    #response.flash = str(len(cols))
    response.flash = T(u'terminé')
    


    
    return dict(grid=grid)


###############################################################################################

@auth.requires(auth.has_membership(role='admin'))
def sql_import():


    grid =""
##########################inser data mappage#######################################
    """

    this_file=r'\\s03vwpr00031\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\groups_hlhl.txt'
    f=open(this_file,"r")
    lines=f.readlines()
    
    #db((db.domains_security_group.id>0)).delete()

    for line in lines:
        line=line.replace("\n","")
        line=line.replace("\r","")
        cols=line.split(';')
       
        if(len(cols)>=2):
            db.domains_security_group.insert(
                domain_id=2,\
                group_name=cols[0],\
                description=cols[1],\
                protected=False,\
                )

    
    response.flash = str(len(cols))
    """

    
    ############# oc_utilisateur code to import these data############

    ##########################inser data mappage#######################################
    """

    db((db.mappage.id>0)).delete()

    this_file=r'C:\Users\unificace\unificace\logonPE16.txt'
    f=open(this_file,"r")
    lines=f.readlines()
    #lines=f.read()#.decode('utf-8', 'ignore')
    #lines=lines.replace('\r\n',"")
    #lines=lines.split('#_#')
    #lines=lines[3:4]
    #db((db.mappage.id>0)).delete()

    for line in lines:
        cols=line.split(',')
        if cols[0].lower()=='lhlnt':
            cols[0]="hlhl.rtss.qc.ca"

        if(len(cols)>6):
            db.mappage.insert(
                newDomaine=cols[0],\
                newUsername=cols[1],\
                oldDomaine=cols[2],\
                OldUsername=cols[3],\
                messages=cols[4],\
                OldShare1=cols[5],\
                OldShare2=cols[6],\
                OldShare3=cols[7],\
                OldShare4=cols[8],\
                OldShare5=cols[9],\
                OldShare6=cols[10],\
                #OldShare7=cols[11],\
                OldShare7="",\
                )

    #response.flash = str(lines[353])
    #cols=(lines[1]).decode('utf-8', 'ignore')
    #cols=lines[1]
    #response.flash = str(len(lines))
    response.flash = str(len(cols))
    """

    
    ############# oc_utilisateur code to import these data############
    """
    this_file=r'C:\Users\admphav\unificatex\powershell\oc_users.txt'
    f=open(this_file,"r")
    lines=f.read()
    lines=lines.split('#_#')
    #lines=lines[3:4]
    
    for line in lines:
        cols=line.split('#,#')
        if(len(cols)>=17):
            db.oc_utilisateur.insert(code=cols[0],\
                                     numero=cols[10],\
                                     nom=cols[15],\
                                     prenom=cols[7],\
                                     nom_famille=cols[8],\
                                     logon=cols[2],\
                                     courriel=cols[3],\
                                     telephone=cols[1],\
                                     poste=cols[13],\
                                     cell=cols[12],\
                                     site=cols[5],\
                                     departement=cols[6],\
                                     titre_emploi=cols[11],\
                                     locale=cols[14],\
                                     note="",\
                                     actif=cols[9],\
                                     )        
    
    
    response.flash = str(len(cols))



    """
    ###################################################
    ############# acces code to import these data############
    """
    this_file=r'C:\Users\admphav\unificatex\powershell\gaa.txt'
    f=open(this_file,"r")
    lines=f.read()
    lines=lines.split('#_#')
    #lines=lines[3:5]

    for line in lines:
        cols=line.split('#,#')
        if(len(cols)>=6):
            this_group=db(db.acces.code==cols[0]).select()
            if(len(this_group)<1):
                groupe="groupe_"+cols[0]
                db.acces.insert(code=cols[0],groupe=groupe,)

    
    
    response.flash = str(len(this_group))

    """
    ###################################################
    ############# acces code to import these data############
    """
    lines=db(db.acces.id>0).select()

    for line in lines:
        
        #code="IUSMM "+line.code
        #db(db.acces.id==line.id).update(code=code,)

        #code=line.code.replace("IUSMM ","IUSMM - ")
        groupe=line.groupe.replace("groupe_","IUSMM_GDA_")
        db(db.acces.id==line.id).update(groupe=groupe,)


    
    
    response.flash = str(len(lines))

    """
    ###################################################
    ############# acces code to import these data############
    """
    this_file=r'C:\Users\admphav\unificatex\powershell\gaa.txt'
    f=open(this_file,"r")
    lines=f.read()
    lines=lines.split('#_#')
    #lines=lines[0:5]

    for line in lines:
        cols=line.split('#,#')
        if(len(cols)>=6):
            this_app=db(db.app.code==cols[1]).select()
            if(len(this_app)<1):
                code=cols[1]
                acces="IUSMM - "+cols[0]
                this_acces=db(db.acces.code==acces).select()
                if(this_acces):
                    acces_id=this_acces[0].id
                else:
                    acces_id=198
                db.app.insert(code=code,acces=acces_id,)

    
    
    response.flash = str(len(lines))

    """
    ###################################################
    ############# acces code to import these data############
    """
    this_file=r'C:\Users\admphav\unificatex\powershell\gaa.txt'
    f=open(this_file,"r")
    lines=f.read()
    lines=lines.split('#_#')
    #lines=lines[0:2]

    for line in lines:
        cols=line.split('#,#')
        if(len(cols)>=6):
            groupe="IUSMM_GDA_"+cols[0]
            this_groupe=db(db.acces.groupe==groupe).select()
            if(this_groupe):
                groupe_id=this_groupe[0].id
                #groupe_id=this_groupe[0].code
            else:
                groupe_id=198
                #groupe_id=""

            #2 3 4
            nom=cols[4].split('#.#')
            if(len(nom)>1):
                prenom=nom[1]
                nom_famille=nom[0]
            else:
                prenom=""
                nom_famille=""


                
            this_utilisateur=db((db.oc_utilisateur.prenom.like(prenom+'%'))&(db.oc_utilisateur.prenom.like(nom_famille+'%'))).select()
            if(this_utilisateur):
                utilisateur_id=this_utilisateur[0].nom
                #utilisateur_id=this_utilisateur[0].nom
            else:
                utilisateur_id=""
                #utilisateur_id=""
            full_name=prenom+" "+nom_famille 
            db.acces_utilisateur.insert(groupe=groupe,utilisateur=full_name)

    
    
    response.flash = str(len(lines))

    """
    ###################################################
    """

    db((db.acces_utilisateur.utilisateur=="")).delete()
    response.flash = str()
    """
    ###################################################


    
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


