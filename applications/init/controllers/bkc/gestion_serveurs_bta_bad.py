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
        (T('Inventaires'), False, URL( f='inventory'),[]),
        (T('Inventaires des serveurs'), False, URL( f='inventory_server'),[]),
        (T('Inventaires des serveurs physiques'), False, URL( f='inventory_physical_server'),[]),
        (T('Inventaires des serveurs virtuels'), False, URL( f='inventory_virtual_server'),[]),
        (T('Inventaires des serveurs hotes'), False, URL( f='inventory_host_server'),[]),
        (T('Inventaires des serveurs inconnus'), False, URL( f='inventory_unknown_server'),[]),
        #(T('Vue-ADs-VMs-Hosts'), False, URL( f='PCs_VMs_Hosts'),[]),
        #(T('Vue-VMs-Hosts-ADs'), False, URL( f='VMs_Hosts_PCs'),[]),
        #(T('Vue-Hosts-ADs'), False, URL( f='Hosts_PCs'),[]),
        (T('Tables'), False, URL( f='tables'),[]),
        (T('Mettre à jour des tables'), False, URL( f='tables_update'),[]),
        #(T('Mettre à jour des serveurs'), False, URL( f='servers_update'),[]),
        (T('Mettre à jour des inventaires'), False, URL( f='inventory_update'),[]),
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


import datetime
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

    response.flash = T(u'Bievenue au module de gestion des inventaires')
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def tables():
    menu_url=[]
    servers_table=["inventory","ads_computers","vcenters_vm","vcenters_host","octopus_servers","servers",""]

    for table in servers_table:
    #    if '_' not in table: # tables will be in menu
    #        menu_url+=[(T(table), False, URL(c='manage',f='manage',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[table])),]

    response.menu += [(T("Tables"), False, '#', menu_url)]

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
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    #count0=db(query&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day)&(db.inventaire.beginning >= datetime.date(this_year-1,this_month,this_day))).count()    
    #response.flash = str(request.args[:1])
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
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='physique')&(db.inventaire.in_service==True)
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






