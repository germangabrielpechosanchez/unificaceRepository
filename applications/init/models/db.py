# -*- coding: utf-8 -*-

#vp redirection
#if "." not in request.env.http_host:    
#    redirect("https://"+request.env.http_host+".cemtl.rtss.qc.ca")
    


# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
    
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------
from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------

#auth.define_tables(username=False, signature=False) #original

# -------------------------------------------------------------------------
# Active Directory 9
# -------------------------------------------------------------------------

from gluon.contrib.login_methods.ldap_auth import ldap_auth

auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             db = db,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             #manage_groups= True,
                                             #group_dn='OU=Security Groups,OU=Unificace,OU=Solutions,OU=PROD,DC=cemtl,DC=rtss,DC=qc,DC=ca',
                                             #group_name_attrib = 'cn',
                                             #group_member_attrib = 'member',
                                             #group_filterstr = 'objectClass=Group',
                                             server='cemtl.rtss.qc.ca',
                                             base_dn='dc=cemtl,dc=rtss,dc=qc,dc=ca',
                                             ))
auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             db = db,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             #manage_groups= True,
                                             #group_dn='OU=Groupes,OU=Unificatex,OU=CIUSSS Ressources,DC=hlhl,DC=rtss,DC=qc,DC=ca',
                                             #group_name_attrib = 'cn',
                                             #group_member_attrib = 'member',
                                             #group_filterstr = 'objectClass=Group',
                                             server='hlhl.rtss.qc.ca',
                                             base_dn='dc=hlhl,dc=rtss,dc=qc,dc=ca',
                                             ))
auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             server='hsco.net',
                                             base_dn='DC=HSCO,DC=NET',
                                             ))
auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             server='pdi.rtss.qc.ca',
                                             base_dn='DC=pdi,DC=rtss,DC=qc,DC=ca',
                                             ))
auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             server='hmr.hmr.qc.ca',
                                             base_dn='DC=hmr,DC=hmr,DC=qc,DC=ca',
                                             ))
auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             server='lteas.rtss.qc.ca',
                                             base_dn='DC=lteas,DC=rtss,DC=qc,DC=ca',
                                             ))
auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             server='icpbe.local',
                                             base_dn='dc=icpbe,dc=local',
                                             ))
auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             server='csssslsm.rtss.qc.ca',
                                             base_dn='DC=csssslsm,DC=rtss,DC=qc,DC=ca',
                                             ))
auth.settings.login_methods.append(ldap_auth(mode='ad',
                                             #manage_user=True,
                                             user_firstname_attrib='cn:1',
                                             user_lastname_attrib='cn:2',
                                             server='cemtl.gouv.qc.ca',
                                             base_dn='DC=cemtl,DC=gouv,DC=qc,DC=ca',
                                             ))

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
#icpbe
#auth.settings.login_methods.append(ldap_auth(mode='domino',server='10.128.46.21'))


#auth.settings.actions_disabled=['register','change_password','request_reset_password','retrieve_username','profile']
auth.settings.actions_disabled=['register','change_password','request_reset_password','retrieve_username','profile']
#auth.define_tables(username=False, signature=False) #original
auth.define_tables(username=True, signature=False)
auth.settings.create_user_groups=False
#auth.settings.remember_me_form = False
auth.settings.remember_me_form = True

#"""
#Clean Table
#db(db.person.id>0).delete()
#db.person.truncate()
#db.auth_user.truncate()
#db(db.auth_group.id>0).delete()
#db(db.auth_user.id>0).delete()

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------

mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False


# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


#vp
import datetime
today=datetime.date.today()
now=datetime.datetime.now()

#auth.settings.expiration = 3600*1

try: 
    auth_id=session.auth.user.id
except:
    auth_id=1

#Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('AUTHORS')),
signature = db.Table(db, 'signature',
                #Field('edit_by','integer',requires=IS_IN_SET([auth_id]),default=auth_id),
                Field('edit_by','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('Edit By')),
                Field('edit_time','datetime',default=now,writable=False),#False
                )
#temp data
db.define_table('working_data',
                Field('auth_ID','integer'),
                Field('working_data',length=4096),
                )
#Octopus User
db.define_table('oc_utilisateur',
                Field('code',requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'oc_utilisateur.code')]),
                Field('numero'),
                Field('nom'),
                Field('prenom'),
                Field('nom_famille'),
                Field('logon'),
                Field('courriel'),
                Field('telephone'),
                Field('poste'),
                Field('cell'),
                Field('site'),
                Field('departement'),
                Field('titre_emploi'),
                Field('locale'),
                Field('note'),
                Field('actif'),
                )
#windows user to octopus utilisateur
db.define_table('ad_utilisateur',
                Field('code',requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'ad_utilisateur.code')]),
                Field('utilisateur',db.oc_utilisateur,requires=IS_IN_DB(db,'oc_utilisateur.code')),
                )
#acces
db.define_table('acces',
                Field('code',requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'acces.code')]),
                Field('groupe'),
                )
#application
db.define_table('app',
                Field('code',requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'app.code')]),
                Field('acces',db.acces,requires=IS_IN_DB(db,'acces.id','acces.code')),
                #Field('acces'),
                )


db.define_table('acces_utilisateur',
                Field('groupe'),
                Field('utilisateur'),
                )

db.define_table('profil',
                Field('code',requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'profil.code')]),
                )

db.define_table('acces_profil',
                Field('acces',db.acces,requires=IS_IN_DB(db,'acces.code')),
                Field('profil',db.profil,requires=IS_IN_DB(db,'profil.code')),
                )
db.define_table('person',
                Field('auth_user',db.auth_user,requires=IS_IN_DB(db,'auth_user.id','auth_user.username')),
                Field('ad_account'),
                )

#mappage lecteur reseau link for executable
db.define_table('archives',
                Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('AUTHORS')),
                Field('archives',label=T('INSTRUCTIONS')),
                Field('dates','datetime',default=now,label=T('DATES')),
                Field('files', 'upload', uploadfield='file_data',label=T('FICHIERS'),represent=lambda value,row:A('fichier' if value else '',_href=URL('download', args=value))),
                #Field('files', 'upload', uploadfield='file_data',label=T('FILES')),
                Field('file_data', 'blob',label=T(' ')),
                Field('links', represent=lambda value,row:A('go to' if value else '',_href=value),label=T('LINKS')),
                )
