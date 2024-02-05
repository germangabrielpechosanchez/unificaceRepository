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

    (T("Actualisation des inventaires"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T("Préparation la liste des CIs"), False, URL( f='cis_listing'),[]),
        (T("Désactivation des CIs"), False, URL( f='cis_deactivation'),[]),
        (T("Entrepôt des fichiers Octopus"), False, URL( f='octopus_files'),[]),
        (T("Historique"), False, URL( f='all_items'),[]),
        (T("Réactivation des CIs - Retour en arrière"), False, URL( f='cis_reactivation'),[]),                
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        (T('Gestion des accès au module'), False, URL( f='module_access_create'),[]),
    ]),
]
try: 
    auth_id=session.auth.user.id
except:
    auth_id=1

act_inventaires_groups=(1046,1047,1048)
import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()

if auth.is_logged_in():
    if (auth.has_membership(role='admin')):
        create=True
        deletable=True
        editable=True
        user_signature=True
        searchable=True
        details=True
    elif (auth.has_membership(role='actualisation_inventaires'))|(auth.has_membership(role='actualisation_inventaires_admin')):
        create=True
        deletable=True
        editable=True
        user_signature=True
        searchable=True
        details=True
    elif (auth.has_membership(role='actualisation_inventaires_pcs')):
        create=False
        deletable=False
        editable=True
        user_signature=True
        searchable=True
        details=True
    else:
        create=False
        deletable=False
        editable=False
        user_signature=True
        searchable=True
        details=False
else:
    create=False
    deletable=False
    editable=False
    user_signature=True
    searchable=True
    details=False

@auth.requires_login()
def index():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        ]
    grid=""
    #session.this_manager=False
    #db(db.app2app.id>0).delete()
    #db(db.mappage.oldDomaine.like('hsco',case_sensitive=False)).update(oldDomaine="hsco.net")

    #db(db.app2app.status=="donne").delete()
    #octopus_importation((274,))
    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires')|auth.has_membership(role='actualisation_inventaires_pcs'))