"""
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def inventory_host_server():
    response.menu+=[
        (T('Inventaires des serveurs hotes'), False, URL( f='inventory_host_server'),[]),
        ]
    query=(db.inventaire.types=='serveur')&(db.inventaire.category=='hote')&(db.inventaire.in_service==True)
    grid = SQLFORM.grid(query,user_signature=False,maxtextlength=50,deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)
    #response.flash = T(u'terminé')
    return dict(grid=grid)
"""


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
    #response.flash = T(u'terminé')
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def PCs_VMs_Hosts():
    response.menu+=[
        (T('Vue-ADs-VMs-Hosts'), False, URL( f='PCs_VMs_Hosts'),[]),
        ]
    query=(db.ads_computers.id>0)
    #left=[db.section.on(db.department.id==db.section.department_id),
    #  db.department.on(db.division.id==db.department.division_id)]
    #left=db.vcenters_vm.on(db.ads_computers.DNSHostName == db.vcenters_vm.HostName)
    left=[db.vcenters_vm.on(db.ads_computers.DNSHostName == db.vcenters_vm.HostName), db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name)]
    fields=[db.ads_computers.DNSHostName,db.ads_computers.IPv4Address,db.ads_computers.LastLogonDate,db.ads_computers.whenCreated,db.ads_computers.OperatingSystem,\
    db.vcenters_vm.name,db.vcenters_vm.States,db.vcenters_vm.OSFullName,\
    db.vcenters_host.name,db.vcenters_host.versions,db.vcenters_host.LicenseKey,db.vcenters_host.installedDate]
    grid = SQLFORM.grid(query,left=left,fields=fields,user_signature=False,maxtextlength=50,\
    deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)

    response.flash = T(u'terminé')

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def VMs_Hosts_PCs():
    response.menu+=[
        (T('Vue-VMs-Hosts-ADs'), False, URL( f='VMs_Hosts_PCs'),[]),
        ]
    #query=(db.ads_computers.id>0)
    query=(db.vcenters_vm.id>0)
    #left=[db.vcenters_vm.on(db.ads_computers.DNSHostName == db.vcenters_vm.HostName), db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name)]
    left=[db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name), db.ads_computers.on(db.vcenters_vm.HostName==db.ads_computers.DNSHostName)]
    fields=[db.ads_computers.DNSHostName,db.ads_computers.IPv4Address,db.ads_computers.LastLogonDate,db.ads_computers.whenCreated,db.ads_computers.OperatingSystem,\
    db.vcenters_vm.name,db.vcenters_vm.States,db.vcenters_vm.OSFullName,\
    db.vcenters_host.name,db.vcenters_host.versions,db.vcenters_host.LicenseKey,db.vcenters_host.installedDate]
    grid = SQLFORM.grid(query,left=left,fields=fields,user_signature=False,maxtextlength=50,
    deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)

    response.flash = T(u'terminé')

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs')|auth.has_membership(role='gestion_serveurs_read')|auth.has_membership(role='gestion_serveurs_edit')|auth.has_membership(role='gestion_serveurs_edit_add'))
def Hosts_PCs():
    response.menu+=[
        (T('Vue-Hosts-ADs'), False, URL( f='Hosts_PCs'),[]),
        ]
    #query=(db.ads_computers.id>0)
    query=(db.ads_computers.id>0)
    #left=[db.vcenters_vm.on(db.ads_computers.DNSHostName == db.vcenters_vm.HostName), db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name)]
    left=[db.vcenters_host.on(db.ads_computers.DNSHostName == db.vcenters_host.name),]
    fields=[db.ads_computers.DNSHostName,db.ads_computers.IPv4Address,db.ads_computers.LastLogonDate,db.ads_computers.whenCreated,db.ads_computers.OperatingSystem,\
    #db.vcenters_vm.name,db.vcenters_vm.States,db.vcenters_vm.OSFullName,\
    db.vcenters_host.name,db.vcenters_host.versions,db.vcenters_host.LicenseKey,db.vcenters_host.installedDate]
    grid = SQLFORM.grid(query,left=left,fields=fields,user_signature=False,maxtextlength=50,
    deletable=deletable,editable=editable,create=create,searchable=searchable,details=details)

    response.flash = T(u'terminé')

    return dict(grid=grid)
#####################################################
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def servers_update():
    ##########
    ##########
    
    left=[db.vcenters_vm.on(db.ads_computers.DNSHostName == db.vcenters_vm.HostName), db.vcenters_host.on(db.vcenters_vm.VMHost == db.vcenters_host.name)]

    fields=[db.ads_computers.DNSHostName,db.ads_computers.IPv4Address,db.ads_computers.LastLogonDate,db.ads_computers.whenCreated,db.ads_computers.OperatingSystem,\
    db.vcenters_vm.name,db.vcenters_vm.States,db.vcenters_vm.OSFullName,\
    db.vcenters_host.name,db.vcenters_host.versions,db.vcenters_host.LicenseKey,db.vcenters_host.installedDate]

    query=((db.ads_computers.LastLogonDate>='2017-02')&(db.ads_computers.OperatingSystem.like('%server%'))|(db.vcenters_vm.OSFullName.like('%server%')))
    
    rows = db(query).select(db.ads_computers.DNSHostName,db.ads_computers.IPv4Address,db.ads_computers.LastLogonDate,db.ads_computers.whenCreated,db.ads_computers.OperatingSystem,\
    db.vcenters_vm.name,db.vcenters_vm.States,db.vcenters_vm.OSFullName,\
    db.vcenters_host.name,db.vcenters_host.versions,db.vcenters_host.LicenseKey,db.vcenters_host.installedDate,left=left)

    this_table=db.servers
    db(this_table.id>0).delete()
    
    for r in rows:
        if r.vcenters_vm.name==None:
            this_value="---"
        else:
            this_value=r.vcenters_vm.name
        found=db(this_table.DNSHostName==r.ads_computers.DNSHostName).select()
        if found:
            db(this_table.DNSHostName==r.ads_computers.DNSHostName).update(\
                DNSHostName=r.ads_computers.DNSHostName,\
                IPv4Address=r.ads_computers.IPv4Address,\
                LastLogonDate=r.ads_computers.LastLogonDate,\
                whenCreated=r.ads_computers.whenCreated,\
                OperatingSystem=r.ads_computers.OperatingSystem,\
                name=this_value,\
                States=r.vcenters_vm.States,\
                OSFullName=r.vcenters_vm.OSFullName,\
                nameHost=r.vcenters_host.name,\
                versions=r.vcenters_host.versions,\
                LicenseKey=r.vcenters_host.LicenseKey,\
                installedDate=r.vcenters_host.installedDate,\
            )
        else:
            this_table.insert(\
                DNSHostName=r.ads_computers.DNSHostName,\
                IPv4Address=r.ads_computers.IPv4Address,\
                LastLogonDate=r.ads_computers.LastLogonDate,\
                whenCreated=r.ads_computers.whenCreated,\
                OperatingSystem=r.ads_computers.OperatingSystem,\
                name=this_value,\
                States=r.vcenters_vm.States,\
                OSFullName=r.vcenters_vm.OSFullName,\
                nameHost=r.vcenters_host.name,\
                versions=r.vcenters_host.versions,\
                LicenseKey=r.vcenters_host.LicenseKey,\
                installedDate=r.vcenters_host.installedDate,\
            )

    grid=""

    response.flash = T(u'terminé')

    return dict(grid=grid)