#mappage table
db.define_table('mappage',
                Field('newDomaine',label=T('newDomaine'),default="hlhl.rtss.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca","cemtl.gouv.qc.ca",])),
                Field('newUsername',label=T('newUsername'),requires=IS_NOT_EMPTY()),
                Field('oldDomaine',label=T('oldDomaine'),requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",])),
                Field('OldUsername',label=T('OldUsername'),requires=IS_NOT_EMPTY()),
                Field('messages',label=T('message')), #must be message on ouput
                Field('OldShare1',label=T('OldShare1 - S:')),
                Field('OldShare2',label=T('OldShare2 - J:')),
                Field('OldShare3',label=T('OldShare3 - U:')),
                Field('OldShare4',label=T('OldShare4 - O:')),
                Field('OldShare5',label=T('OldShare5 - Z:')),
                Field('OldShare6',label=T('OldShare6 - K:')),
                Field('OldShare7',label=T('OldShare7 -I:')),
                )

#add auth_user to group
db.define_table('pre_user_to_group',
                Field('user_id',label=T('User'),requires = IS_LOWER()),
                Field('group_id','reference auth_group',label=T('Group')),
               )

#add users to group automaticly from pre_user_to_group table
user_to_group=db(db.pre_user_to_group.id>0).select()# db.pre_user_to_group.id,db.pre_user_to_group.user_id,db.pre_user_to_group.group_id
if user_to_group: # check if records existe in db.pre_user_to_group
    for utg in user_to_group:
        #msg+=str(utg_user_id)+"---"+str(utg.group_id)
        utg_user_id=(utg.user_id).lower()
        this_utg=db(db.auth_user.username==utg_user_id).select(db.auth_user.id)#if user already exist in auth_user table
        if this_utg:
            #msg+=str(this_utg[0].id)
            exist_utg=db((db.auth_membership.user_id==this_utg[0].id)&(db.auth_membership.group_id==utg.group_id)).select(db.auth_membership.id)
            if not exist_utg:
                member=db.auth_membership.insert(user_id=this_utg[0].id,group_id=utg.group_id)
                #msg+=str(utg_user_id)+"---"+str(utg.group_id)+"--- est ajoute"
            db(db.pre_user_to_group.id==utg.id).delete()#delete from pre_user_to_group
            #else:
            #    msg+=str(utg_user_id)+"---"+str(utg.group_id)+"--- existe deja"
##################
# ads        
db.define_table('department',
                Field('name',label=T('Direction'),requires = IS_UPPER()),
                Field('description',label=T('Description')),
                format='%(name)s',
                )

db.define_table('user_to_department',
                Field('user_id',label=T('User'),requires = IS_LOWER()),
                Field('department_id',db.department,requires=IS_IN_DB(db,'department.id','department.name'),label=T('Direction')),
               )

#Gestion ADs           
db.define_table('domains',
                Field('fqdn',label=T('FQDN'),requires = IS_LOWER()),
                Field('netbios',label=T('NetBIOS'),requires = IS_LOWER()),
                format='%(fqdn)s',
                )
                
db.define_table('domains_security_group',
                #Field('domain_id',db.domains,requires=IS_IN_DB(db,'domains.id','domains.fqdn'),label=T('Domaine'),default=2),
                Field('domain_id','reference domains',label=T('Domaine'),default=2),
                Field('group_name',label=T('Nom de groupe de securité'),requires = IS_UPPER()),
                Field('description',label=T('Description de groupe de securité'),requires = IS_UPPER(),comment=T("Il faut ajouter nom de domaine (CEMTL - IUSMM - HSCO - PDI - HMR - LTEAS - ICPBE - SLSM -) comme par example: IUSMM - PU_DLOG_ACHATS")),
                Field('protected', 'boolean',label=T('Protégé'),comment=T("Peut être utilisé uniquement par les administrateurs")),
                Field('department_id','reference department',label=T('Direction')),
                #format='%(domain_id)s %(department_id)s %(description)s',
                format='%(description)s',
               )

db.define_table('access_octopus',
                Field('access_id','integer',label=T("AccessID Octopus")),
                Field('title',length=100),
                Field('status_id','integer',label=T("StatusID Octopus")),
                Field('status',length=20),
                format='%(title)s ',
                )

db.define_table('access_to_domains_security_group',
                Field('access_id',db.access_octopus,requires=IS_IN_DB(db,'access_octopus.id','access_octopus.title'),label=T("Accès")),
                #Field('group_id',db.domains_security_group,requires=IS_IN_DB(db,'domains_security_group.id','%(description)s'),label=T("Groupe de securité")),
                Field('group_id','reference domains_security_group',label=T("Groupe de securité")),
                #Field('account','reference account_department',label=T('Code budgétaire')),
                #Field('group_id',db.domains_security_group,requires=IS_IN_DB(db,'domains_security_group.id','%(group_name)s - %(domain_id)s'),label=T("Groupe de securité")),
                )
#signature
db.define_table('ads_actions_tracking',
                signature,
                Field('actions',length=4048),
                )
#gestion serveurs
db.define_table('ads_computers',
                Field('DNSHostName'),
                Field('IPv4Address'),
                Field('SamAccountName'),
                Field('LastLogonDate'),
                Field('whenCreated'),
                Field('OperatingSystem'),
                Field('Enabled'),
                Field('Types',requires=IS_IN_SET(('','serveur vm','serveur physique','serveur host'))),
                Field('CanonicalName'),
                )

#"$HostName; $IPAddress;$name;$OSFullName;$State;$VMHost">> $file_Vms #States
db.define_table('vcenters_vm',
                Field('HostName'),
                Field('IPAddress'),
                Field('name'),
                Field('OSFullName'),
                Field('States'),
                Field('VMHost'),
                Field('NumCpu'),
                Field('MemoryGB'),
                Field('UsedSpaceGB'),
                Field('last_sync','date',default=datetime.date(2000,1,1)),
                )

#"$name;$version;$PowerState;$LicenseKey">> $file_hosts
db.define_table('vcenters_host',
                Field('name'),
                Field('versions'),
                Field('PowerState'),
                Field('LicenseKey'),
                Field('installedDate',length=20),
                Field('NumCpu'),
                Field('CpuUsageMhz'),
                Field('CpuTotalMhz'),
                Field('MemoryUsageGB'),
                Field('MemoryTotalGB'),
                Field('last_sync','date',default=datetime.date(2000,1,1)),
                )

db.define_table('servers',
                Field('DNSHostName'),
                Field('IPv4Address'),
                Field('LastLogonDate'),
                Field('whenCreated'),
                Field('OperatingSystem'),
                Field('name'),
                Field('OSFullName'),
                Field('States'),
                Field('nameHost'),
                Field('versions'),
                Field('LicenseKey'),
                Field('installedDate',length=20),
                )
db.define_table('octopus_servers',
                Field('name'),
                Field('category'),
                Field('ip'),
                Field('os'),
                Field('date_purchase'),
                Field('model'),
                Field('serial'),
                )

