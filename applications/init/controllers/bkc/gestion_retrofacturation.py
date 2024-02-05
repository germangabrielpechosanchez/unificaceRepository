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
        (T('Synchronisation avec Octopus'), False, URL( f='validation_octopus'),[]),
        (T('Historique de rétrofacturation'), False, URL( f='history'),[]),
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
        deletable=True
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
    """
    #db(db.ci_payment.id>0).update(completed=datetime.datetime(3000,1,1))

    fs=db(db.ci_files.id==11).select(db.ci_files.file_data_octopus)
    for f in fs:
        ls=f.file_data_octopus.split('\r\n')
        ls=ls[1:]
        i=0
        not_found=""
        for l in ls:
            cs=l.split('\t')
            if len(cs)==4:
                a=db(db.account_department.account==cs[2]).select()
                db(db.ci_payment.name==cs[1]).update(account=a[0].id,completed=today,to_update=False)
                i+=1

        response.flash =i
    """
    #db(db.ci_payment.completed==datetime.datetime(2018,5,1)).update(imported=datetime.datetime(2018,4,5),exported=datetime.datetime(2018,4,5))
    #db(db.ci_payment.exported==datetime.datetime(2018,5,1)).update(exported=datetime.datetime(3000,1,1))

    
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
    #db(db.ci_payment.completed==datetime.date(3000,1,1)).update(to_update=False,)
    #read data from Octopus
    #"""
    import subprocess 
    script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\read_octopus_retrofacturation.py'
    p1 = subprocess.Popen([r'C:\python27\python.exe',script],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,error = p1.communicate()
    #"""
    rs=db(db.ci_octopus.id).select()
    db(db.ci_payment.completed==datetime.date(3000,1,1)).delete()
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
            #db((db.ci_payment.ci_id==r.ci_id)&(db.ci_payment.completed==datetime.date(3000,1,1))).update(
                ci_id=r.ci_id,
                name=r.name,
                type_id=r.type_id,
                ci_type=r.ci_type,
                code_ecriture=code_ecriture,
                account_code=r.account_code,
                grm_code=r.grm_code,
                account=account,
                #account_name=account_name,
                purchase_price=r.purchase_price,
                purchase_dates=r.purchase_dates,
                imported=today,
                to_update=False,
                exported=datetime.date(3000,1,1),
                completed=datetime.date(3000,1,1),
                descriptions=r.descriptions,
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
                grm_code=r.grm_code,
                account=account,
                #account_name=account_name,
                purchase_price=r.purchase_price,
                purchase_dates=r.purchase_dates,
                imported=today,
                to_update=False,
                exported=datetime.date(3000,1,1),
                completed=datetime.date(3000,1,1),
                descriptions=r.descriptions,
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
    qry=(db.ci_payment.exported==datetime.date(3000,1,1))|(db.ci_payment.exported==today) #&(db.ci_payment.account==db.account_department.id)
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    #qry=(db.ci_payment.id>0)&((db.ci_payment.exported==datetime.date(3000,1,1))|(db.ci_payment.exported==today))&(db.ci_payment.account==db.account_department.id)
    #fields=[db.ci_payment.id,db.ci_payment.ci_id,db.ci_payment.name,db.ci_payment.type_id,db.ci_payment.ci_type,db.ci_payment.code_ecriture,db.ci_payment.account_code,db.account_department.account,db.account_department.department,db.account_department.account_type,db.ci_payment.purchase_price,db.ci_payment.purchase_dates,db.ci_payment.imported,db.ci_payment.exported]
    #grid = SQLFORM.grid(qry,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    #grid = SQLFORM.grid(qry,fields=fields,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

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
    #mark exported and mark for update with Octopus
    db(db.ci_payment.exported==datetime.date(3000,1,1)).update(exported=today,to_update=True)#for prod
    #db(db.ci_payment.id.belongs(2454,2455)).update(exported=today,to_update=True)#for test
    #db((db.ci_payment.exported==datetime.date(3000,1,1))&(db.ci_payment.account<>9679).update(to_update=True)# for  old test
    date_finan=date_financial(today)
    #line="10;;"+str(session.auth.user.username)+";"+str(date_finan[0])+";"+str(date_finan[1])+";"+str(datetime.date.today()).replace('-','')+";1001;G20;Sortie d'inventaire equipements informatiques\r\n"
    line="10;;"+str(session.auth.user.username)+";"+str(date_finan[0])+";"+str(date_finan[1])+";"+str(datetime.date.today()).replace('-','')+";1001;G20;Sortie d'inventaire equipements informatiques\r\n"
    this_file.write(line)
    total=0
    for r in rs:
        #purchase_price=r.purchase_price
        purchase_price=round(r.purchase_price*1.056879,2)
        total-=purchase_price
        account_code=db(db.account_department.id==r.account).select(db.account_department.account).first().account
        if r.descriptions:
            r_descriptions=r.descriptions
        else:
            r_descriptions=''
        r_grm_code='' if r.grm_code==None else r.grm_code
        #line="20;;;;;;;;;"+r.ci_type+"-"+r.name+";1001;;"+account_code+";"+r.code_ecriture+";"+str(purchase_price)+"\r\n"
        line="20;;;;;;;;;"+r.ci_type+"-"+r.name+"-"+r_descriptions+";1001;;"+account_code+";"+r.code_ecriture+";;;"+str(purchase_price)+";;;;;;;"+r_grm_code+"\r\n"
        this_file.write(line)
    line="20;;;;;;;;;Sortie d'inventaire equipements informatiques;1001;100111150095;;;;;"+str(total)+"\r\n"
    this_file.write(line)
    #line="99;"+str(len(rs)+3)+";;;;;;;;;;;;;\r\n"
    line="99;"+str(len(rs)+3)+";;;;;;;;;;;;;;;\r\n"
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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add'))
def validation_octopus():

    menu_octopus=[
            (T('Préparation'), False, URL( f='validation_octopus'),[]),
            (T('Synchronisation'), False, URL( f='exportation_octopus'),[]),
            (T("Historique"), False, URL( f='log_file'),[]),
        ]       
    response.menu += [
        (T("Synchronisation avec Octopus"), False, '#',menu_octopus),
        (T('Préparation'), False, URL( f='validation_octopus'),[]),
        ]

    grid =""
    qry=(db.ci_payment.exported<>datetime.date(3000,1,1))&(db.ci_payment.to_update==True)
    #qry=(db.ci_payment.exported<>datetime.date(3000,1,1))&(db.ci_payment.to_update==True)#original <2020-05-20
    #qry=(db.ci_payment.exported==datetime.date(3000,1,1))&(db.ci_payment.to_update==True)#for test
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add'))
def exportation_octopus():
    menu_octopus=[
            (T('Préparation'), False, URL( f='validation_octopus'),[]),
            (T('Synchronisation'), False, URL( f='exportation_octopus'),[]),
            (T("Historique"), False, URL( f='log_file'),[]),
        ]       
    response.menu += [
        (T("Synchronisation avec Octopus"), False, '#',menu_octopus),
        (T('Synchronisation'), False, URL( f='exportation_octopus'),[]),
        ]  
    rs=db((db.ci_payment.exported<>datetime.date(3000,1,1))&(db.ci_payment.to_update==True)&(db.ci_payment.account==db.account_department.id)).select(db.ci_payment.name,db.account_department.account,db.ci_payment.exported,db.ci_payment.exported)

    if rs:
        import subprocess,os     
        file_name=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus\ci_csv.csv'
        #this_file=codecs.open('file_name', encoding='latin1', mode='w')
        #"""
        #disable for test
        this_file=open(file_name, 'w')
        #mark as already syned
        db((db.ci_payment.exported<>datetime.date(3000,1,1))&(db.ci_payment.to_update==True)).update(to_update=False,completed=today) #mark as already syned
        line="Type,Nom,RF - Centre de coûts,RF - Complétée\n".decode('utf8').encode('ISO-8859-1')
        this_file.write(line)
        for r in rs:
            #line=","+r.ci_payment.name+","+r.account_department.account+","+str(r.ci_payment.exported)+"\n".decode('utf8').encode('ISO-8859-1')
            line=","+r.ci_payment.name+","+r.account_department.account+","+str(today)+"\n".decode('utf8').encode('ISO-8859-1')
            this_file.write(line)
        this_file.close()
        #"""
        this_file=open(file_name, 'r')
        date_exported=rs[0].ci_payment.exported
        r=db(db.ci_files.dates==date_exported).select()
        if r:
            db(db.ci_files.dates==date_exported).update(files_octopus=db.ci_files.files_octopus.store(this_file,file_name),file_data_octopus=this_file.read())
        else:
            db.ci_files.insert(user_id=session.auth.user.id,dates=date_exported,description="retrofacturation",files_octopus=db.ci_files.files_octopus.store(this_file,file_name),file_data_octopus=this_file.read())
        this_file.close()
        #old
        #script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus\data_importer_csv.bat'
        #p1 = subprocess.Popen([script,script],shell=True, stdout = subprocess.PIPE)
        #stdout,error = p1.communicate()

        ########################
        file_xml="ci_csv.xml"
        script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus\data_importer_csv.bat'
        #crete bat file
        this_file=open(script, 'w')
        bat_line=r"C:\Users\admphav\AppData\Local\Octopus_cemtl\ESI.Octopus.DataImporterApp.exe /Login:octsys01 /Password:Bonjour02 /ConfigFilePath:C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus\\"+file_xml+" /team:1 /LogFilePath:"
        log_file=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus\DataImporter"+str(session.auth.user.id)+".log"
        bat_line+=log_file
        this_file.write(bat_line)
        this_file.close()
        #Clean log file
        this_file=open(log_file, 'w')
        this_file.close()
        #\\S03VWdv00006\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus
        log_path=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus"
        file_patern="DataImporter"+str(session.auth.user.id)
        #list of files in dir #new log of octopus with timestamps like DataImporter1117_20190905_111036.log
        for i in os.listdir(log_path):
            if file_patern in i:
                os.remove(log_path+"\\"+i)

        #p1 = subprocess.Popen([script,script],shell=True, stdout = subprocess.PIPE)
        p1 = subprocess.Popen([script,script],shell=True, stdout = subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,error = p1.communicate()

        #read new log
        for i in os.listdir(log_path):
            if file_patern in i:
                log_file=log_path+"\\"+i
                break


        this_file=open(log_file, 'r')
        grid=this_file.read()
        this_file.close()
        grid=grid.replace("\n","\r\n")
        grid=grid.replace("unificace","")
        grid=grid.replace("web2py","")
        grid=grid.replace("gestion_octopus","")
        grid=grid.replace("octsys01","")
        grid=grid.replace("Bonjour02","")
        grid=grid.replace("ConfigFilePath","By Unificace")
        db(db.ci_files.dates==date_exported).update(file3=db.ci_files.file3.store(this_file,"dataImportLog.txt"),file_data3=grid)

        redirect(URL('log_file')) 
    else:
        redirect(URL('validation_octopus'))
    return dict()

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add'))
def log_file():
    import os
    menu_octopus=[
            (T('Préparation'), False, URL( f='validation_octopus'),[]),
            (T('Synchronisation'), False, URL( f='exportation_octopus'),[]),
            (T("Historique"), False, URL( f='log_file'),[]),
        ]       
    response.menu += [
        (T("Synchronisation avec Octopus"), False, '#',menu_octopus),
        (T("Historique"), False, URL( f='log_file'),[]),
        ] 
    grid=""
    try:    
        #log_file=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus\DataImporter"+str(session.auth.user.id)+".log"
        
        log_path=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_retrofacturation\octopus"
        file_patern="DataImporter"+str(session.auth.user.id)
        for i in os.listdir(log_path):
                if file_patern in i:
                    log_file=log_path+"\\"+i
                    break
        
        
        this_file=open(log_file, 'rb')
        grid=this_file.read()
        this_file.close()
        grid=grid.replace("\n","<br>")
        grid=grid.replace("unificace","")
        grid=grid.replace("web2py","")
        grid=grid.replace("gestion_octopus","")
        grid=grid.replace("octsys01","")
        grid=grid.replace("Bonjour02","")
        grid=grid.replace("ConfigFilePath","By Unificace")
    except:
        pass
    
    return dict(grid=grid)




@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_retrofacturation')|auth.has_membership(role='gestion_retrofacturation_edit')|auth.has_membership(role='gestion_retrofacturation_edit_add'))
def history():
    response.menu += [
        (T('Historique de rétrofacturation'), False, URL( f='history'),[]),
    ]
    #qry=(db.ci_payment.id>0)&(db.ci_payment.account==db.account_department.id)
    qry=(db.ci_payment.id>0)
    #fields=[db.ci_payment.ci_id,db.ci_payment.name,db.ci_payment.type_id,db.ci_payment.ci_type,db.ci_payment.code_ecriture,db.ci_payment.account_code,db.account_department.account,db.account_department.department,db.account_department.account_type,db.ci_payment.purchase_price,db.ci_payment.purchase_dates,db.ci_payment.imported,db.ci_payment.exported]
    #grid = SQLFORM.grid(qry,fields=fields,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=False,editable=False,create=False,user_signature=user_signature,searchable=searchable,details=details)

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