#####################################################

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update_ttttt():
    #this_table=db.inventaire

    #this_date=datetime.date(1789,1,1)
    #old_date=datetime.date(2017,4,10)
    #db.mytable.myfield.like('%value%')

    #qry=(this_table.operating_system.like('%Windows%'))&(this_table.operating_system.like('%7%'))
    #rows=len(db(qry).select())  
    #rows=db(qry).update(types='ordinateur')

    #qry=(this_table.operating_system.like('%Windows%'))&(this_table.operating_system.like('%xp%'))
    #rows=len(db(qry).select())  
    #rows=db(qry).update(types='ordinateur')

    #qry=(this_table.id>0)
    #rows=len(db(qry).select(this_table.full_name,orderby=this_table.full_name,groupby=this_table.full_name))
    #rows=len(db(qry).select(this_table.name,orderby=this_table.name,groupby=this_table.name))
    #qry=(this_table.types=='serveur')&(this_table.in_octopus==True)&(this_table.in_ads==False)&(this_table.in_vcenters==False)
    #qry=(this_table.types=='serveur')&(this_table.in_vcenters==False)
    #qry=(this_table.id>0)
    #recs=db(qry)._select(this_table.name)
    #rows=len(db(db.vcenters_vm.name.belongs(recs)).select())
    #rows=db(db.vcenters_vm.name.belongs(recs)).select(db.vcenters_vm.name)
    #for row in rows:
    #    db(this_table.name==row.name).update(in_vcenters=True)

    #qry=(this_table.operating_system.like('%Telephonie%'))
    #rows=db(qry).update(types='serveur telephonique')
    #rows=len(db(qry).select())
    """
    qry=(this_table.id>0)
    rows=db(qry).select()
    for r in rows:
        found_id=(this_table.id==r.id)
        if  r.purchase!=datetime.date(1789,1,1):
            db(found_id).update(beginning=r.purchase)
        else:
            db(found_id).update(beginning=r.created)
    
    #servers_to_in_service
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\servers_to_in_service.txt',]
    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        this_table=db.inventaire

        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')
        
            if(len(cols)>=2): #secure with symbol ;

                name=cols[0].lower()
                ip=cols[1]
                


                found=db((this_table.name==name)|(this_table.full_name==name)).select()
                if found:
                    db((this_table.name==name)|(this_table.full_name==name)).update(
                        ip=ip,\
                        in_service=True,\
                        
                    )
    
    #servers_to_in_service
    this_table=db.inventaire
    #rows=db((this_table.types=='serveur')&(this_table.in_service==True)&(this_table.operating_system=='')&(this_table.in_ads==False)&(this_table.in_vcenters==False)).select(this_table.id)
    #rows=db((this_table.types=='serveur')&(this_table.in_service==True)&(this_table.operating_system=='')&(this_table.in_ads==False)&(this_table.in_vcenters==False)).update(in_service=False,)
    
    #rows=len(rows)
    
    i=0
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\servers_to_in_service1.txt',]
    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        this_table=db.inventaire

        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')
        
            if(len(cols)>=2): #secure with symbol ;

                name=cols[0].lower()
                ip=cols[1]
                


                found=db((this_table.name==name)|(this_table.full_name==name)).select()
                if found:
                    i+=1
                    
                    db((this_table.name==name)|(this_table.full_name==name)).update(ip=ip,in_service=True,)
                #else:
                #    db((this_table.name==name)|(this_table.full_name==name)).update(ip=ip,in_service=True,)
                    
                    
    

    #Field('code',requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'oc_utilisateur.code')]),


    rs=db(db.inventory.id>0).select()
    this_table=db.inventaire
    #db(db.inventaire.id>0).delete()
    msg='---'
    for r in rs:

        full_name=r.full_name.lower()
        name=r.name.lower()
        qry=(this_table.name==name)|(this_table.full_name==full_name)
        found=db(qry).select()
        if found:
            msg+= name+"----"+full_name        
            db((this_table.name==name)|(this_table.full_name==full_name)).update(
            name=name,\
            full_name=full_name,\
            types=r.types,\
            category=r.category,\
            ip=r.ip,\
            operating_system=r.operating_system,\
            model=r.model,\
            serial=r.serial,\
            notes=r.notes,\
            last_logon=r.last_logon,\
            created=r.created,\
            purchase=r.purchase,\
            beginning=r.beginning,\
            in_ads=r.in_ads,\
            in_vcenters=r.in_ads,\
            in_octopus=r.in_ads,\
            in_service=r.in_ads\
            )
        else:

        if True:
            this_table.insert(
            name=r.name,\
            full_name=r.full_name,\
            types=r.types,\
            category=r.category,\
            ip=r.ip,\
            operating_system=r.operating_system,\
            model=r.model,\
            serial=r.serial,\
            notes=r.notes,\
            last_logon=r.last_logon,\
            created=r.created,\
            purchase=r.purchase,\
            beginning=r.beginning,\
            in_ads=r.in_ads,\
            in_vcenters=r.in_ads,\
            in_octopus=r.in_ads,\
            in_service=r.in_ads\
            )



    rs=db(db.inventory.id>0).select()
    this_table=db.inventaire
    db(db.inventaire.id>0).delete()
    msg='+++'
    for r in rs:
        full_name=r.full_name.lower()
        name=r.name.lower()
        qry=(this_table.name==name)|(this_table.full_name==full_name)|(this_table.name==full_name)|(this_table.full_name==name)
        rs=len(db(qry).select())
        if rs>1:
            msg+=name+"---"+full_name
    """

    #rs=db(db.inventaire.id>0).select()
    #rs=len(rs)    

    #response.flash = T(u'terminé')
    

    #db(db.inventaire.id>0).delete()
    #response.flash = str(msg)
    response.flash = str(len(rs))
    grid=""
    



    return dict(grid=grid)