# Gestion des inventaires
db.define_table('inventaire',
                Field('name',length=500,requires=[IS_LOWER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'inventaire.name')]),
                Field('full_name',length=500,requires=[IS_LOWER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'inventaire.full_name')]),
                Field('canonical_name',length=500,requires=[IS_LOWER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'inventaire.canonical_name')]),
                #Field('hotfix',length=1000,default=''),
                #Field('hotfix_installed','boolean',default=False),
                Field('types',length=20,default='serveur',requires=IS_IN_SET(('','serveur','serveur fournisseur','serveur telephonique','autre','ordinateur','ordinateur portable','ordinateur leger','imprimante'))),
                Field('category',length=20,requires=IS_IN_SET(('','virtuel','physique','hote','cluster'))),
                Field('ip',length=500,default=''),
                Field('cpus','double'),
                Field('memory','double'),
                Field('memory_used','double'),
                Field('storages','double'),
                Field('storages_used','double'),
                Field('operating_system',length=500),
                Field('model',length=500,default=''),
                Field('serial',length=500,default=''),
                Field('roles',length=500,default=''),
                Field('department',length=500,default=''),
                Field('description',length=1000,default=''),
                Field('notes',length=1000,default=''),
                Field('infos',length=2000,default=''),
                Field('last_sync','date'),#,default=today
                Field('last_logon','date'),
                Field('created','date'),
                Field('purchase','date'),
                Field('beginning','date'),
                Field('ping','date',default=datetime.date(2000,1,1)),
                Field('in_ads','boolean',default=False),
                Field('in_vcenters','boolean',default=False),
                Field('in_octopus','boolean',default=False),
                Field('in_service','boolean',default=False),
                #Field('verified','boolean',default=False),
                Field('gestred_2017','boolean',default=False),
                )
