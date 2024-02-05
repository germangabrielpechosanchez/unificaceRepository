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
        (T('Inventaires tout'), False, URL( f='inventory'),[]),
        (T('Inventaires des serveurs'), False, URL( f='inventory_server'),[]),
        (T('Inventaires des serveurs physiques'), False, URL( f='inventory_physical_server'),[]),
        (T('Inventaires des serveurs virtuels'), False, URL( f='inventory_virtual_server'),[]),
        (T('Inventaires des serveurs hotes'), False, URL( f='inventory_host_server'),[]),
        (T('Inventaires des serveurs inconnus'), False, URL( f='inventory_unknown_server'),[]),
        (T('Inventaires sans ping'), False, URL( f='inventory_no_ping_no_172'),[]),
        (T('Tables'), False, URL( f='tables'),[]),
        #(T('Mettre à jour des tables'), False, URL( f='tables_update'),[]),
        (T('Mettre à jour avec ADs et Vcenters'), False, URL( f='inventory_update'),[]),
        (T("Extraction d'infos"), False, URL( f='infos_extraction'),[]),
        ]),
    
    ]
menu_server=[
        (T('Serveurs en service'), False, URL( f='inventory_server'),[]),
        (T('Serveurs âge 0 an'), False, URL( f='inventory_server_0'),[]),
        (T('Serveurs âge 1 ans'), False, URL( f='inventory_server_1'),[]),
        (T('Serveurs âge 2 ans'), False, URL( f='inventory_server_2'),[]),
        (T('Serveurs âge 3 ans'), False, URL( f='inventory_server_3'),[]),
        (T('Serveurs âge 4 ans'), False, URL( f='inventory_server_4'),[]),
        (T('Serveurs âge 5 ans et plus'), False, URL( f='inventory_server_5'),[]),
    ]
menu_server=[(T('Inventaires des serveurs'), False, '#',menu_server)]

menu_physical_server=[
        (T('Serveurs en service'), False, URL( f='inventory_physical_server'),[]),
        (T('Serveurs âge 0 an'), False, URL( f='inventory_physical_server_0'),[]),
        (T('Serveurs âge 1 ans'), False, URL( f='inventory_physical_server_1'),[]),
        (T('Serveurs âge 2 ans'), False, URL( f='inventory_physical_server_2'),[]),
        (T('Serveurs âge 3 ans'), False, URL( f='inventory_physical_server_3'),[]),
        (T('Serveurs âge 4 ans'), False, URL( f='inventory_physical_server_4'),[]),
        (T('Serveurs âge 5 ans et plus'), False, URL( f='inventory_physical_server_5'),[]),
    ]
menu_physical_server=[(T('Inventaires des serveurs physiques'), False, '#',menu_physical_server)]

menu_virtual_server=[
        (T('Serveurs en service'), False, URL( f='inventory_virtual_server'),[]),
        (T('Serveurs âge 0 an'), False, URL( f='inventory_virtual_server_0'),[]),
        (T('Serveurs âge 1 ans'), False, URL( f='inventory_virtual_server_1'),[]),
        (T('Serveurs âge 2 ans'), False, URL( f='inventory_virtual_server_2'),[]),
        (T('Serveurs âge 3 ans'), False, URL( f='inventory_virtual_server_3'),[]),
        (T('Serveurs âge 4 ans'), False, URL( f='inventory_virtual_server_4'),[]),
        (T('Serveurs âge 5 ans et plus'), False, URL( f='inventory_virtual_server_5'),[]),
    ]
menu_virtual_server=[(T('Inventaires des serveurs virtuels'), False, '#',menu_virtual_server)]

menu_host_server=[
        (T('Serveurs en service'), False, URL( f='inventory_host_server'),[]),
        (T('Serveurs âge 0 an'), False, URL( f='inventory_host_server_0'),[]),
        (T('Serveurs âge 1 ans'), False, URL( f='inventory_host_server_1'),[]),
        (T('Serveurs âge 2 ans'), False, URL( f='inventory_host_server_2'),[]),
        (T('Serveurs âge 3 ans'), False, URL( f='inventory_host_server_3'),[]),
        (T('Serveurs âge 4 ans'), False, URL( f='inventory_host_server_4'),[]),
        (T('Serveurs âge 5 ans et plus'), False, URL( f='inventory_host_server_5'),[]),
    ]
