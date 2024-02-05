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

    (T("Gestion des importations vers Octopus"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]), 
        (T('Entrepôt des templates'), False, URL( f='template_files'),[]),
        (T("Entrepôt des fichiers d'importation"), False, URL( f='importation_files'),[]),
        (T('Importation'), False, URL( f='importation'),[]),
        (T("Historique"), False, URL( f='log_file'),[]),
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        ]),
    
    ]
import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()

if auth.is_logged_in():
    if (auth.has_membership(role='admin')): #auth.has_membership(role='gestion_octopus_edit_add')
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_octopus')): #auth.has_membership(role='gestion_octopus_edit_add')
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_octopus_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_octopus_edit')):
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

@auth.requires_login()
def index():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        ]
    grid=""
    #db(db.oct_importation_files.id>0).update(team=1) 
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_octopus')|auth.has_membership(role='gestion_octopus_edit')|auth.has_membership(role='gestion_octopus_edit_add'))
def template_files():    
    response.menu+=[
        (T('Entrepôt des templates'), False, URL( f='template_files'),[]),
        ]
    qry=db.oct_template_files.id>0
    orderby=db.oct_template_files.types
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_octopus')|auth.has_membership(role='gestion_octopus_edit')|auth.has_membership(role='gestion_octopus_edit_add'))
def importation_files():    
    response.menu+=[
        (T("Entrepôt des fichiers d'importation"), False, URL( f='importation_files'),[]),
        ]
    qry=db.oct_importation_files.id>0
    orderby=db.oct_importation_files.imported|~db.oct_importation_files.dates
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_octopus')|auth.has_membership(role='gestion_octopus_edit')|auth.has_membership(role='gestion_octopus_edit_add'))
def importation():
    response.menu+=[
        (T('Importation'), False, URL( f='importation'),[]),
        ]
    import subprocess,os
    fs=db(db.oct_importation_files.imported==False).select(db.oct_importation_files.ALL)
    for f in fs:
        #ls=f.file_data.replace('\r','')
        #ls=f.file_data.replace(',',' ')
        ls=f.file_data.replace(',','.')
        ls=ls.replace(';',',')
        ls=ls.replace('\r','\n')
        ls=ls.replace('\n\n','\n')
        ls=ls.replace(',\n','\n')
        if len(ls.split('\n'))>1:
            f_name=f.types.lower()+"_data_importer"             
            file_csv=f_name+".csv"
            file_xml=f_name+".xml"              
            path= r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\\'
            file_name= path+file_csv
            #"""
            this_file=open(file_name, 'w')
            #lines=ls.decode('utf8').encode('ISO-8859-1')
            #lines=ls.encode('ISO-8859-1')
            #lines=ls.encode('utf8')
            lines=ls
            this_file.write(lines)
            this_file.close()
            #"""
            this_file=open(file_name, 'r')
            db(db.oct_importation_files.id==f.id).update(imported=True,file2=db.oct_importation_files.file2.store(this_file,file_name),file_data2=this_file.read())
            this_file.close()
            script=path+f_name+".bat"
            #script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\ci_data_importer.bat'
            #crete bat file
            this_file=open(script, 'w')
            bat_line=r"C:\Users\admphav\AppData\Local\Octopus_cemtl\ESI.Octopus.DataImporterApp.exe /Login:octsys01 /Password:Bonjour02 /ConfigFilePath:C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\\"+file_xml+" /team:"+str(f.team)+" /LogFilePath:"
            log_file=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\logs\DataImporter"+str(session.auth.user.id)+".log"
            bat_line+=log_file
            this_file.write(bat_line)
            this_file.close()

            #Clean log file
            #this_file=open(log_file, 'w')
            #this_file.close()
            log_path=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\logs"
            file_patern="DataImporter"+str(session.auth.user.id)
            #list of files in dir #new log of octopus with timestamps like DataImporter1117_20190905_111036.log
            for i in os.listdir(log_path):
                if file_patern in i:
                    os.remove(log_path+"\\"+i)

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
            db(db.oct_importation_files.id==f.id).update(file3=db.oct_importation_files.file3.store(this_file,"dataImportLog.txt"),file_data3=grid)

    if fs:
        redirect(URL('log_file')) 
    else:
        redirect(URL('importation_files'))
    return dict()

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_octopus')|auth.has_membership(role='gestion_octopus_edit')|auth.has_membership(role='gestion_octopus_edit_add'))
def log_file():
    import os
    response.menu += [
        (T("Historique"), False, URL( f='log_file'),[]),
        ] 
    grid=""
    log_file="test"
    try:
        
        log_path=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\logs"
        file_patern="DataImporter"+str(session.auth.user.id)
        for i in os.listdir(log_path):
                if file_patern in i:
                    log_file=log_path+"\\"+i
                    break
        #log_file=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\logs\DataImporter"+str(session.auth.user.id)+".log"
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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_octopus'))
def tables():
    menu_url=[]
    tables={"Templates des CIs":"oct_template_files","Fichier des importation":"oct_importation_files","Équipe":"oct_support_team"}
    for table in tables.keys():
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    table = request.args(0) or 'oct_template_files'
    if not table in db.tables(): redirect(URL('error'))

    grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

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