#gestion pvs
db.define_table('pvs_prod_image',
                Field('title',length=50),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('pvs_dev_image',
                Field('title',length=50),
                Field('description',length=100),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('pvs_admin',
                Field('title',length=50),
                Field('description',length=100),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('pvs_management',
                Field('dev_name',db.pvs_dev_image,requires=IS_IN_DB(db,'pvs_dev_image.id','pvs_dev_image.title'),label=T("Nom d'image (pvs_dev_image)")),
                Field('prod_name',db.pvs_prod_image,requires=IS_IN_DB(db,'pvs_prod_image.id','pvs_prod_image.title'),label=T("Ancienne version (pvs_prod_image)")),
                Field('time_begin','datetime',label=T("Début")),
                Field('time_end','datetime',label=T("Fin")),
                Field('description',length=1024),
                Field('admin_name',db.pvs_admin,requires=IS_IN_DB(db,'pvs_admin.id','pvs_admin.title'),label=T("Admin")),
                Field('applicant',length=50,label=T("Demandeur")),
                Field('notes',length=2048),
                #Field('replace_id','integer'),
                Field('edit_by','integer',requires=IS_IN_SET([auth_id]),default=auth_id,label=T("par")),
                Field('edit_time','datetime',default=now,label=T("@")),
                )
#
db.define_table('groups',
                Field('groups_id','integer',label=T("ID Octopus")),
                Field('title',length=50),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('resources',
                Field('resources_id','integer',label=T("ID Octopus")),
                Field('title',length=50),
                Field('email',length=100),
                Field('phone_extesion',length=50),
                Field('mobile_phone',length=50),
                Field('start_time','time', default='08:00'),
                Field('end_time','time', default='16:00'),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('resource_group',
                Field('resources_id','integer',label=T("Resources")),
                Field('groups_id','integer',label=T("Groups")),
                Field('team_id','integer',label=T("ID Équipe")),
                )

db.define_table('resources_availability',
                Field('resources',db.resources,requires=IS_IN_DB(db,'resources.id','resources.title')),
                #Field('groups',db.groups,requires=IS_IN_DB(db,'groups.id','groups.title')),
                Field('time_begin','datetime',default=datetime.datetime(today.year,today.month,today.day),label=T("Début")),
                Field('time_end','datetime',default=datetime.datetime(today.year+5,today.month,today.day,23,59,59),label=T("Fin")),
                Field('bank','integer',requires=IS_INT_IN_RANGE(-2100,2100), default=1050,label=T("Banque de projet hebdomadaire en minutes (en cas absence = -1050)")),
                )

db.define_table('resources_management',
                Field('resources_id','integer',label=T("Code")),
                Field('resources',length=50),
                Field('group_id','integer',label=T("Code")),
                Field('groups',length=50),
                Field('task_id','integer',label=T("Code")),
                Field('task_number',length=15),#  ParentID-Number
                Field('estimated_begin','datetime'),
                Field('estimated_end','datetime'),
                #Field('actual_begin','datetime'),
                #Field('actual_end','datetime'),
                Field('subject',length=500),
                Field('description',length=500),
                Field('estimated_effort','integer'),
                Field('status_id','integer',label=T("Code")),
                Field('status',length=50),
                Field('separated','boolean',default=False),
                )
#resources separated weekly for report
db.define_table('resources_report',
                Field('resources_id','integer',label=T("Code")),
                Field('resources',length=50),
                Field('group_id','integer',label=T("Code")),
                Field('groups',length=50),
                Field('task_id','integer',label=T("Code")),
                Field('task_number',length=15),#  ParentID-Number
                Field('estimated_begin','datetime'),
                Field('estimated_end','datetime'),
                Field('available_time','integer'),
                Field('estimated_effort','integer'),
                Field('estimated_no_effort','integer'),
                Field('status_id','integer',label=T("Code")),
                Field('status',length=50),
                )
db.define_table('resources_reports_created',
                Field('created','date'),
                )

########### adaptation for module capacity  from resources  3 tables ***** resources<-----> capacity
#resources_management
db.define_table('capacity_availability',
                Field('resources',db.resources,requires=IS_IN_DB(db,'resources.id','resources.title')),
                Field('time_begin','datetime',default=datetime.datetime(today.year,today.month,today.day),label=T("Début")),
                Field('time_end','datetime',default=datetime.datetime(today.year+5,today.month,today.day,23,59,59),label=T("Fin")),
                Field('bank','integer',requires=IS_INT_IN_RANGE(0,2100), default=2100,label=T("Banque hebdomadaire en minutes")),
                )

db.define_table('capacity_management',
                Field('resources_id','integer',label=T("Code")),
                Field('resources',length=50),
                Field('group_id','integer',label=T("Code")),
                Field('groups',length=50),
                Field('task_id','integer',label=T("Code")),
                Field('task_number',length=15),#  ParentID-Number
                Field('estimated_begin','datetime'),
                Field('estimated_end','datetime'),
                #Field('actual_begin','datetime'),
                #Field('actual_end','datetime'),
                Field('parent_subject',length=100),
                Field('subject',length=500),
                Field('description',length=500),
                Field('estimated_effort','integer'),
                Field('status_id','integer',label=T("Code")),
                Field('status',length=50),
                Field('separated','boolean',default=False),
                Field('project','integer',default=0),
                )
#resources separated weekly for report
#resources_report
db.define_table('capacity_report',
                Field('resources_id','integer',label=T("Code")),
                Field('resources',length=50),
                Field('group_id','integer',label=T("Code")),
                Field('groups',length=50),
                Field('task_id','integer',label=T("Code")),
                Field('task_parent',length=100),
                Field('task_number',length=15),#  ParentID-Number
                Field('estimated_begin','datetime'),
                Field('estimated_end','datetime'),
                Field('available_time','integer'),
                Field('total_time','integer'),
                Field('estimated_effort','integer'),#for project
                Field('estimated_effort2','integer'),#for anothers 
                Field('estimated_no_effort','integer'),
                Field('estimated_no_effort2','integer'),
                Field('status_id','integer',label=T("Code")),
                Field('status',length=50),
                )

#resources_reports_created              
db.define_table('capacity_reports_created',
                Field('created','date'),
                )

#reservation from timeWalker gestion absence &  gestion temps
db.define_table('rs_object',
                Field('title',length=50),
                Field('description',length=100),
                Field('object_group',length=20),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )

db.define_table('rs_type',
                Field('title',length=50),
                Field('description',length=100),
                Field('color',length=50),
                Field('object_group',length=20),
                Field('is_active','boolean',default=True),
                format='%(title)s',
                )
#pour gestion absence
db.define_table('reservation',
                Field('rs_object',db.rs_object,requires=IS_IN_DB(db,'rs_object.id','rs_object.title')),
                Field('resources',db.resources,requires=IS_IN_DB(db,'resources.id','resources.title')),
                Field('rs_type',db.rs_type,requires=IS_IN_DB(db,'rs_type.id','rs_type.title')),
                #Field('task_id','integer',default=0),
                Field('title',length=1000),
                Field('description',length=4000),
                Field('time_begin','datetime'),
                Field('time_end','datetime'),
                Field('absence','integer'),
                Field('replace_id','integer'),
                Field('edit_by','integer',requires=IS_IN_SET([auth_id]),default=auth_id),
                Field('edit_time','datetime',default=now),
                #migrate=True,
                )
#db.reservation.absence=Field.Virtual('absence',lambda row: row.reservation.time_end-row.reservation.time_start)
#pour gestion temps
db.define_table('rs_details',
                Field('rs_object',db.rs_object,requires=IS_IN_DB(db,'rs_object.id','rs_object.title')),
                Field('rs_type',db.rs_type,requires=IS_IN_DB(db,'rs_type.id','rs_type.title')),
                Field('task_id','integer',default=0),
                Field('title',length=1000),
                Field('description',length=4000),
                Field('time_begin','datetime'),
                Field('time_end','datetime'),
                Field('replace_id','integer'),
                Field('edit_by','integer',requires=IS_IN_SET([auth_id]),default=auth_id),
                Field('edit_time','datetime',default=now),
                )

db.define_table('swiki',
                Field('title',length=1000),
                Field('description',length=4000),
                Field('relations_ids',length=500),
                Field('edit_time','datetime',default=now,label=T("@")),
                Field('edit_by','integer',requires=IS_IN_SET([auth_id]),default=auth_id,label=T("par")),
                )

# Gestion des factures
db.define_table('invoice_file',
                Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('AUTHORS')),
                Field('invoice_type',length=20,requires=IS_IN_SET(('Telus facture','','Telus AirtimeDetail')),default='Telus facture',label=T('FACTURE')),
                #Field('invoice_number',length=50,requires=[IS_LOWER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'invoice_file.invoice_number')],label=T('NUMERO DE FACTURE')),
                Field('invoice_number',default='',label=T('NUMERO DE FACTURE'),writable=False),
                Field('dates','date',label=T('DATES'),writable=False),
                Field('description',length=200,default='',requires=IS_NOT_EMPTY(),label=T('DESCRIPTION')),
                Field('imported','boolean',default=False,label=T('IMPORTÉ')),#,writable=False
                Field('exported','boolean',default=False,label=T('EXPORTÉ')),#,writable=False
                Field('sent','boolean',default=False,label=T('ENVOYÉ')),#,writable=False
                Field('files', 'upload', uploadfield='file_data',label=T(' '),comment=T("Le fichier de facture de Telus en format texte"),represent=lambda value,row:A('facture en text' if value else '',_href=URL('download', args=value))),
                #Field('files', 'upload', uploadfield='file_data',label=T('FILES')),
                Field('file_data', 'blob',label=T(' ')),
                Field('files_pdf', 'upload', uploadfield='file_data_pdf',label=T(' '),comment=T("Le fichier de facture de Telus en format pdf (1er page seulement)"),represent=lambda value,row:A('facture en pdf (1er page)' if value else '',_href=URL('download', args=value))),
                Field('file_data_pdf', 'blob',label=T(' ')),
                Field('files_csv', 'upload', uploadfield='file_data_csv',label=T(' '),comment=T("Le fichier pour la comptablilité en csv"),represent=lambda value,row:A('fichier pour la comptablilité en csv' if value else '',_href=URL('download', args=value))),
                Field('file_data_csv', 'blob',label=T(' ')),
                Field('links', represent=lambda value,row:A('go to' if value else '',_href=value),label=T('LINKS')),
                 )
# 0 * Client Number; 1 * Bill Date; 2 * Billing Name; 3 * Additional Line of Billing Name; 4 * Purchase Order Number; 5 * Bill Number; 6 * Product Type; 
# 7 * User; 8 * Sub Level A Name; 9 * Sub Level B Name; 10 * User Name; 11 * Additional User Name; 12 * Reference 1;
# 13 * Reference 2; 14 * Adjustments; 15 * Adjusted HST; 16 * Adjusted PST/QST; 17 * Adjusted GST; 18 * Service Plan Name; 
# 19 * Service Plan Price; 20 * Additional Local Airtime; 21 * Over/Under; 22 * Contribution to Pool; 23 * Phone Long Distance Charges; 24 * Private/Group Long Distance Charges;
# 25 * Roaming Charges; 26 * Data and Other Services; 27 * Voice Services; 28 * Pager Services; 29 * Value Added Services; 30 * Other Charges and Credits;
# 31 * Network and Access; 32 * HST - BC; 33 * HST - AB; 34 * HST - SK; 35 * HST - MB; 36 * HST - ON; 37 * HST - PE; 38 * HST - NB; 39 * HST - NS; 40 * HST - NT; 41 * HST - NF; 42 * HST - PQ; 43 * HST - YT; 44 * HST - NU; 45 * PST - BC; 46 * PST - AB; 47 * PST - SK; 48 * PST - MB; 49 * PST - ON; 50 * PST - PE;
# 51 * QST; 52 * Subtotal before GST; 53 * GST; 54 * Total Current Charges; 55 * Total Charges and Adjustments; ×

# 0 * 31564264; 1 * 2017-07-14; 2 * GACEQ - CIUSSS DE; 3 * L'EST-DE-L'ILE-DE-MONTREAL; 4 * ; 5 * 031564264013; 6 * C; 7 * 5142362453; 8 * IUSMM; 9 * 7340205; 10 * VILOUNHA PHANALASY; 11 * ; 12 * ; 13 * ; 14 * 0.00; 15 * 0.00; 16 * 0.00; 17 * 0.00; 18 * GACEQ voice plan; 19 * 0.75; 20 * 2.25; 21 * Under; 22 * 0.00; 23 * 0.00; 24 * 0.00; 25 * 0.00; 26 * 29.00; 27 * 0.00; 28 * 0.00; 29 * 2.00; 30 * 0.00; 31 * 0.00; 32 * 0.00; 33 * 0.00; 34 * 0.00; 35 * 0.00; 36 * 0.00; 37 * 0.00; 38 * 0.00; 39 * 0.00; 40 * 0.00; 41 * 0.00; 42 * 0.00; 43 * 0.00; 44 * 0.00; 45 * 0.00; 46 * 0.00; 47 * 0.00; 48 * 0.00; 49 * 0.00; 50 * 0.00; 51 * 3.38; 52 * 37.38; 53 * 1.70; 54 * 39.08; 55 * 39.08; ×



db.define_table('invoices',
                Field('Client_Number',label=T('# Reférence')),#0
                Field('Bill_Date',label=T('Date de facturation')),#1
                Field('Bill_Number',label=T('Numéro de facture')),#5
                Field('Product_Type',label=T('Type de produit')),#6
                Field('User_Number',label=T("Numéro d'utilisateur")),#7
                Field('Sub_Level_A_Name'),#8
                Field('Sub_Level_B_Name',label=T('Code budgétaire')),#9
                Field('User_Name',label=T("Nom d'utilisateur")),#10
                Field('Reference_1'),#12
                Field('Service_Plan_Price','double'),#19
                Field('Additional_Local_Airtime','double',label=T("Air time")),#20
                Field('Phone_Long_Distance_Charges','double',label=T("Long distance")),#23
                Field('Private_Group_Long_Distance_Charges','double'),#24
                Field('Roaming_Charges','double',label=T("Roaming")),#25
                Field('Data_and_Other_Services','double',label=T("Data")),#26
                Field('Value_Added_Services','double',label=T("Value added")),#29
                Field('QST','double'),#51
                Field('Subtotal_before_GST','double'),#52
                Field('GST','double'),#53
                Field('Total_Current_Charges','double'),#54
                Field('Total_Charges_and_Adjustments','double',label=T("Total")),#55
                )

db.define_table('airtime_invoices',
                Field('Numero_facture',label=T("Numéro de facture")),#6
                Field('Date_facturation',label=T("Date de facturation")),#2
                Field('Numero_appareil',label=T("Numéro d'appareil")),#9
                Field('Nom_utilisateur',label=T("Nom de l'utilisateur")),#10
                Field('appel',label=T("# appel")),#15
                Field('Dates',label=T("Date")),#16
                Field('Heure',label=T("Heure")),#17
                Field('Periode_appel',label=T("Période d'appel")),#18
                Field('De',label=T("De")),#19
                Field('Numero_appele',label=T("Numéro appelé")),#20
                Field('A_',label=T("À")),#21
                Field('Type_appel',label=T("Type d'appel")),#22
                Field('Duree',label=T("Durée")),#23
                Field('Frais_temps_antenne',label=T("Frais de temps d'antenne")),#24
                Field('Frais_temps_antenne_local',label=T("Frais de temps d'antenne local")),#25
                Field('Frais_interurbain',label=T("Frais d'interurbain")),#26
                Field('Frais_appels_additionnels',label=T("Frais d'appels additionnels")),#27
                Field('Total',label=T("Total")),#28
                )

db.define_table('account_department',
                #Field('account',label=T('Code budgétaire'),requires=IS_MATCH('[0-9]+')),
                Field('account',label=T('Code budgétaire'),requires=[IS_MATCH('[0-9]+'),IS_NOT_IN_DB(db,'account_department.account')]),
                #Field('account',label=T('Code budgétaire')),
                Field('department',label=T('Département')),
                Field('account_type',label=T('Catégorie'),requires=IS_IN_SET(('','100171','100172','100175','100132'))),
                Field('account_nature',label=T('Nature'),default="5315"),
                Field('date_begin','date',default=datetime.datetime(today.year,today.month,today.day),label=T("Date effective")),
                Field('date_end','date',default=datetime.datetime(3000,1,1),label=T("Date fin")),
                Field('is_active','boolean',default=True),
                format='%(account)s %(department)s %(account_type)s Active: %(is_active)s',
                )

db.define_table('client_departments',
                Field('account','reference account_department',label=T('Code budgétaire')),
                Field('client_number',label=T('Numéro de téléphone'),requires=IS_MATCH('[0-9]+')),#,requires=IS_MATCH('[0-9]+')
                Field('client_name',label=T("Nom d'utilisateur")),
                Field('account_type',label=T('Forfait'),requires=IS_IN_SET(('','voix et données','données','voix'))),#IS_IN_SET(('','Téléphones cellulaires (forfait voix ou voix et données)', 'Clés internet (forfait données)', 'Tablettes LTE (forfait données) ', 'Portables avec carte SIM intégrée (forfait données)')))
                Field('device_type',label=T('Équipement'),requires=IS_IN_SET(('','Téléphone cellulaire','Clé internet','Tablette LTE','Portable avec carte SIM intégrée'))),
                Field('infos',length=50,label=T("Information supplémentaire")),
                Field('employee_number',length=10,label=T("Numro d'employé")),
                Field('job_tilte',length=100,label=T("Titre d'emploi")),
                #Field('old_account'),
                Field('date_begin','date',default=datetime.datetime(today.year,today.month,today.day),label=T("Date effective")),
                Field('date_end','date',default=datetime.datetime(3000,1,1),label=T("Date fin")),
                Field('is_active','boolean',default=True,comment="Appliqué sur cette période"),
                )

db.define_table('managers',
                Field('windows_code',default='',label=T("Code Windows du gestionnaire"),requires=IS_LOWER()),
                Field('name',label=T('Gestionnaire'),requires=IS_UPPER()),
                Field('email',length=200),
                Field('notification',label=T('Notification'),default="",requires=IS_IN_SET(("","CS","DA","DD"))),
                Field('is_active','boolean',default=True),
                format='%(name)s %(windows_code)s Active: %(is_active)s',
               )

db.define_table('managers_to_account',
                Field('manager','reference managers',label=T("Gestionnaire")),
                Field('account','reference account_department',label=T('Code budgétaire')),
               )

db.define_table('cap_file',
                Field('Type_transaction',default=''),#1 A
                Field('Nombre_enregistrements',default=''),#2 B
                Field('No_founisseur',default=''),#3 C
                Field('No_facture',default=''),#4 D
                Field('Entite_principale',default=''),#5 E
                Field('Description_facture',default=''),#6 F
                Field('Entite_principale2',default=''),#7 G
                Field('Periode_financiere',default=''),#8 H
                Field('Date_facture',default=''),#9 I               
                Field('Date_echeance',default=''),#10 J
                Field('Date_escompte',default=''),#11 K
                Field('Montant_total',default=''),#12 L
                Field('Reference_externe',default=''),#13 M
                Field('Description_article',default=''),#14 N
                Field('Entite_legale_CF',default=''),#15 O
                Field('Entite_legale_article',default=''),#16 P
                Field('Compte_GL_Financier',default=''),#17 Q
                Field('Code_primaire',default=''),#18 R
                Field('Code_secondaire',default=''),#19 S
                Field('Montant',default=''),#20 T
                Field('Unites',default=''),#21 U
               )

#Place this to the last 
# Gestion des VMs

### by pass error of mssql of this line Field('datastore','reference vmw_datastore',label=T("datastore")),
#for key in ['reference', 'reference FK']:
#    db._adapter.types[key]=db._adapter.types[key].replace('%(on_delete_action)s', 'NO ACTION')
###

db.define_table('vms_folders',
                Field('paths',length=1024),
                Field('folder_id'),
                Field('types'),
                #Field('datacenter_id'),
                #Field('is_active','boolean',default=False),
                )
#table tempo exchange data for more apps
db.define_table('app2app',
                Field('publish_id',length=50,default=''),
                Field('subscribe_id',length=50,default=''),
                Field('app',default='',requires=IS_IN_SET(('gestion_vms','gestion_factures','mappage_reseau','actualisation_inventaires','mappage_reseau_test'))),
                Field('status',default='',requires=IS_IN_SET(('new','pending','donne','scheduling','canceled'))),
                Field('command',length=1024,default=''),
                Field('response',length=4096,default=''),
                )

# Gestion des retrofactures
db.define_table('ci_octopus',
                Field('ci_id','integer',label=T('#')),
                Field('name',label=T('CI')),
                Field('type_id','integer',label=T('Type ID')),
                Field('ci_type',label=T('Type')),
                Field('account_code',label=T('RF - Centre de coûts initial')),
                Field('grm_code',label=T('RF - GRM initial')),
                #Field('account','reference account_department',label=T('Code budgétaire')),
                Field('purchase_price','double',label=T("Prix d'achat")),
                Field('purchase_dates','date',label=T("Date d'achat")),
                Field('descriptions',label=T('Descriptions')),
                )

db.define_table('ci_payment',
                Field('ci_id','integer',label=T('#')),
                Field('name',label=T('CI')),
                Field('type_id','integer',label=T('Type ID')),
                Field('ci_type',label=T('Type')),
                Field('code_ecriture',label=T("Code d'ecriture")),
                Field('account_code',label=T('RF - Centre de coûts initial')),
                Field('grm_code',label=T('RF - GRM initial')),
                #Field('unit',db.unit,requires=IS_IN_DB(db,'unit.id','unit.title')),
                Field('account','reference account_department',label=T('Code budgétaire')),
                #Field('account',db.account_department,requires=IS_IN_DB(db,'account_department.id','account_department.account'),label=T('Code budgétaire')),
                #Field('account_name',label=T('Code budgétaire description')),
                Field('purchase_price','double',label=T("Prix d'achat")),
                Field('purchase_dates','date',label=T("Date d'achat")),
                Field('imported','date',default=datetime.datetime(today.year,today.month,today.day),label=T("Date d'importation")),
                Field('exported','date',default=datetime.datetime(3000,1,1),label=T("Date d'exportation")),
                Field('to_update','boolean',default=False,label=T("Prêt à sychroniser avec Octupus")),
                Field('completed','date',default=datetime.datetime(3000,1,1),label=T("Terminé")),
                Field('descriptions',label=T('Descriptions')),
                )

db.define_table('ci_type',
                Field('type_id','integer',label=T('Type ID')),
                Field('name',label=T('Type')),
                Field('code_ecriture',label=T("Code d'ecriture"),requires=IS_IN_SET(('5325','5330','5430'))),
                Field('is_active','boolean',default=True),
                )

db.define_table('ci_files',
                Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('AUTHORS')),
                Field('dates','date',label=T('DATES'),writable=False),
                Field('description',length=200,default='',requires=IS_NOT_EMPTY(),label=T('DESCRIPTION')),
                Field('files_csv', 'upload', uploadfield='file_data_csv',label=T(' '),comment=T("Fichier pour la comptablilité en csv"),represent=lambda value,row:A('Fichier pour la comptablilité en csv' if value else '',_href=URL('download', args=value))),
                Field('file_data_csv', 'blob',label=T(' ')),
                Field('files_octopus', 'upload', uploadfield='file_data_octopus',label=T(' '),comment=T("Historique de la MAJ Octoupus"),represent=lambda value,
                row:A('Historique de la MAJ Octoupus' if value else '',_href=URL('download', args=value)),writable=False),
                Field('file_data_octopus', 'blob',label=T(' ')),
                Field('file3', 'upload', uploadfield='file_data3',label=T(' '),comment=T("Fichier log"),represent=lambda value,row:A('Fichier log' if value else '',_href=URL('download', args=value)),writable=False),
                Field('file_data3', 'blob',label=T(' ')),
                )

#Gestion des importation vers Octopus
db.define_table('oct_template_files',
                Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('AUTHORS')),
                Field('types',length=100,default='CI',requires=IS_IN_SET(('CI','CI_Clear','CIAttachement','CIAttribut','CIRelation','CIType','CIUser'))),
                Field('files', 'upload', uploadfield='file_data',label=T(' '),comment=T("Télécharger ce template, compléter et téléverser vers <<l'entrepot des fichier d'importation>>"),represent=lambda value,row:A("Télécharger ce template, compléter et téléverser vers <<l'entrepot des fichier d'importation>>" if value else '',_href=URL('download', args=value))),
                Field('file_data', 'blob',label=T(' ')),
                )

db.define_table('oct_support_team',
                Field('oct_number','integer',label=T('Numéro')),
                Field('name',length=50,label=T('Nom')),
                format='%(name)s',
                )

db.define_table('oct_importation_files',
                Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('Par')),
                Field('team','reference oct_support_team',default=1,label=T('Équipe')),
                Field('types',length=100,default='CI',requires=IS_IN_SET(('CI','CI_Clear','CIAttachement','CIAttribut','CIRelation','CIType','CIUser','USER','USER_Clear','GROUPMEMBER'))),
                Field('dates','datetime',default=now,label=T('Date')),
                Field('description',length=200,default='',requires=IS_NOT_EMPTY(),label=T('Description')),
                Field('files', 'upload', uploadfield='file_data',label=T(' '),comment=T("Ficher à importer (le fichier doit être en format CSV point-virgule; en Excel vous devez enregister sous CSV point-virgule)"),represent=lambda value,row:A('Ficher à importer' if value else '',_href=URL('download', args=value))),
                Field('file_data', 'blob',label=T(' ')),
                Field('imported','boolean',default=False,label=T("Importé"),comment=T("Vide = Ça veut dire le fichier est prêt à importer ou à reimporter")),
                Field('file2', 'upload', uploadfield='file_data2',label=T(' '),comment=T("Fichier CSV transformé et importé"),represent=lambda value,row:A('Fichier CSV importé' if value else '',_href=URL('download', args=value)),writable=False),
                Field('file_data2', 'blob',label=T(' ')),
                Field('file3', 'upload', uploadfield='file_data3',label=T(' '),comment=T("Fichier log"),represent=lambda value,row:A('Fichier log' if value else '',_href=URL('download', args=value)),writable=False),
                Field('file_data3', 'blob',label=T(' ')),
                )
# Gestion des écrans d'affichage
db.define_table('computer',
                Field('ip'),
                Field('name'),
                Field('screen_height','integer'),
                Field('screen_width','integer'),
                Field('sync','datetime'),
                Field('command'),
                Field('messages',length=1024),
                Field('links', represent=lambda value,row:A('Copiez ce lien pour modifier le script sur Raspberry Pi' if value else '',_href=value),label=T('LINKS')),
                )

# Gestion des courriels
db.define_table('emails_file',
                Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('AUTHORS')),
                #Field('dates','date',default=datetime.datetime(today.year,today.month,today.day),label=T('DATES')),
                Field('dates','datetime',default=now,label=T('DATES')),
                Field('description',length=200,default='',requires=IS_NOT_EMPTY(),label=T('DESCRIPTION')),
                Field('imported','boolean',default=False,label=T('IMPORTÉ')),
                #Field('exported','boolean',default=False,label=T('ENVOYÉ')),
                Field('files', 'upload', uploadfield='file_data',label=T(' '),comment=T("Le fichier des courriels format txt à envoyer (Il faut exporter le fichier excel en format de text séparé par des tabulations)"),represent=lambda value,row:A('courriels en txt' if value else '',_href=URL('download', args=value))),
                Field('file_data', 'blob',label=T(' ')),
                #Field('links', represent=lambda value,row:A('go to' if value else '',_href=value),label=T('LINKS')),
                )