def cis_listing():
    grid=""
    form=""    
    response.menu+=[
        (T("Préparation la liste des CIs"), False, URL( f='cis_listing'),[]),
        #(T("Désactivation des CIs"), False, URL( f='cis_deactivation'),[]),
    ]

    if request.vars.request_ci_name:
        request_ci_name=request.vars.request_ci_name
    else:
        request_ci_name=""
        
    fields=[
        Field('cis_name',type='text',label=T("Nom de CI(s)"),length=30000,requires=IS_NOT_EMPTY(),default=request_ci_name,comment=T("Un nom du CI sans domaine par ligne. Par exemple cpc00123. On peut avoir plusieurs lignes."),represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
        #Field('days_delete','integer',label=T('Sera supprimé dans [jours]'),default=3,requires = IS_INT_IN_RANGE(1,8),comment="Le CI sera supprimé automatiquement dans x jour(s) après désactivation."),
    ]
    #form = SQLFORM.factory(*fields)
    buttons=[
            TD(INPUT(_type="submit",_value="Ajouter",_id="Ajouter",_name="Ajouter",_style="background-color:#0066ff")),
        ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(9,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        #db(db.act_cis.id>0).delete()
        cis_name=request.vars.cis_name.split('\r\n')
        session.data=dict(
            command='actualisation_inventaires_verifier',
            cis_name=cis_name,
            auth_id=auth_id
        )
        import json
        response_data=call_background_task()
        try:
            response_dict=json.loads(response_data.response)
            session.msg="La liste des serveurs non trouvés: "+str(response_dict['non_trouve'])
        except:
            session.msg="Aucun réponse de Powershell background service."

        

    qry=(db.act_cis.disabled==False)&(db.act_cis.edit_by==auth_id)
    orderby=~db.act_cis.id
    #grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=False,user_signature=user_signature,searchable=searchable,details=details)
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=True,editable=editable,create=False,user_signature=user_signature,searchable=searchable,details=details)
    response.flash=session.msg
    session.msg=None
    return dict(script="",form=form,grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires')|auth.has_membership(role='actualisation_inventaires_pcs'))
def cis_deactivation():
    grid=""
    form=""    
    response.menu+=[
        (T("Désactivation des CIs"), False, URL( f='cis_deactivation'),[]),
    ]
    fields=[
        Field('days_delete','integer',label=T('Sera supprimé dans [jours]'),default=7,requires = IS_INT_IN_RANGE(1,8),comment="Le CI sera supprimé automatiquement dans x jour(s) après désactivation."),
    ]
    form = SQLFORM.factory(*fields)
    buttons=[
            TD(INPUT(_type="submit",_value="Sélectionner tout",_id="Sélectionner tout",_name="Sélectionner tout",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="Déselectionner tout",_id="Déselectionner tout",_name="Déselectionner tout",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="Désactiver",_id="Désactiver",_name="Désactiver",_style="background-color:#0066ff")),
        ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(9,elements)
    cis_origin=()
    if form.accepts(request.vars,session,keepvalues=True):
        if auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires'):
            qry=(db.act_cis.disabled==False)&(db.act_cis.edit_by==auth_id)
        elif auth.has_membership(role='actualisation_inventaires_pcs'):
            qry=(db.act_cis.disabled==False)&(db.act_cis.edit_by==auth_id)&(db.act_cis.description.like("%Workstation%")|db.act_cis.description.like("%Ordinateur%")|db.act_cis.description.like("%Computer%"))

        if request.vars.has_key("Sélectionner tout"):
            db(qry).update(selected=True)
        elif request.vars.has_key("Déselectionner tout"):
            db(qry).update(selected=False)
        elif request.vars.has_key("Désactiver"):
            qry=qry&(db.act_cis.selected==True)
            db(qry).update(edit_time=now,date_disabled=today,days_delete=request.vars.days_delete)
            rs=db(qry).select(db.act_cis.id,db.act_cis.name)
            cis_origin=db(qry).select(db.act_cis.id)
            cis=[[r.id,r.name] for r in rs]
            if len(cis)>0:
                session.data=dict(
                    command='actualisation_inventaires_desactivation',
                    cis=cis
                )
                import json
                #desactivation
                response_data=call_background_task()
                response_dict=json.loads(response_data.response)
                session.msg=response_dict['cis']
                #[u'267;AD:desactive|VCENTER:PoweredOff|', u'268;AD:desactive|'] ×
                for r in response_dict['cis']:
                    t=r.split(';')
                    r_id=int(t[0])
                    r_description=t[1]
                    description=db(db.act_cis.id==r_id).select(db.act_cis.description).first().description
                    db(db.act_cis.id==r_id).update(description=r_description+';'+description,disabled=True,selected=False)
                    #create app2app new scheduling task to delete
                    this_r=db(db.act_cis.id==r_id).select(db.act_cis.name,db.act_cis.date_disabled,db.act_cis.days_delete).first()
                    ci_name=this_r.name
                    date_disabled=datetime.datetime.now()+datetime.timedelta(days=this_r.days_delete)
                    publish_id=str(date_disabled)+"_act_cis_id_"+str(r_id)
                    #session.msg=publish_id
                    #for test
                    #publish_id=str(datetime.datetime.now()+datetime.timedelta(minutes=120))+"_act_cis_id_"+str(r_id)
                    ###
                    command=dict(
                        command='actualisation_inventaires_supprimer',
                        act_cis_id=r_id,
                        ci_name=ci_name
                        )
                    db.app2app.insert(
                        publish_id=publish_id,
                        subscribe_id='',
                        app='actualisation_inventaires',
                        status='scheduling',
                        command=json.dumps(command),
                        response='',
                        )
                    # delete from
                    server_name='%|'+ci_name.split('@')[0].upper()
                    db(db.vms_folders.paths.like(server_name)).delete() 
                    
                #update octopus status "retiré"
                octopus_importation(cis_origin,"Retiré")
            else:
                session.msg="Aucun élément sélectionné."

    qry=((db.act_cis.disabled==False)&(db.act_cis.edit_by==auth_id))|(db.act_cis.id.belongs(cis_origin))
    #orderby=~db.act_cis.id
    orderby=db.act_cis.id
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=False,user_signature=user_signature,searchable=searchable,details=details)
    response.flash=session.msg
    session.msg=None
    return dict(script="",form=form,grid=grid)

def octopus_importation(ids,status):
    import json,uuid
    file_name=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_inventaires\octopus\ci_csv'+uuid.uuid4().hex+'.csv'
    this_file=open(file_name, 'w')
    line="Nom;Type;État\n".decode('utf8').encode('ISO-8859-1')
    this_file.write(line)
    rs=db(db.act_cis.id.belongs(ids)).select()
    for r in rs:
        r_name=(r.name.split(';')[0]).split('@')[0]
        r_description=r.description.lower()
        if ('workstation' in r_description):
            line=(r_name+";Ordinateur;"+status+"\n").decode('utf8').encode('ISO-8859-1')
            this_file.write(line)
        elif ('server' in r_description)|('servers' in r_description)|('serveur' in r_description)|('serveurs' in r_description):
            #line=(r_name+";Serveur;"+status+"\n").decode('utf8').encode('ISO-8859-1')
            line=(r_name+";;"+status+"\n").decode('utf8').encode('ISO-8859-1')
            this_file.write(line)
        else:
            #line=(r_name+";Ordinateur;"+status+"\n").decode('utf8').encode('ISO-8859-1')
            line=(r_name+";;"+status+"\n").decode('utf8').encode('ISO-8859-1')
            this_file.write(line)
            # line=(r_name+";Serveur;"+status+"\n").decode('utf8').encode('ISO-8859-1')
            # this_file.write(line)
    this_file.close()
    this_file=open(file_name, 'r')
    author=db(db.auth_user.id==auth_id).select(db.auth_user.username).first().username
    db.oct_importation_files.insert(user_id=auth_id,team=1,types='CI',dates=now,description="Géneré par le module de actualisation inventaires :"+author,imported=False,files=db.oct_importation_files.files.store(this_file,file_name),file_data=this_file.read())
    this_file.close()
    import os;os.remove(file_name)
    db(db.act_cis.id.belongs(ids)).update(imported=True) #mark as imported
    session.msg="Un fichier d'exportation est générer et prêt à exporter."
    #redirect(URL('octopus_files'))
    return

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires')|auth.has_membership(role='actualisation_inventaires_pcs'))
def cis_reactivation():

    grid=""
    form=""    
    response.menu+=[
        (T("Réactivation des CIs"), False, URL( f='cis_reactivation'),[]),
    ]
    fields=[
        Field('reactivate','text',label=T('Réactivation'),default='maintenant',requires=IS_IN_SET(('maintenant',))),
    ]
    form = SQLFORM.factory(*fields)
    buttons=[
            TD(INPUT(_type="submit",_value="Sélectionner tout",_id="Sélectionner tout",_name="Sélectionner tout",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="Déselectionner tout",_id="Déselectionner tout",_name="Déselectionner tout",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="Réactiver",_id="Réactiver",_name="Réactiver",_style="background-color:#0066ff")),
        ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(9,elements)
    cis_origin=()
    if form.accepts(request.vars,session,keepvalues=True):
        if auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires'):
            qry=(db.act_cis.deleted==False)&(db.act_cis.edit_by==auth_id)
        elif auth.has_membership(role='actualisation_inventaires_pcs'):
            qry=(db.act_cis.deleted==False)&(db.act_cis.edit_by==auth_id)&(db.act_cis.description.like("%Workstation%")|db.act_cis.description.like("%Ordinateur%")|db.act_cis.description.like("%Computer%"))

        if request.vars.has_key("Sélectionner tout"):
            db(qry).update(selected=True)
        elif request.vars.has_key("Déselectionner tout"):
            db(qry).update(selected=False)
        elif request.vars.has_key("Réactiver"):
            qry=qry&(db.act_cis.selected==True)
            cis_origin=db(qry).select(db.act_cis.id)
            rs=db(qry).select(db.act_cis.id,db.act_cis.name)
            cis=[[r.id,r.name] for r in rs]
            if len(cis)>0:
                session.data=dict(
                    command='actualisation_inventaires_reactivation',
                    cis=cis
                )
                import json
                #session.msg=session.data['cis']
                #reactivation
                response_data=call_background_task()
                response_dict=json.loads(response_data.response)
                session.msg=response_dict['cis']
                #[u'267;AD:desactive|VCENTER:PoweredOff|', u'268;AD:desactive|']
                for r in response_dict['cis']:
                    t=r.split(';')
                    r_id=int(t[0])
                    r_description=t[1]
                    description=db(db.act_cis.id==r_id).select(db.act_cis.description).first().description
                    db(db.act_cis.id==r_id).update(description=r_description+';'+description,disabled=False,selected=False,reactivated=True)
                    #Cancel app2app scheduling task to canceled
                    id_like="%_act_cis_id_"+str(r_id)
                    db((db.app2app.status=='scheduling')&(db.app2app.publish_id.like(id_like))).update(status='canceled')
                #octopus_importation    
                octopus_importation(cis_origin,"En service")
            else:
                session.msg="Aucun élément sélectionné."

    qry=((db.act_cis.deleted!=True)&(db.act_cis.edit_by==auth_id)&(db.act_cis.disabled!=False))|(db.act_cis.id.belongs(cis_origin))
    #orderby=~db.act_cis.id
    orderby=db.act_cis.id
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=False,user_signature=user_signature,searchable=searchable,details=details)
    response.flash=session.msg
    session.msg=None
    
    return dict(script="",form=form,grid=grid)

def call_background_task():
    import json,uuid,time
    publish_id=uuid.uuid4().hex
    db.app2app.insert(
        publish_id=publish_id,
        subscribe_id='',
        app='actualisation_inventaires',
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
            if(i>30):
                waiting=False
                r="too long"
            else:
                i+=1
    return r    
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires')|auth.has_membership(role='actualisation_inventaires_pcs'))
def all_items():    
    response.menu+=[
        (T("Historique"), False, URL( f='all_items'),[]),
        ]
    qry=db.act_cis.id>0
    orderby=~db.act_cis.id
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False,buttons_placement = 'left')
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin'))#|auth.has_membership(role='actualisation_inventaires')
def tables():
    menu_url=[]
    tables={"Actualisation des CIs":"act_cis","App2app":"app2app"}

    for table in tables.keys():
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    table = request.args(0) or 'act_cis'
    if not table in db.tables(): redirect(URL('error'))
    grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=160,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires')|auth.has_membership(role='actualisation_inventaires_pcs'))
def octopus_files():    
    response.menu+=[
        (T("Entrepôt des fichiers Octopus"), False, URL( f='octopus_files'),[]),
        (T("Exportation vers Octopus"), False, URL( f='importation'),[]),
        ]
    form=FORM(TABLE(
        TR(
            TD(INPUT(_type="submit",_value="Exportation vers Octopus",_id="Exportation vers Octopus",_name="Exportation vers Octopus",_style="background-color:#0066ff")),
        ),
        TR(),
    ))
    if form.accepts(request.vars,session):
        if request.vars.has_key("Exportation vers Octopus"):
            redirect(URL('importation'))

    qry=db.oct_importation_files.description.like('%actualisation inventaires%')
    orderby=db.oct_importation_files.imported|~db.oct_importation_files.dates
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False,buttons_placement = 'left')
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires')|auth.has_membership(role='actualisation_inventaires_pcs'))
def importation():
    response.menu+=[
        (T('Importation'), False, URL( f='importation'),[]),
        ]
    import subprocess,os
    fs=db((db.oct_importation_files.imported==False)&(db.oct_importation_files.description.like('%actualisation_inventaires%'))).select(db.oct_importation_files.ALL)
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
            
            this_file=open(file_name, 'w')
            #lines=ls.decode('utf8').encode('ISO-8859-1')
            #lines=ls.encode('ISO-8859-1')
            #lines=ls.encode('utf8')
            lines=ls
            this_file.write(lines)
            this_file.close()
            this_file=open(file_name, 'r')
            db(db.oct_importation_files.id==f.id).update(imported=True,file2=db.oct_importation_files.file2.store(this_file,file_name),file_data2=this_file.read())
            this_file.close()
            script=path+f_name+".bat"
            cs=(
                'Octopus_cemtl',
                #'Octopus_test'
            )
            


            #create ini file for text
            head_line=(lines.split('\n')[0]).split(',')
            ini_name=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\Schema.ini'
            ini_file=open(ini_name,'w')
            ini_lines="["+file_csv+"]\nColNameHeader=True\nFormat=CSVDelimited\nDecimalSymbol=.\n"
            i=0
            for col in head_line:
                i+=1
                ini_lines+='Col'+str(i)+'="'+col.replace('\n','')+'" Text\n'
            ini_file.write(ini_lines)
            ini_file.close()



            for c in cs:
                this_file=open(script, 'w')
                bat_line=r"C:\Users\admphav\AppData\Local\Octopus_cemtl\ESI.Octopus.DataImporterApp.exe /Login:octsys01 /Password:Bonjour02 /ConfigFilePath:C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\\"+file_xml+" /team:1 /LogFilePath:"
                log_file=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\logs\DataImporter"+str(session.auth.user.id)+".log"
                #for all
                bat_line=bat_line.replace('Octopus_cemtl',c)

                bat_line+=log_file
                this_file.write(bat_line)
                this_file.close()

                log_path=r"C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_octopus\logs"
                file_patern="DataImporter"+str(session.auth.user.id)
                #list of files in dir #new log of octopus with timestamps like DataImporter1117_20190905_111036.log
                for i in os.listdir(log_path):
                    if file_patern in i:
                        os.remove(log_path+"\\"+i)

                p1 = subprocess.Popen([script,script],shell=True, stdout = subprocess.PIPE,stderr=subprocess.PIPE)
                stdout,error = p1.communicate()


                #delete ini file
                os.remove(ini_name)


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
                #grid=grid.replace("gestion_octopus","")
                grid=grid.replace("gestion_octopus","")
                grid=grid.replace("octsys01","")
                grid=grid.replace("Bonjour02","")
                grid=grid.replace("ConfigFilePath","By Unificace")            
                db(db.oct_importation_files.id==f.id).update(file3=db.oct_importation_files.file3.store(this_file,"dataImportLog.txt"),file_data3=grid)

    if fs:
        redirect(URL('log_file')) 
    else:
        redirect(URL('octopus_files'))
    return dict()

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires')|auth.has_membership(role='actualisation_inventaires_pcs'))
def log_file():
    import os
    if session.function=='reprinting_support':
        session.function=None
        redirect(URL('label_files'))
    response.menu += [
        (T("Logs"), False, URL( f='log_file'),[]),
        #(T("impression d'étiquettes"), False, URL( f='inventory_impression'),[]),
        #(T("impression d'étiquettes ( PTouch)"), False, URL( f='inventory_impression_pt'),[]),
        ] 
    grid=""
    form=""
    
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

    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires_admin'))
def module_access_create():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Créer un accès'), False, URL(f='module_access_create'),[]),
    ]    
    grid=""    
    qry=(db.pre_user_to_group.group_id.belongs(act_inventaires_groups))
    #qry=(db.auth_membership.group_id.belongs(act_inventaires_groups))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='actualisation_inventaires_admin'))
def module_access_edit():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
    ]    
    grid=""    
    #qry=(db.pre_user_to_group.group_id.belongs(act_inventaires_groups))
    qry=(db.auth_membership.group_id.belongs(act_inventaires_groups))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

def access_onvalidation(form):
    #form.vars.group_id
    if form.vars.group_id not in act_inventaires_groups:
        rs=db(db.auth_group.id.belongs(act_inventaires_groups)).select(db.auth_group.role)
        form.errors.group_id="Le groupe doit être dans cette liste: "+((str(rs).replace("auth_group.role","")).replace("actualisation_inventaires",", actualisation_inventaires"))
        form.errors= True
    return

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