#####################################################
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update():
    #db(db.inventaire.id>55550).delete()


    this_table=db.db.ads_computers

    rows=db((this_table.OperatingSystem.like('%server%')).select()


 

    response.flash = str(len(rs))
    grid=""
    return dict(grid=grid)

#####################################################
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update_servers_manual_hmr_os():
    #Nom;Type / catégorie;Manufacturier / modèle;No. de série;Date d'achat;
    #BDR5-LABO;virtuel;VMware, Inc, Vsphere 5.1;;2007-05-24;

    #BDR5-LABO;Red hat 4
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\servers_manual_hmr_os.txt',]
    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        this_table=db.inventaire

        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')
        
            if(len(cols)>=2): #secure with symbol ;

                full_name=cols[0].lower()
                name=full_name.split('.')[0]
                operating_system=cols[1]
                


                found=db((this_table.name==name)|(this_table.full_name==full_name)).select()
                if found:
                    db((this_table.name==name)|(this_table.full_name==full_name)).update(
                        operating_system=operating_system,\
                        
                    )



    response.flash = T(u'terminé')
    grid=""

    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update_vm_host6   ():
#
#in_ads=db((db.ads_computers.DNSHostName==full_name)|(db.ads_computers.DNSHostName==name)|(db.ads_computers.SamAccountName==name)).select()
#in_vms=db((db.vcenters_vm.HostName==full_name)|(db.vcenters_vm.HostName==name)).select()
#in_hosts=db((db.vcenters_host.name==full_name)|(db.vcenters_host.name==name)).select()
#in_octopus=db((db.octopus_servers.name==full_name)|(db.octopus_servers.name==name)).select()

    this_table=db.inventaire

    rows=db((db.vcenters_host.id>0)).select()


    for row in rows:
        
        full_name=row.name.lower()
        name=full_name.split('.')[0]
        category='host'
        #ip=row.ip
        #if ip==None: ip=''
        operating_system="VMWare ver.: "+row.versions+ "lic.: "+row.LicenseKey
        created=row.installedDate
        if created=='0000-00-00': created='1789-01-01'
        created=created.split('-')
        created=datetime.date(int(created[0]),int(created[1]),int(created[2]))
        #if operating_system==None: operating_system=''
        #notes=row.notes
        #if notes==None: notes=''
        #states=row.States
        #if states=="NotRunning":
        #in_service=False
        #else:
        #in_service=True
        
        #qry=(this_table.name==full_name)|(this_table.full_name==full_name)
        qry=(this_table.name==name)|(this_table.full_name==full_name)|(this_table.full_name==name)
        #qry=(db.ads_computers.DNSHostName==name)|(db.ads_computers.DNSHostName==full_name)|(db.ads_computers.SamAccountName==name)
        found=db(qry).select()
        if found:
            
            db((this_table.name==name)|(this_table.full_name==full_name)|(this_table.full_name==name)).update(
            name=name,\
            full_name=full_name,\
            types='serveur',\
            category=category,\
            #ip=found[0].IPv4Address,\
            operating_system=operating_system,\
            #model=model,\
            #serial=serial,\
            #notes="octopus: "+found[0].category+";"+found[0].notes,\
            #notes=notes+";"+operating_system+";"+ip,\
            #last_logon=last_logon,\
            created=created,\
            #in_ads=True,\
            in_vcenters=True,\
            #in_octopus=True,\
            in_service=True\
            )
            #if purchase_update:
            #db(qry).update(purchase=purchase,)
        #"""
        else:
            this_table.insert(
            name=name,\
            full_name=full_name,\
            types='serveur',\
            category=category,\
            #ip=found[0].IPv4Address,\
            operating_system=operating_system,\
            #model=model,\
            #serial=serial,\
            #notes="octopus: "+found[0].category+";"+found[0].notes,\
            #notes=notes+";"+operating_system+";"+ip,\
            #last_logon=last_logon,\
            created=created,\
            #in_ads=True,\
            in_vcenters=True,\
            #in_octopus=True,\
            in_service=True\
            )
        #"""



    response.flash = T(u'terminé')
    grid=""

    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update_ads_5():
#
#in_ads=db((db.ads_computers.DNSHostName==full_name)|(db.ads_computers.DNSHostName==name)|(db.ads_computers.SamAccountName==name)).select()
#in_vms=db((db.vcenters_vm.HostName==full_name)|(db.vcenters_vm.HostName==name)).select()
#in_hosts=db((db.vcenters_host.name==full_name)|(db.vcenters_host.name==name)).select()
#in_octopus=db((db.octopus_servers.name==full_name)|(db.octopus_servers.name==name)).select()

    this_table=db.inventaire

    rows=db((db.inventaire.id>0)).select()


    for row in rows:
        
        full_name=row.full_name.lower()
        name=full_name.split('.')[0]
        #category='virtuel'
        ip=row.ip
        if ip==None: ip=''
        operating_system=row.operating_system
        if operating_system==None: operating_system=''
        notes=row.notes
        if notes==None: notes=''
        #states=row.States
        #if states=="NotRunning":
        #in_service=False
        #else:
        #in_service=True
        """
        purchase=row.date_purchase
        model=row.model
        serial=row.serial

        if purchase=='':
            purchase='1789-01-01'
            purchase_update=False
        else:
            purchase_update=True
        purchase=purchase.split('-')
        purchase=datetime.date(int(purchase[0]),int(purchase[1]),int(purchase[2]))
        """

        #qry=(this_table.name==name)|(this_table.full_name==full_name)|(this_table.full_name==name)
        qry=(db.ads_computers.DNSHostName==name)|(db.ads_computers.DNSHostName==full_name)|(db.ads_computers.SamAccountName==name)
        found=db(qry).select()
        if found:
            last_logon=found[0].LastLogonDate
            created=found[0].whenCreated
            if last_logon=='':
                last_logon='3000-01-01'
            last_logon=last_logon.split('-')
            last_logon=datetime.date(int(last_logon[0]),int(last_logon[1]),int(last_logon[2]))

            if created=='':
                    created='1789-01-01'
            created=created.split('-')
            created=datetime.date(int(created[0]),int(created[1]),int(created[2]))
           
            db((this_table.name==name)|(this_table.full_name==full_name)|(this_table.full_name==name)).update(
            name=name,\
            full_name=found[0].DNSHostName,\
            #types='serveur',\
            #category=category,\
            ip=found[0].IPv4Address,\
            operating_system=found[0].OperatingSystem,\
            #model=model,\
            #serial=serial,\
            #notes="octopus: "+found[0].category+";"+found[0].notes,\
            notes=notes+";"+operating_system+";"+ip,\
            last_logon=last_logon,\
            created=created,\
            in_ads=True,\
            #in_vcenters=True,\
            #in_octopus=True,\
            #in_service=in_service\
            )
            #if purchase_update:
            #db(qry).update(purchase=purchase,)
        """
        else:
            this_table.insert(
            name=name,\
            full_name=full_name,\
            types='serveur',\
            category=category,\
            ip=ip,\
            operating_system=operating_system,\
            #model=model,\
            #serial=serial,\
            #notes='',\
            #purchase=purchase,\
            #in_ads=False,\
            in_vcenters=True,\
            #in_octopus=True,\
            in_service=in_service\
            )
        """



    response.flash = T(u'terminé')
    grid=""

    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update_vms_4():
#
#in_ads=db((db.ads_computers.DNSHostName==full_name)|(db.ads_computers.DNSHostName==name)|(db.ads_computers.SamAccountName==name)).select()
#in_vms=db((db.vcenters_vm.HostName==full_name)|(db.vcenters_vm.HostName==name)).select()
#in_hosts=db((db.vcenters_host.name==full_name)|(db.vcenters_host.name==name)).select()
#in_octopus=db((db.octopus_servers.name==full_name)|(db.octopus_servers.name==name)).select()

    this_table=db.inventaire

    rows=db((db.vcenters_vm.id>0)).select()


    for row in rows:
        
        full_name=row.HostName.lower()
        name=full_name.split('.')[0]
        category='virtuel'
        ip=row.IPAddress
        operating_system=row.OSFullName
        states=row.States
        if states=="NotRunning":
            in_service=False
        else:
            in_service=True
        """
        purchase=row.date_purchase
        model=row.model
        serial=row.serial

        if purchase=='':
            purchase='1789-01-01'
            purchase_update=False
        else:
            purchase_update=True
        purchase=purchase.split('-')
        purchase=datetime.date(int(purchase[0]),int(purchase[1]),int(purchase[2]))
        """

        qry=(this_table.name==name)|(this_table.full_name==full_name)|(this_table.full_name==name)
        found=db(qry).select()
        if found:
            
            db(qry).update(
            name=name,\
            full_name=full_name,\
            types='serveur',\
            category=category,\
            ip=ip,\
            operating_system=operating_system,\
            #model=model,\
            #serial=serial,\
            #notes="octopus: "+found[0].category+";"+found[0].notes,\
            #in_ads=False,\
            in_vcenters=True,\
            #in_octopus=True,\
            in_service=in_service\
            )
            #if purchase_update:
            #db(qry).update(purchase=purchase,)
        else:
            this_table.insert(
            name=name,\
            full_name=full_name,\
            types='serveur',\
            category=category,\
            ip=ip,\
            operating_system=operating_system,\
            #model=model,\
            #serial=serial,\
            #notes='',\
            #purchase=purchase,\
            #in_ads=False,\
            in_vcenters=True,\
            #in_octopus=True,\
            in_service=in_service\
            )
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update_octopus_3():
#
#in_ads=db((db.ads_computers.DNSHostName==full_name)|(db.ads_computers.DNSHostName==name)|(db.ads_computers.SamAccountName==name)).select()
#in_vms=db((db.vcenters_vm.HostName==full_name)|(db.vcenters_vm.HostName==name)).select()
#in_hosts=db((db.vcenters_host.name==full_name)|(db.vcenters_host.name==name)).select()
#in_octopus=db((db.octopus_servers.name==full_name)|(db.octopus_servers.name==name)).select()

    this_table=db.inventaire

    rows=db((db.octopus_servers.id>0)).select()


    for row in rows:
        
        full_name=row.name.lower()
        name=full_name.split('.')[0]
        category=row.category
        ip=row.ip
        operating_system=row.os
        purchase=row.date_purchase
        model=row.model
        serial=row.serial

        if purchase=='':
            purchase='1789-01-01'
            purchase_update=False
        else:
            purchase_update=True
        purchase=purchase.split('-')
        purchase=datetime.date(int(purchase[0]),int(purchase[1]),int(purchase[2]))

        qry=(this_table.name==name)|(this_table.full_name==full_name)|(this_table.full_name==name)
        found=db(qry).select()
        if found:
            
            db(qry).update(
            name=name,\
            full_name=full_name,\
            types='serveur',\
            category=category,\
            ip=ip,\
            operating_system=operating_system,\
            model=model,\
            serial=serial,\
            notes=found[0].category+";"+found[0].notes,\
            #in_ads=False,\
            #in_vcenters=False,\
            in_octopus=True,\
            #in_service=True\
            )
            if purchase_update:
                db(qry).update(purchase=purchase,)
        else:
            this_table.insert(
            name=name,\
            full_name=full_name,\
            types='serveur',\
            category=category,\
            ip=ip,\
            operating_system=operating_system,\
            model=model,\
            serial=serial,\
            notes='',\
            purchase=purchase,\
            #in_ads=False,\
            #in_vcenters=False,\
            in_octopus=True,\
            #in_service=True\
            )



    response.flash = T(u'terminé')
    grid=""

    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update_servers_manual_2():
    #Nom;Type / catégorie;Manufacturier / modèle;No. de série;Date d'achat;
    #BDR5-LABO;virtuel;VMware, Inc, Vsphere 5.1;;2007-05-24;
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\servers_manual.txt',]
    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        this_table=db.inventaire

        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')
        
            if(len(cols)>=5): #secure with symbol ;

                full_name=cols[0].lower()
                name=full_name.split('.')[0]
                category=cols[1]
                model=cols[2]
                serial=cols[3]
                purchase=cols[4]
                

                if purchase=='':
                    purchase='1789-01-01'


                purchase=purchase.split('-')
                purchase=datetime.date(int(purchase[0]),int(purchase[1]),int(purchase[2]))


                #purchase=datetime.date(2000,1,1)


                #this_tables=[db.ads_computers,db.vcenters_vm,db.vcenters_host,db.octopus_servers]
                in_ads=db((db.ads_computers.DNSHostName==full_name)|(db.ads_computers.DNSHostName==name)|(db.ads_computers.SamAccountName==name)).select()
                in_vms=db((db.vcenters_vm.HostName==full_name)|(db.vcenters_vm.HostName==name)).select()
                in_hosts=db((db.vcenters_host.name==full_name)|(db.vcenters_host.name==name)).select()
                in_octopus=db((db.octopus_servers.name==full_name)|(db.octopus_servers.name==name)).select()

                found=db((this_table.name==name)|(this_table.full_name==full_name)).select()
                if found:
                    db((this_table.name==name)|(this_table.full_name==full_name)).update(
                        name=name,\
                        full_name=full_name,\
                        types='serveur',\
                        category=category,\
                        model=model,\
                        serial=serial,\
                        notes='',\
                        purchase=purchase,\
                        #in_ads=False,\
                        #in_vcenters=False,\
                        #in_octopus=False,\
                        #in_service=True\
                    )
                else:
                    this_table.insert(
                        name=name,\
                        full_name=full_name,\
                        types='serveur',\
                        category=category,\
                        model=model,\
                        serial=serial,\
                        notes='',\
                        purchase=purchase,\
                        #in_ads=False,\
                        #in_vcenters=False,\
                        #in_octopus=False,\
                        #in_service=True\

                    )



    response.flash = T(u'terminé')
    grid=""

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def inventory_update_servers_manual_used_1():
    #servers.DNSHostName;Type;servers.IPv4Address;servers.LastLogonDate;servers.whenCreated;servers.whenPurchase;servers.OperatingSystem
    #s-clusterfs.hlhl.rtss.qc.ca;cluster;10.129.65.104;2017-03-21;2015-02-26;;Windows Server 2012 R2 Standard;
    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\servers_manual_used_1.txt',]
    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        #lines=lines[10:30]

        this_table=db.inventaire
    
        db(this_table.id>0).delete() #to deable

        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')
        
            if(len(cols)>=7): #secure with symbol ;

                full_name=cols[0].lower()
                name=full_name.split('.')[0]
                category=cols[1]
                ip=cols[2]
                last_logon=cols[3]
                created=cols[4]
                purchase=cols[5]
                operating_system=cols[6]
                
                if last_logon=='':
                    last_logon='3000-01-01'
                if created=='':
                    created='1789-01-01'
                if purchase=='':
                    purchase='1789-01-01'

                last_logon=last_logon.split('-')
                last_logon=datetime.date(int(last_logon[0]),int(last_logon[1]),int(last_logon[2]))

                created=created.split('-')
                created=datetime.date(int(created[0]),int(created[1]),int(created[2]))

                purchase=purchase.split('-')
                purchase=datetime.date(int(purchase[0]),int(purchase[1]),int(purchase[2]))

                #last_logon=datetime.date(2000,12,31)
                #created=datetime.date(2000,1,1)
                #purchase=datetime.date(2000,1,1)


                #this_tables=[db.ads_computers,db.vcenters_vm,db.vcenters_host,db.octopus_servers]
                in_ads=db((db.ads_computers.DNSHostName==full_name)|(db.ads_computers.DNSHostName==name)|(db.ads_computers.SamAccountName==name)).select()
                in_vms=db((db.vcenters_vm.HostName==full_name)|(db.vcenters_vm.HostName==name)).select()
                in_hosts=db((db.vcenters_host.name==full_name)|(db.vcenters_host.name==name)).select()
                in_octopus=db((db.octopus_servers.name==full_name)|(db.octopus_servers.name==name)).select()

                found=db((this_table.name==name)|(this_table.full_name==full_name)).select()
                if found:
                    db((this_table.name==name)|(this_table.full_name==full_name)).update(
                        name=name,\
                        full_name=full_name,\
                        types='serveur',\
                        category=category,\
                        ip=ip,\
                        operating_system=operating_system,\
                        model='',\
                        serial='',\
                        notes='',\
                        last_logon=last_logon,\
                        created=created,\
                        purchase=purchase,\
                        #in_ads=False,\
                        #in_vcenters=False,\
                        #in_octopus=False,\
                        #in_service=True\
                    )
                else:
                    this_table.insert(
                        name=name,\
                        full_name=full_name,\
                        types='serveur',\
                        category=category,\
                        ip=ip,\
                        operating_system=operating_system,\
                        model='',\
                        serial='',\
                        notes='',\
                        last_logon=last_logon,\
                        created=created,\
                        purchase=purchase,\
                        #in_ads=False,\
                        #in_vcenters=False,\
                        #in_octopus=False,\
                        #in_service=True\
                    )



    response.flash = T(u'terminé')
    grid=""

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_serveurs'))
def tables_update():
    grid =""

    this_files=[r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_serveurs\Liste_serveurs_wanacry.txt',]

    for this_file in this_files:
        f=open(this_file,"r")
        lines=f.readlines()
        #lines=lines[10:30]

        this_table=this_table=db.inventaire
    
        #db(this_table.id>0).delete() #to deable

        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            cols=line.split(';')
        


    
    
                    



    
    response.flash = str(len(lines))
    #response.flash = T(u'terminé')
    


    
    return dict(grid=grid)


###############################################################################################






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