db.define_table('emails_records',
                Field('recipient',default='',label=T('to')),
                Field('cc',default='',label=T('cc')),
                Field('bcc',length=500,default='',label=T('bcc')),
                Field('subject',default='',label=T('subject')),
                Field('attachments',default='',label=T('attachments')),
                Field('reply_to',default='',label=T('reply_to')),
                Field('messages',length=3000,default='',label=T('messages')),
                Field('created','datetime',default=now,label=T("IMPORTÉ")),
                Field('sent','datetime',default=datetime.datetime(3000,1,1),label=T("ENVOYÉ"),comment=T("Par défaut: 3000-01-01 00:00:00")),
                Field('emails_file','integer',label=T('ID du fichier')),
                )

db.define_table('emails_attachments',
                Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('AUTHORS')),
                Field('dates','datetime',default=now,label=T('DATES')),
                Field('description',length=200,default='',requires=IS_NOT_EMPTY(),label=T('DESCRIPTION')),
                Field('files', 'upload',label=T(' '),comment=T("Le fichier d'attachement a envoyer")),
                Field('to_send','boolean',default=True,label=T('A ENVOYER')),
                )

#gestion de mapappage d'imprimante
db.define_table('gmi_printers',
                Field('name',length=50,requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'gmi_printers.name')],label=T('Imprimante'),comment=T("")),
                Field('url',length=50,requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'gmi_printers.url')],label=T('Lien pour le mappage'),comment=T(r'Par example:  \\\\S-PRINT2\BE-116-32-060007 ou \\\\10.129.64.135\BE-116-32-060007')),
                Field('description',length=200),
                Field('is_active','boolean',default=True),
                format='%(name)s Active: %(is_active)s',
                )

