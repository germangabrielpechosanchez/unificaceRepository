# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

###############################

################################

response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Rétrofacturation du compte bilan"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]), 
        (T('Importation'), False, URL( f='importation'),[]),
        (T('Validation'), False, URL( f='validation'),[]),
        (T('Exportation'), False, URL( f='exportation'),[]),
        (T('Entrepôt des fichiers'), False, URL( f='ci_files'),[]),
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        #(T('Importation des données'), False, URL( f='import_data'),[]),
        ]),
    
    ]
import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()

if auth.is_logged_in():
    if (auth.has_membership(role='admin')): #auth.has_membership(role='gestion_retrofacturation_edit_add')
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_retrofacturation')): #auth.has_membership(role='gestion_retrofacturation_edit_add')
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_retrofacturation_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_retrofacturation_edit')):
        create=False
        deletable=False
        editable=True
        user_signature=False
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
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        ]
    grid=""
    session.this_manager=False
    
    return dict(grid=grid)

def escape(arg1):
    #arg1=arg1.upper()
    arg1=arg1.replace("À","A")
    arg1=arg1.replace("Â","A")
    arg1=arg1.replace("Ç","C")
    arg1=arg1.replace("É","E")
    arg1=arg1.replace("Ê","E")
    arg1=arg1.replace("È","E")
    return arg1


@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add'))
def importation():
    #read data from Octopus
    #"""
    import subprocess 
    script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\read_octopus_retrofacturation.py'
    p1 = subprocess.Popen([r'C:\python27\python.exe',script],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,error = p1.communicate()
    #"""
    rs=db(db.ci_octopus.id).select()
    #db(db.ci_payment.ci_id).delete() #test
    for r in rs:
        found=db(db.ci_payment.ci_id==r.ci_id).select()
        if found:
            #db(db.ci_payment.ci_id==r.ci_id).delete()
            to_update=True
        else:
            to_update=False
        #find account in the list 
        found=db(db.account_department.account==r.account_code).select()
        if found:
            account=found[0].id
            #department=a.department
        else:
            account=9679
            #department='xxx'
        #check ci_type
        found=db(db.ci_type.type_id==r.type_id).select()
        if found:
            code_ecriture=found[0].code_ecriture
        else:
            code_ecriture='5430'
                        
        if to_update:
            #active this for demo 
            #in production must be disable (not export same item two time)
            #"""
            db(db.ci_payment.ci_id==r.ci_id).update(
                ci_id=r.ci_id,
                name=r.name,
                type_id=r.type_id,
                ci_type=r.ci_type,
                code_ecriture=code_ecriture,
                account_code=r.account_code,
                account=account,
                #account_name=account_name,
                purchase_price=r.purchase_price,
                purchase_dates=r.purchase_dates,
                imported=today,
                #exported=datetime.date(3000,1,1),
                #exported=datetime.date(3000,1,1),
            )
            #""" 
            #pass          
        else:    
            db.ci_payment.insert(
                ci_id=r.ci_id,
                name=r.name,
                type_id=r.type_id,
                ci_type=r.ci_type,
                code_ecriture=code_ecriture,
                account_code=r.account_code,
                account=account,
                #account_name=account_name,
                purchase_price=r.purchase_price,
                purchase_dates=r.purchase_dates,
                imported=today,
                exported=datetime.date(3000,1,1),
            )
    
    redirect(URL('validation'))   
    return dict()

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add'))
def validation():
    response.menu = [
    (response.menu[0]), #Home - Page d'accueil
    (response.menu[1]), #Gestion des factures
    (T('Validation'), False, URL( f='validation'),[]),
    ]
    grid =""
    #qry=db.ci_payment
    qry=(db.ci_payment.exported==datetime.date(3000,1,1))|(db.ci_payment.exported==today)
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=deletable,editable=editable,create=False,user_signature=user_signature,searchable=searchable,details=details)

    return dict(grid=grid)

def date_financial(date):
    if date.month>3:
        year=date.year+1
        ref=datetime.date(date.year,4,30)
    else:
        year=date.year
        ref=datetime.date(date.year-1,4,30)
    weekday=ref.weekday()
    if weekday<6:
        const=-weekday-2
    else:
        const=-1
    ref=datetime.date(ref.year,ref.month,ref.day+const)
    period=((date-ref).days-1)/28+2
    if period>13:period=13
    return (year,period)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add'))
def exportation():       
    import os

    file_name='retrofacturation_'+str(now).replace('.','').replace(':','').replace(' ','')+'.csv'
    this_file=open(file_name, 'w')
    rs=db((db.ci_payment.exported==datetime.date(3000,1,1))|(db.ci_payment.exported==today)).select()
    #mark exported
    db(db.ci_payment.exported==datetime.date(3000,1,1)).update(exported=today)
    date_finan=date_financial(today)
    line="10;;"+str(session.auth.user.username)+";"+str(date_finan[0])+";"+str(date_finan[1])+";"+str(datetime.date.today()).replace('-','')+";1001;G20;Sortie d'inventaire equipements informatiques\r\n"
    this_file.write(line)
    total=0
    for r in rs:
        purchase_price=r.purchase_price
        total-=purchase_price
        account_code=db(db.account_department.id==r.account).select(db.account_department.account).first().account
        line="20;;;;;;;;;"+r.ci_type+"-"+r.name+";1001;;"+account_code+";"+r.code_ecriture+";"+str(purchase_price)+"\r\n"
        this_file.write(line)
    line="20;;;;;;;;;Sortie d'inventaire equipements informatiques;1001;100111150095;;;"+str(total)+"\r\n"
    this_file.write(line)
    line="99;"+str(len(rs)+3)+";;;;;;;;;;;;;\r\n"
    this_file.write(line)
    this_file.close()
    this_file=open(file_name, 'r')
    r=db(db.ci_files.dates==today).select()
    if r:
        db(db.ci_files.dates==today).update(files_csv=db.ci_files.files_csv.store(this_file,file_name),file_data_csv=this_file.read())
    else:
        db.ci_files.insert(user_id=session.auth.user.id,dates=today,description="retrofacturation",files_csv=db.ci_files.files_csv.store(this_file,file_name),file_data_csv=this_file.read())        
    this_file.close()
    #delete the file
    os.remove(file_name)

    redirect(URL('ci_files')) 
    return dict()

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add')|auth.has_membership(role='gestion_retrofacturation_read'))
def ci_files():    
    response.menu+=[
        (T('Entrepôt des fichiers'), False, URL( f='ci_files'),[]),
        ]
    grid = SQLFORM.grid(db.ci_files,orderby=~db.ci_files.dates,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False)
    return dict(grid=grid)

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation'))
#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation'))
def tables():
    menu_url=[]
    #tables=["account_department","client_departments","manager_to_account","invoice_file","invoices"]
    #tables={"Départements":"account_department","Clients":"client_departments","Gestionaires":"managers_to_account","Fichiers de facture":"invoice_file","Factures":"invoices"}
    tables={"Dernière importation":"ci_octopus","Rétrofacturation":"ci_payment","Code d'ecriture":"ci_type","Code budgétaire":"account_department"}

    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    #table = request.args(0) or 'invoice_file'
    table = request.args(0) or 'ci_octopus'
    if not table in db.tables(): redirect(URL('error'))

    #grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)
    #response.flash = T(u'terminé')
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