menu_host_server=[(T('Inventaires des serveurs hotes'), False, '#',menu_host_server)]


import datetime,subprocess,platform,wmi
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()

if auth.is_logged_in():
    if (auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_edit_add')):
        create=True
        deletable=True
        editable=True
        user_signature=True
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_serveurs_edit')):
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


@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def index():
    grid=""
    """
    rs=db(db.inventaire.id>0).select(db.inventaire.id,db.inventaire.in_service)
    for r in rs:
        db(db.inventaire.id==r.id).update(gestred_2017=r.in_service)

    db(db.vcenters_host.id>0).update(
        NumCpu="",
        CpuUsageMhz="",
        CpuTotalMhz="",
        MemoryUsageGB="",
        MemoryTotalGB="",
        last_sync=datetime.date(2000,1,1),
        )
    db(db.vcenters_vm.id>0).update(
        NumCpu="",
        MemoryGB="",
        UsedSpaceGB="",
        last_sync=datetime.date(2000,1,1),
    )
    """

    response.flash = read_wmi_file()
    #response.flash = T(u'Bievenue au module de gestion des inventaires')

    return dict(grid=grid)

def read_wmi_file():
    gbits=float(2**30)
    in_file=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\read_ads_vms_to_file\out.txt'
    f_in=open(in_file,"r")
    lines=f_in.readlines()
    for line in lines:
        #hmrsql2005-2;2;3.874;0.003;113.895;71.393
        wmi_infos=line.replace("\n","")
        wmi_infos=wmi_infos.split(";")
        this_name=wmi_infos[0]
        wmi_infos=wmi_infos[1:]
        wmi_infos=(long(wmi_infos[0]),float(wmi_infos[1]),float(wmi_infos[2]),float(wmi_infos[3]),float(wmi_infos[4]))
        #wmi_infos=(wmi_infos[0],round(wmi_infos[1]/gbits,3),round(wmi_infos[2]/gbits,3),round(wmi_infos[3]/gbits,3),round(wmi_infos[4]/gbits,3))
        db(db.inventaire.name==this_name).update(
                    cpus=wmi_infos[0],
                    memory=wmi_infos[1],
                    memory_used=wmi_infos[1]-wmi_infos[2],
                    storages=wmi_infos[3],
                    storages_used=wmi_infos[3]-wmi_infos[4],
        )
        db.commit()
    f_in.close()
    return len(lines)
   

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
@auth.requires(auth.has_membership(role='admin'))
def infos_extraction():
    #import subprocess, platform
    grid =""
    rs=db(db.inventaire.id>0).select(db.inventaire.id,db.inventaire.name,db.inventaire.full_name,db.inventaire.ip)
    #rs=db(db.inventaire.id==14363).select(db.inventaire.id,db.inventaire.name,db.inventaire.full_name,db.inventaire.ip)
    #rs=rs[221:250]
    #"""
    gbits=float(2**30)
    for r in rs:
        """
        ping_date=datetime.date(2000,1,1)
        for i in [r.full_name,r.ip,r.name]:
            if ping_ok(i):
                ping_date=today
                break
        infos=""
        for i in [r.full_name,r.ip,r.name]:
            infos=pstools_psinfo(i)
            if infos<>"":
                break
        """
        #(cpus,full_memory,free_memory,full_disk,free_disk)
        #wmi_infos=(0,0,0,0,0)       
        for i in [r.full_name,r.ip,r.name]:
            wmi_infos=wmi_read(i)
            if wmi_infos<>(0,0,0,0,0):
                #to float
                wmi_infos=(wmi_infos[0],round(wmi_infos[1]/gbits,3),round(wmi_infos[2]/gbits,3),round(wmi_infos[3]/gbits,3),round(wmi_infos[4]/gbits,3))
                db(db.inventaire.id==r.id).update(
                    #ping=ping_date,
                    #infos=infos,
                    cpus=wmi_infos[0],
                    memory=wmi_infos[1],
                    memory_used=wmi_infos[1]-wmi_infos[2],
                    storages=wmi_infos[3],
                    storages_used=wmi_infos[3]-wmi_infos[4],
                    )
                db.commit()
                break

    #"""
    #redirect(URL('index'))
    #response.flash = str(rs)
    return dict(grid=grid)

def ping_ok(sHost):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', sHost), shell=True)
    except Exception, e:
        return False
    return True

def pstools_psinfo(sHost):
    p1 = subprocess.Popen([r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\PSTools\PsInfo.exe',"\\\\"+sHost,'-d'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,error = p1.communicate()
    if error=="":
        return output
    else:
        return ""

def wmi_read(sHost):
    #connection = wmi.WMI(ip, user=username, password=password)
    try:
        c=wmi.WMI(sHost)
        free_disk=0
        full_disk=0   
        for disk in c.Win32_LogicalDisk (DriveType=3):
            try: free_disk+=long(disk.FreeSpace)    
            except: pass
            try: full_disk+=long(disk.Size)
            except: pass
        cpus=0
        cores=0
        for cpu in c.Win32_Processor():
            cpus+=1
            try: cores+=long(cpu.NumberOfCores)
            except: pass
        full_memory=0
        for i in c.Win32_ComputerSystem():
            try: full_memory+=long(i.TotalPhysicalMemory)
            except: pass
        free_memory=0
        for os in c.Win32_OperatingSystem():
            try: free_memory+=long(os.FreePhysicalMemory)
            except: pass
        if cores<>0: cpus=cores
        else: cpus=cpus
        return (cpus,full_memory,free_memory,full_disk,free_disk)
    except:
        return (0,0,0,0,0)



@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_no_ping_no_172():
    response.menu+=[
        (T('Inventaires sans ping'), False, URL( f='inventory_no_ping_no_172'),[]),
        ]
    query=(db.inventaire.last_logon<datetime.date(2017,7,1))&(db.inventaire.ping<datetime.date(2017,9,1))&(db.inventaire.types=="serveur")&(db.inventaire.in_service==True)&(~db.inventaire.ip.like('%172.%'))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    #query=query&(db.inventaire.operating_system.like('%2003%'))
    #rs=db(query).select()
    #rs=db(query).update(in_service=False)
    #response.flash = rs
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def tables():
    menu_url=[]
    servers_table=["inventory","ads_computers","vcenters_vm","vcenters_host","octopus_servers","servers",""]

    for table in servers_table:
    #    if '_' not in table: # tables will be in menu
    #        menu_url+=[(T(table), False, URL(c='manage',f='manage',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[table])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    table = request.args(0) or 'vcenters_host'
    if not table in db.tables(): redirect(URL('error'))

    grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)
    #response.flash = T(u'terminé')
    return dict(grid=grid)


@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory():
    response.menu+=[
        (T('Inventaires'), False, URL( f='inventory'),[]),
        ]
    query=(db.inventaire.id>0)
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    #response.flash = T(u'terminé')
    return dict(grid=grid)
#(T('Inventaires des serveurs'), False, URL( f='inventory_server'),[]),

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_server():    
    response.menu += menu_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.in_service==True)
    #db(query).update(gestred_2017=True)
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    #count0=db(query&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day)&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day))).count()    
    #response.flash = str(request.args[:1])
    #rs=db(query&(db.inventaire.category.like('%hote%'))).select()
    #for r in rs:
    #    db(db.inventaire.id==r.id).update(category="hote")    
    #response.flash = str(len(rs))

    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_server_0():        
    response.menu += menu_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.in_service==True)&(db.inventaire.beginning>=datetime.date(this_year-1,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_server_1():
    response.menu += menu_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-1,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-2,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_server_2():
    response.menu += menu_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-2,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-3,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_server_3():
    response.menu += menu_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-3,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-4,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_server_4():
    response.menu += menu_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-4,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-5,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_server_5():
    response.menu += menu_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-5,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_physical_server():    
    response.menu += menu_physical_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='physique')&(db.inventaire.in_service==True)#db.inventaire.category.like('%physique%')#db.inventaire.category=='physique'
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    #count0=db(query&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day)&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day))).count()    
    #response.flash = str(request.args[:1])
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_physical_server_0():        
    response.menu += menu_physical_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='physique')&(db.inventaire.in_service==True)&(db.inventaire.beginning>=datetime.date(this_year-1,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_physical_server_1():
    response.menu += menu_physical_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='physique')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-1,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-2,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_physical_server_2():
    response.menu += menu_physical_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='physique')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-2,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-3,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_physical_server_3():
    response.menu += menu_physical_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='physique')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-3,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-4,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_physical_server_4():
    response.menu += menu_physical_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='physique')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-4,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-5,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_physical_server_5():
    response.menu += menu_physical_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='physique')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-5,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_virtual_server():    
    response.menu += menu_virtual_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='virtuel')&(db.inventaire.in_service==True)
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    #count0=db(query&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day)&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day))).count()    
    #response.flash = str(request.args[:1])
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_virtual_server_0():        
    response.menu += menu_virtual_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='virtuel')&(db.inventaire.in_service==True)&(db.inventaire.beginning>=datetime.date(this_year-1,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_virtual_server_1():
    response.menu += menu_virtual_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='virtuel')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-1,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-2,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_virtual_server_2():
    response.menu += menu_virtual_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='virtuel')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-2,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-3,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_virtual_server_3():
    response.menu += menu_virtual_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='virtuel')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-3,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-4,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_virtual_server_4():
    response.menu += menu_virtual_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='virtuel')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-4,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-5,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_virtual_server_5():
    response.menu += menu_virtual_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='virtuel')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-5,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_host_server():    
    response.menu += menu_host_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='hote')&(db.inventaire.in_service==True)
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    #count0=db(query&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day)&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day))).count()    
    #response.flash = str(request.args[:1])
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_host_server_0():        
    response.menu += menu_host_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='hote')&(db.inventaire.in_service==True)&(db.inventaire.beginning>=datetime.date(this_year-1,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_host_server_1():
    response.menu += menu_host_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='hote')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-1,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-2,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_host_server_2():
    response.menu += menu_host_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='hote')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-2,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-3,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_host_server_3():
    response.menu += menu_host_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='hote')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-3,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-4,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_host_server_4():
    response.menu += menu_host_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='hote')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-4,this_month,this_day))\
    &(db.inventaire.beginning>=datetime.date(this_year-5,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_host_server_5():
    response.menu += menu_host_server
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='hote')&(db.inventaire.in_service==True)&(db.inventaire.beginning<datetime.date(this_year-5,this_month,this_day))
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_unknown_server():
    response.menu+=[
        (T('Inventaires des serveurs inconnus'), False, URL( f='inventory_unknown_server'),[]),
        ]
    query=(db.inventaire.types=='serveur')&(db.inventaire.category!='hote')&(db.inventaire.category!='physique')&(db.inventaire.category!='virtuel')&(db.inventaire.in_service==True)
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    db(query&(db.inventaire.name.like("%vxpr%"))).update(category='virtuel')
    db(query&(db.inventaire.name.like("%vxdv%"))).update(category='virtuel')
    db(query&(db.inventaire.name.like("%phdv%"))).update(category='hote')
    db(query&(db.inventaire.name.like("%vwdv%"))).update(category='virtuel')
    #response.flash = str(len(rs))
    #response.flash = T(u'terminé')
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update():#inventory_update_from_ads_vcenters
    #msg="---"
    msg=read_tables_from_files() #db.ads_computers;vcenters_vm;;vcenters_host
    #"""
    #ads_computers to inventaire
    rs=db((db.ads_computers.OperatingSystem.like("%server%"))&(db.ads_computers.Enabled == "True")&(db.ads_computers.LastLogonDate > "2017-08-01")).select()
    #rows=db(db.inventaire.id>0).update(last_sync=datetime.date(2017,4,1))
    this_table=db.inventaire
    for r in rs:
        name=r.SamAccountName.lower()
        full_name=r.DNSHostName.lower()
        canonical_name=r.CanonicalName
        ip=r.IPv4Address
        types="serveur"
        category=""
        ip=r.IPv4Address
        operating_system=r.OperatingSystem
        #model=r.model
        #serial=r.serial
        #notes=r.notes
        last_sync=today
        last_logon=r.LastLogonDate
        created=r.whenCreated
        #purchase=r.purchase
        beginning=r.whenCreated
        in_ads=True
        #in_vcenters=r.in_ads
        #in_octopus=r.in_octopus
        in_service=True

        qry=(this_table.name==name)|(this_table.name==full_name)|(this_table.full_name==full_name)|(this_table.full_name==name)
        found=db(qry).select()
        if found:
            db(qry).update(\
            #name=name,\
            full_name=full_name,\
            canonical_name=canonical_name,\
            #types=types,\
            #category=category,\
            ip=ip,\
            #operating_system=operating_system,\
            #model=r.model,\
            #serial=r.serial,\
            #notes=r.notes,\
            last_sync=last_sync,\
            last_logon=last_logon,\
            created=created,\
            #purchase=purchase,\
            beginning=beginning,\
            in_ads=in_ads,\
            #in_vcenters=in_ads,\
            #in_octopus=in_octopus,\
            in_service=in_service\
            )
        else:
            this_table.insert(\
            name=name,\
            full_name=full_name,\
            canonical_name=canonical_name,\
            types=types,\
            category=category,\
            ip=ip,\
            operating_system=operating_system,\
            #model=r.model,\
            #serial=r.serial,\
            #notes=r.notes,\
            last_sync=last_sync,\
            last_logon=last_logon,\
            created=created,\
            #purchase=purchase,\
            beginning=beginning,\
            in_ads=in_ads,\
            #in_vcenters=in_ads,\
            #in_octopus=in_octopus,\
            in_service=in_service\
            )
    #vcenters_vm to inventaire
    #rs=db((db.vcenters_vm.States=="Running")&(db.vcenters_vm.OSFullName.like("%server%"))).select()#used in september
    rs=db((db.vcenters_vm.last_sync==today)&(db.vcenters_vm.States=="Running")&(db.vcenters_vm.OSFullName.like("%server%"))).select()
    this_table=db.inventaire
    for r in rs:
        name=r.name.lower()
        full_name=r.HostName.lower()
        #ip=r.IPv4Address
        types="serveur"
        category="virtuel"
        #ip=r.IPv4Address
        operating_system=r.OSFullName
        #model=r.model
        #serial=r.serial
        #notes=r.notes
        last_sync=today
        #last_logon=r.LastLogonDate
        #created=r.whenCreated
        #purchase=r.purchase
        #beginning=r.whenCreated
        #in_ads=True
        in_vcenters=True
        #in_octopus=r.in_octopus
        in_service=True
        try: cpus=float(r.NumCpu)
        except: cpus=0.0
        try: memory=float(r.MemoryGB)
        except: memory=0.0
        try: storages_used=float(r.UsedSpaceGB)
        except: storages_used=0.0


        qry=(this_table.name==name)|(this_table.name==full_name)|(this_table.full_name==full_name)|(this_table.full_name==name)
        found=db(qry).select()
        if found:
            db(qry).update(\
            #name=name,\
            full_name=full_name,\
            types=types,\
            category=category,\
            #ip=ip,\
            #operating_system=operating_system,\
            #model=r.model,\
            #serial=r.serial,\
            #notes=r.notes,\
            last_sync=last_sync,\
            #last_logon=last_logon,\
            #created=created,\
            #purchase=purchase,\
            #beginning=beginning,\
            #in_ads=in_ads,\
            in_vcenters=in_vcenters,\
            #in_octopus=in_octopus,\
            in_service=in_service,\
            cpus=cpus,\
            memory=memory,\
            storages_used=storages_used,\
            )
        else:
            this_table.insert(\
            name=name,\
            full_name=full_name,\
            types=types,\
            category=category,\
            #ip=ip,\
            operating_system=operating_system,\
            #model=r.model,\
            #serial=r.serial,\
            #notes=r.notes,\
            last_sync=last_sync,\
            #last_logon=last_logon,\
            #created=created,\
            #purchase=purchase,\
            #beginning=beginning,\
            #in_ads=in_ads,\
            in_vcenters=in_vcenters,\
            #in_octopus=in_octopus,\
            in_service=in_service,\
            cpus=cpus,\
            memory=memory,\
            storages_used=storages_used,\
            )
    
    #vcenters_host to inventaire
    rs=db((db.vcenters_host.last_sync==today)).select()
    this_table=db.inventaire
    for r in rs:
        full_name=r.name.lower()
        #ip=r.IPv4Address
        types="serveur"
        category="hote"
        #ip=r.IPv4Address
        #operating_system=r.OSFullName
        #model=r.model
        #serial=r.serial
        #notes=r.notes
        description="Versions: "+r.versions+"; Licensekey: "+r.LicenseKey
        last_sync=today
        #last_logon=r.LastLogonDate
        #created=r.whenCreated
        #purchase=r.purchase
        beginning=r.installedDate
        #in_ads=True
        in_vcenters=True
        #in_octopus=r.in_octopus
        in_service=True
        try: cpus=float(r.NumCpu)
        except: cpus=0.0
        try: memory_used=float(r.MemoryUsageGB)
        except: memory_used=0.0
        try: memory=float(r.MemoryTotalGB)
        except: memory=0.0

        qry=(this_table.full_name==full_name)
        found=db(qry).select()
        if found:
            db(qry).update(\
            #name=name,\
            #full_name=full_name,\
            types=types,\
            category=category,\
            #ip=ip,\
            #operating_system=operating_system,\
            #model=r.model,\
            #serial=r.serial,\
            #notes=r.notes,\
            #description=description,\
            last_sync=last_sync,\
            #last_logon=last_logon,\
            #created=created,\
            #purchase=purchase,\
            #beginning=beginning,\
            #in_ads=in_ads,\
            in_vcenters=in_vcenters,\
            #in_octopus=in_octopus,\
            in_service=in_service,\
            cpus=cpus,\
            memory=memory,\
            memory_used=memory_used,\
            )
        else:
            this_table.insert(\
            name=full_name,\
            full_name=full_name,\
            types=types,\
            category=category,\
            #ip=ip,\
            #operating_system=operating_system,\
            #model=r.model,\
            #serial=r.serial,\
            #notes=r.notes,\
            last_sync=last_sync,\
            description=description,\
            #last_logon=last_logon,\
            #created=created,\
            #purchase=purchase,\
            #beginning=beginning,\
            #in_ads=in_ads,\
            in_vcenters=in_vcenters,\
            #in_octopus=in_octopus,\
            in_service=in_service,\
            cpus=cpus,\
            memory=memory,\
            memory_used=memory_used,\
            )
    #"""


    response.flash = msg
    grid=""
    return dict(grid=grid)



#@auth.requires(auth.has_membership(role='admin'))
def read_tables_from_files():
    #update PCs
    msg="read_tables_from_files"
    #"""
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\read_ads_vms_to_file\ADs.txt']
    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        #lines=lines[10:30]
        this_table=db.ads_computers    
        #db(this_table.id>0).delete() 
        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')        
            if(len(cols)>=7): #secure with symbol 
                DNSHostName=cols[0].lower()
                IPv4Address=cols[1]
                SamAccountName=cols[2].replace("$","").lower()
                LastLogonDate=cols[3]
                whenCreated=cols[4]
                OperatingSystem=cols[5]
                Enabled=cols[6]
                CanonicalName=cols[7]
                if  DNSHostName.strip()=="":
                    DNSHostName=SamAccountName
                found=db((this_table.DNSHostName==DNSHostName)|(this_table.SamAccountName==SamAccountName)).select()
                if found:
                    #this_rec=found[0]
                    db(this_table.DNSHostName==DNSHostName).update(
                        IPv4Address=IPv4Address,\
                        SamAccountName=SamAccountName,\
                        LastLogonDate=LastLogonDate,\
                        whenCreated=whenCreated,\
                        OperatingSystem=OperatingSystem,\
                        Enabled=Enabled,\
                        CanonicalName=CanonicalName,\
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
                        Types='',\
                        CanonicalName=CanonicalName,\
                    )
    #"""
    #update vcenters_vm
    #this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\read_ads_vms_to_file\vms.txt', r'\\HLHL-apps.hlhl.rtss.qc.ca\Apps\Commun\echange\vilounha\unificace\vms.txt']
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\read_ads_vms_to_file\vms.txt']
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
        
            if(len(cols)>=9): #secure with symbol ;

                HostName=cols[0].lower()
                IPAddress=cols[1]
                name=cols[2].lower()
                OSFullName=cols[3]
                States=cols[4]
                VMHost=cols[5].lower()
                NumCpu=cols[6]
                MemoryGB=cols[7]
                UsedSpaceGB=cols[8]
                if  HostName.strip()=="":
                    HostName=name
                found=db(this_table.HostName==HostName).select()
                if found:
                    #this_rec=found[0]
                    db(this_table.HostName==HostName).update(
                        IPAddress=IPAddress,\
                        name=name,\
                        OSFullName=OSFullName,\
                        States=States,\
                        VMHost=VMHost,\
                        NumCpu=NumCpu,\
                        MemoryGB=MemoryGB,\
                        UsedSpaceGB=UsedSpaceGB,\
                        last_sync=today,\
                        )
                else:
                    this_table.insert(
                        HostName=HostName,\
                        IPAddress=IPAddress,\
                        name=name,\
                        OSFullName=OSFullName,\
                        States=States,\
                        VMHost=VMHost,\
                        NumCpu=NumCpu,\
                        MemoryGB=MemoryGB,\
                        UsedSpaceGB=UsedSpaceGB,\
                        last_sync=today,\
                        )
        msg+="---"+str(len(lines))

    #update vcenters_host
    #this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\read_ads_vms_to_file\hosts.txt', r'\\HLHL-apps.hlhl.rtss.qc.ca\Apps\Commun\echange\vilounha\unificace\hosts.txt']
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\read_ads_vms_to_file\hosts.txt']
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
        
            if(len(cols)>=10): #secure with symbol ;

                name=cols[0].lower()
                versions=cols[1]
                PowerState=cols[2]
                LicenseKey=cols[3]
                installedDate=cols[4]
                NumCpu=cols[5]
                CpuUsageMhz=cols[6]
                CpuTotalMhz=cols[7]
                MemoryUsageGB=cols[8]
                MemoryTotalGB=cols[9]
                found=db(this_table.name==name).select()
                if found:
                    #this_rec=found[0]
                    db(this_table.name==name).update(
                        versions=versions,\
                        LicenseKey=LicenseKey,\
                        PowerState=PowerState,\
                        installedDate=installedDate,\
                        NumCpu=NumCpu,\
                        CpuUsageMhz=CpuUsageMhz,\
                        CpuTotalMhz=CpuTotalMhz,\
                        MemoryUsageGB=MemoryUsageGB,\
                        MemoryTotalGB=MemoryTotalGB,\
                        last_sync=today,\
                        )
                else:
                    this_table.insert(
                        name=name,\
                        versions=versions,\
                        LicenseKey=LicenseKey,\
                        PowerState=PowerState,\
                        installedDate=installedDate,\
                        NumCpu=NumCpu,\
                        CpuUsageMhz=CpuUsageMhz,\
                        CpuTotalMhz=CpuTotalMhz,\
                        MemoryUsageGB=MemoryUsageGB,\
                        MemoryTotalGB=MemoryTotalGB,\
                        last_sync=today,\
                        )

        msg+="---"+str(len(lines))
    #"""
    return msg
    

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