db.define_table('gmi_thins',
                Field('name',length=50,requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'gmi_thins.name')],label=T('Client léger'),comment=T("")),
                Field('url',length=50,requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'gmi_thins.url')],label=T('FQDN'),comment=T("Par example: tc056351.hlhl.rtss.qc.ca")),
                Field('description',length=200),
                Field('is_active','boolean',default=True),
                format='%(name)s Active: %(is_active)s',
                )

db.define_table('gmi_locations',
                Field('name',length=50,requires=[IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'gmi_locations.name')],label=T('Emplacement'),comment=T("Par example: Bedard - Aile 216 - unité 1")),
                Field('description',length=200),
                Field('is_active','boolean',default=True),
                format='%(name)s Active: %(is_active)s',
                )

db.define_table('gmi_printers_locations',
                Field('printer','reference gmi_printers',label=T("Imprimante")),
                Field('locations','reference gmi_locations',label=T('Emplacement')),
                Field('default_printer','boolean',default=False,label=T("Imprimante par défaut")),
                #Field('is_active','boolean',default=True),
                )

db.define_table('gmi_thin_location',
                Field('thin','reference gmi_thins',label=T("Client léger")),
                Field('locations','reference gmi_locations',label=T('Emplacement')),
                #Field('is_active','boolean',default=True),
                )

