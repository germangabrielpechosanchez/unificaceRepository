# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
response.menu += [
    (T("Gestion des fichiers"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T("Creation des fichiers vide de type .ok"), False, URL( f='folder_hl7_ok'),[]), 
        #(T("blob to files "), False, URL( f='blob_files'),[]),
        (T("Tables des fichiers"), False, URL( f='tables'),[]),
    ])
]
import datetime,time
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()

def index():
    #db(db.mysql_files.id>0).delete()
    
    return dict(grid="")
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_fichiers_script'))
def folder_hl7_ok():
    response.menu+=[
        (T("Creation des fichiers vide de type .ok"), False, URL( f='folder_hl7_ok'),[]), 
        ]
    fields=[
        Field('source_root',default="\\\\s01vwpr00090.cemtl.rtss.qc.ca\Interfaces_fichiers\IN\hmr\eClinibase\\20170101",label=T('Dossier souce')),
        Field('target_root',default="\\\\s01vwpr00090.cemtl.rtss.qc.ca\Interfaces_fichiers\IN\hmr\eClinibase\\20170101",label=T('Dossier cible')),
    ]
   
    form = SQLFORM.factory(*fields)
    if form.accepts(request.vars,session,keepvalues=True):
        import subprocess
        arg1=request.vars.source_root
        arg2=request.vars.target_root
        script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_fichiers\folder_hl7_ok.ps1'       
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1,arg2],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p1.communicate()
        #response.flash=(output,error)
        response.flash=output

    return dict(grid=form)

@auth.requires(auth.has_membership(role='admin'))
def blob_files():

    import mysql.connector,uuid

    mydb = mysql.connector.connect(
    host="s03vldv00001.cemtl.rtss.qc.ca",
    user="vp",
    passwd="Uni123456",
    database='mydb',
    auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    #mycursor.execute("select * from wp_cf7dbplugin_submits where (field_value='CV_Jasmine-Doan.docx') or (field_value='Lettre-de-motiv-NATHALIE-TSHIBAMBA1.pdf');")
    mycursor.execute("select * from wp_cf7dbplugin_submits  WHERE FILE IS not NULL;")
    rs = mycursor.fetchall()
    for r in rs:
        #find prenom et nom
        mycursor2 = mydb.cursor()
        mycursor2.execute("select * from wp_cf7dbplugin_submits where (submit_time="+str(r[0])+") AND ((field_name='prenom') OR (field_name='nom'));")
        ns = mycursor2.fetchall()
        name=""
        first_name=""
        for n in ns:
            if n[2]=='nom':
                name=n[3]
            else:
                first_name=n[3]
        full_name=name+";"+first_name

        exten=(r[3].split('.')[-1][:6]).split(',')[0]
        #file_id=uuid.uuid4().hex+'.'+exten
        file_id=name+"_"+first_name+"_"+uuid.uuid4().hex+'.'+exten
        file_name=r'\\s03vwdv00004.cemtl.rtss.qc.ca\files_from_table\myfiles\\'+file_id
        link_name=r'file://s03vwdv00004.cemtl.rtss.qc.ca/files_from_table/myfiles/'+file_id
        #print file_name
            
        data=r[5]
        with open(file_name, 'wb') as file:
            try:
                submit_time=datetime.datetime.fromtimestamp(int(r[0]))
            except:
                submit_time=datetime.datetime(2000,1,1),

            db.mysql_files.insert(
                submit_time_id=(r[0]),
                submit_time=submit_time,
                form_name=r[1],
                field_name=r[2],
                field_value=r[3],
                field_order=r[4],
                full_name=full_name,
                unique_file_name=file_id,
                links=link_name,
            )
            file.write(data)

    redirect(URL('tables'))
    

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_fichiers'))
def tables():
    menu_url=[]
    tables={"mysql_files":"mysql_files",}

    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]
    if request.args(0):
        table = request.args(0)
        grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=150)
        #deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    else:
        grid = ""
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