#gestion_acces_generique
db.define_table('account_generique',
                Field('name',length=15,requires=[IS_LOWER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'account_generique.name')],label=T("Nom d'utilisateur Windows")),
                Field('domains','reference domains',label=T('Domaine')),
                Field('description',length=255),
                Field('is_active','boolean',default=True),
                Field('status',length=255),
                )

#gestion_motdepasse
db.define_table('employees',
                Field('employee_id','integer',label=T("ID Octopus")),
                Field('full_name',length=50),
                Field('first_name',length=50),
                Field('last_name',length=50),
                Field('logon',length=500),
                Field('email',length=200),
                Field('unificace',requires = CRYPT(key='sha512:canada+laos',salt='canada+laos')),
                Field('employee_number',length=50),
                Field('job_title',length=150),
                Field('phone_extesion',length=50),
                Field('mobile_phone',length=50),
                Field('office',length=70),
                Field('is_active','boolean',default=True),
                Field('email_checked','boolean',default=False),
               format='%(full_name)s',
                )

db.define_table('inv_type_ci',
                Field('name',label=T('Type et catégorie'),comment=T('Format: Type;Catégorie')),
                format='%(name)s',
                )

#gestion_inventaires

db.define_table('inv_status',
                Field('name',label=T('État')),
                format='%(name)s',
                )

db.define_table('inv_location',
                Field('name',label=T('Local')),
                Field('printer',label=T('Imprimante'),requires=IS_NOT_EMPTY(),comment=T('Format: IP imprimante grand étiquette;IP imprimante petit étiquette')),
                format='%(name)s',
                )

db.define_table('inv_supplier',
                Field('name',label=T('Fournisseur')),
                Field('phone',length=50),
                #Field('fax',length=50),
                format='%(name)s',
                )

db.define_table('inv_manufacturer',
                Field('name',label=T('Fabriquant')),
                format='%(name)s',
                )

db.define_table('inv_model',
                Field('type_ci','reference inv_type_ci',label=T('Type')),
                Field('manufacturer','reference inv_manufacturer',label=T('Fabriquant')),
                Field('name',label=T('Modèle')),
                format='%(name)s',
                )

db.define_table('inv_funding_source',
                Field('name',label=T('Source de financement')),
                format='%(name)s',
                )

db.define_table('inv_warranty_type',
                Field('name',label=T('Type de garantie')),
                format='%(name)s',
                )

db.define_table('inv_depreciation_period',
                Field('name','integer',label=T("Durée d'amortissement")),
                format='%(name)s',
                )

db.define_table('inv_cis',
                Field('Nom'),
                Field('impression','boolean',default=False,label=T("Imprimé")),
                Field('impression_index','integer',label=T('Location sur la page'),default=1,requires = IS_INT_IN_RANGE(1,11),comment="Il y a 5 lignes et 2 colonnes. Exemple: les emplacements 1 et 2 sont sur la première ligne (la plus bas) et les emplacements 9 et 10 sur la 5ème ligne."),
                Field('importation','boolean',default=False,label=T("Importé")),
                Field('AdresseIP',default='',label=T("Adresse IP")),
                Field('infos',default='',label=T("Numéro Fax pour imprimante / Numéro téléphone pour Ligne mobile")),# can be use as json string and use grid validation: try with json.load  for valide dictionnary
                Field('Compteur'),
                Field('Total'),
                Field('NumeroBonCommande'),
                Field('Requete'),
                Field('CentreDeCouts'),
                Field('NumeroSerie'),
                Field('DateAchat','date',default=today),
                Field('TypeCi',requires=IS_IN_DB(db,'inv_type_ci.name')),
                Field('AdresseMAC'),
                Field('imei',label=T("IMEI")),
                Field('Fournisseur'),
                Field('Manufacturier'),
                Field('grm_code',label=T("RF - GRM")),
                Field('Modele'),
                Field('Site'),
                Field('Locals'),
                Field('Etat'),
                Field('Dimension'),
                Field('SourceDeFinancement'),
                Field('TypeDeGarantie'),
                Field('DureeDAmortissement'),
                Field('CoutDAchat'),
                Field('NoDeFacture'),
                Field('ExpirationDeLaGarantie'),
                signature,
                )


#db.define_table('inv_label_table',
#                Field('Nom'),
#                Field('Compteur'),
#                Field('Total'),
#                Field('NumeroBonCommande'),
#                Field('Requete'),
#                Field('NumeroSerie'),
#                Field('NBITEMCommmande'),
#                )

db.define_table('inv_label_files',
                Field('user_id','reference auth_user',default=auth_id,requires=IS_IN_SET([auth_id]),label=T('AUTHORS')),
                #Field('files', 'upload', uploadfield='file_data',label=T(' '),comment=T("Pour reimprimer ces étiquettes, télécharger ce fichier et sauvegarder comme <<\\cemtl.rtss.qc.ca\cemtl\Ressources\Public\unificace_gestion_inventaires\inv_label_file.csv>>"),represent=lambda value,row:A("Pour reimprimer ces étiquettes, télécharger ce fichier et sauvegarder comme <<\\cemtl.rtss.qc.ca\cemtl\Ressources\Public\unificace_gestion_inventaires\inv_label_file.csv>>" if value else '',_href=URL('download', args=value))),
                Field('files', 'upload', uploadfield='file_data',label=T(' '),comment=T("doc.pdf"),represent=lambda value,row:A("doc.pdf" if value else '',_href=URL('download', args=value))),
                Field('file_data', 'blob',label=T(' ')),
                #Field('impression','boolean',default=False,label=T("Imprimé")),
                )

#from myutils import crypt as CRYPT
#db.employees.unificace2.filter_in = lambda data: CRYPT('encrypt', data, iv_random=False)
#db.employees.unificace2.filter_out = lambda data: CRYPT('decrypt', data, iv_random=False)
#gestion_alias

#actualisation_inventaires
db.define_table('act_cis',
                signature,
                Field('selected','boolean',default=False,label=T("Sélectionné")),
                Field('name',default='',label=T("Nom du CI")),
                Field('description',length=2048,default='',label=T("Description")),
                Field('disabled','boolean',default=False,label=T("Désactivé")),
                Field('imported','boolean',default=False,label=T("Importé"),writable=False),
                Field('date_disabled','date',default=today,label=T("Désactivé à")),
                Field('days_delete','integer',label=T('Sera supprimé dans [jours]'),default=3,requires = IS_INT_IN_RANGE(1,8),comment="Le CI sera supprimé automatiquement dans x jour(s) après désactivation."),
                Field('reactivated','boolean',default=False,label=T("Réactivé"),writable=False),
                Field('deleted','boolean',default=False,label=T("Supprimé"),writable=False),
                )

#gestion_impression
db.define_table('pdfs_printers',
                Field('pdf_folder',requires=IS_NOT_EMPTY(),label=T("Partage de PDFs")),
                Field('url_printers',requires=IS_NOT_EMPTY(),label=T("URLs du imprimante"),comment="URLs du imprimante séparé par <<;>>, par example: \\\\s-print2\la-507-16-060020;\\\\s-print2\LA-507-00-054056"),
                Field('is_active','boolean',default=True),
                )

#mysql file
db.define_table('mysql_files',
                Field('submit_time_id','decimal(16,4)'),
                Field('submit_time','datetime'),
                Field('form_name',default=''),
                Field('field_name',default=''),
                Field('field_value',default=''),
                Field('field_order','integer'),
                Field('full_name',default=''),
                Field('unique_file_name',default=''),
                #Field('files', 'upload', default=r'\\s03VWdv00004\files_from_table'),
                Field('links', represent=lambda value,
                row:A("Cliquer sur ce lien pour consulter" if value else '',_href="https://"+request.env.http_host+"/init/gestion_fichiers/load_file/"+value),label=T('LINKS')),
                )


