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

    (T("Gestion des factures"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]), 
        (T('Navigateur de facture'), False, URL( f='invoice_browser'),[]),
        (T('Navigateur du téléphone'), False, URL( f='phone_browser'),[]),
        (T('Entrepôt des fichiers'), False, URL( f='import_file'),[]),
        (T('Importation'), False, URL( f='invoice_import'),[]),
        (T('Exportation'), False, URL( f='export'),[]),
        (T('Envoi de messages aux gestionnaires'), False, URL( f='sending_messages_link'),[]),
        (T('Historique'), False, URL( f='actions_tracking'),[]),
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
    if (auth.has_membership(role='admin')): #auth.has_membership(role='gestion_factures_edit_add')
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_factures')): #auth.has_membership(role='gestion_factures_edit_add')
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_factures_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_factures_edit')):
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
@auth.requires(auth.has_membership(role='admin'))
def admin_import_managers():
    #db(db.managers.id>0).update(notification="DA",)
    #db(db.managers_to_account.id>0).delete()
    #db(db.managers.id>0).delete()
    #db(db.managers.id>0).update(is_active=False)
    #0UA	1Direction	2Sous direction	3Responsable	4Entité légale	5UA	6Description	7Courriel
    #1011284	44 - Direction recherche	441 - Dir adj recherche	Pierre Fontaine	100175	1011284	Centre-Rech(FDRC/CL)	Pierre.Fontaine.CEMTL@ssss.gouv.qc.ca
    fs=db(db.invoice_file.id==8).select(db.invoice_file.id,db.invoice_file.file_data)
    for f in fs:
        ls=f.file_data.split('\r\n')
        ls=ls[1:]
        #ls=(ls[36],)
        for l in ls:
            cs=l.split('\t')
            if len(cs)>=8:
                #pass
                #import to account_department
                """
                department=(cs[6]+'_'+cs[2]).upper()
                r=db(db.account_department.account==cs[0]).select(db.account_department.id)
                if r:
                    db(db.account_department.account==cs[0]).update(
                        department=department,
                        account_type=cs[4],
                        is_active=True,
                    )
                else:
                    db.account_department.insert(
                        account=cs[0],
                        department=department,
                        account_type=cs[4],
                        account_nature="5315",
                        is_active=True,
                    )

                #import to managers
                name=cs[3].upper()
                r=db(db.managers.name==name).select(db.managers.id)
                if r:

                    #db(db.managers.name==name).update(
                    #    name=name,
                    #    email=cs[7].lower(),
                    #    notification="par courriel DA",
                    #    is_active=True,
                    #)

                    pass
                else:
                    db.managers.insert(
                        name=name,
                        email=cs[7].lower(),
                        notification="par courriel DA",
                        is_active=True,
                    )
                
                #import to managers_to_account
                name=cs[3].upper()
                r=db(db.managers.name==name).select(db.managers.id)
                if r:
                    a=db(db.account_department.account==cs[0]).select(db.account_department.id)
                    if a:
                        if not db((db.managers_to_account.manager==r[0].id)&(db.managers_to_account.account==a[0].id)).select(db.managers_to_account.id):
                            db.managers_to_account.insert(
                                manager=r[0].id,
                                account=a[0].id,
                            )
                """
    return len(ls)
@auth.requires(auth.has_membership(role='admin'))
def admin_import_client_departments():
    #db(db.invoice_file.id>0).update(sent=True)
    fs=db(db.invoice_file.id==9).select(db.invoice_file.id,db.invoice_file.file_data)
    for f in fs:
        ls=f.file_data.split('\r\n')
        ls=ls[1:]
        #ls=(ls[3224],ls[3228])
        """
        for l in ls:
            cs=l.split('\t')
            if len(cs)>=12:
                r=db(db.client_departments.client_number==cs[2]).select(db.client_departments.id,orderby=db.client_departments.id)
                if r:
                    last_id=r.last().id
                    db(db.client_departments.id==last_id).update(
                        client_name=cs[4],
                        infos=cs[5],
                        employee_number=cs[6],
                        job_tilte=cs[7],
                    )
        """
    return len(ls)

@auth.requires(auth.has_membership(role='admin'))
def admin_import_dd():
    #db(db.invoice_file.id>0).update(sent=True)
    fs=db(db.invoice_file.id==7).select(db.invoice_file.id,db.invoice_file.file_data)
    list=()
    for f in fs:
        ls=f.file_data.split('\r\n')
        ls=ls[1:]
        #ls=(ls[14],)

        """
        for l in ls:
            cs=l.split('\t')
            if len(cs)>=3:
                r=db(db.managers.name.like('%'+cs[1]+'%')).select()
                if r:
                    d='_'+cs[0][:2]
                    #rs=db(db.account_department.department.like('%'+d+'%')).select()
                    rs=db(db.account_department.department.contains(d)).select()
                    for i in rs:
                        found=db((db.managers_to_account.account==i.id)&(db.managers_to_account.manager==r[0].id)).select()
                        if not found:
                            db.managers_to_account.insert(
                                manager=r[0].id,
                                account=i.id,
                            )

                        
                    list+=((r[0].id,r[0].name,d,len(rs)),)

                    db(db.managers.id==r[0].id).update(
                        notification="DD",
                        is_active=True,
                    )
                else:
                    db.managers.insert(
                        windows_code="",
                        name=cs[1],
                        email=cs[2],
                        notification="DD",
                        is_active=True,
                    )
        """
    return str(list)

@auth.requires(auth.has_membership(role='admin'))
def admin_import():
    fs=db(db.invoice_file.id==34).select(db.invoice_file.id,db.invoice_file.file_data)
    #fs=db(db.invoice_file.id==59).select(db.invoice_file.id,db.invoice_file.file_data)
    #db(db.client_departments.id>0).update(account_type='',device_type='')
    for f in fs:
        ls=f.file_data.split('\r\n')
        ls=ls[1:]
        #ls=(ls[14],)
        for l in ls:
            cs=l.split('\t')
            """            
            if len(cs)>=15:
                number=cs[3]
                db(db.client_departments.client_number==number).update(account_type='voix',device_type='Téléphones cellulaires')

            if len(cs)>=13:
                number=cs[4]
                plan=cs[11]
                if plan=='2':
                    db(db.client_departments.client_number==number).update(account_type='données',device_type='')
                else:
                    db(db.client_departments.client_number==number).update(account_type='voix et données',device_type='Téléphones cellulaires')
            """

            


    return len(ls)


#@auth.requires(auth.has_membership(role='admin'))
@auth.requires_login()
def index():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        ]
    grid=""
    session.this_manager=False
    #table = request.args(0) or 'pvs_management'
    #grid = SQLFORM.smartgrid(db[table],args=request.args[:1],maxtextlength=70,\
    #deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    #grid = SQLFORM.smartgrid(db.pvs_management,maxtextlength=70,\
    #deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #rs=db(db.invoice_file.id>0).select(db.invoice_file.file_data)[0].file_data
    #db.invoice_file.insert(user_id=16,invoice_type='Telus facture pour CAP',description='test',files='testname',file_data=rs)
    #db.invoice_file.insert(files='testname',file_data=rs)

    """
    rs=rs.split('\r\n')
    r=rs[0].split('\t')
    s=''
    i=0
    #0 * Client Number; 1 * Bill Date; 2 * Billing Name; 3 * Additional Line of Billing Name; 4 * Purchase Order Number; 5 * Bill Number; 6 * Product Type; 7 * User; 8 * Sub Level A Name; 9 * Sub Level B Name; 10 * User Name; 11 * Additional User Name; 12 * Reference 1; 13 * Reference 2; 14 * Adjustments; 15 * Adjusted HST; 16 * Adjusted PST/QST; 17 * Adjusted GST; 18 * Service Plan Name; 19 * Service Plan Price; 20 * Additional Local Airtime; 21 * Over/Under; 22 * Contribution to Pool; 23 * Phone Long Distance Charges; 24 * Private/Group Long Distance Charges; 25 * Roaming Charges; 26 * Data and Other Services; 27 * Voice Services; 28 * Pager Services; 29 * Value Added Services; 30 * Other Charges and Credits; 31 * Network and Access; 32 * HST - BC; 33 * HST - AB; 34 * HST - SK; 35 * HST - MB; 36 * HST - ON; 37 * HST - PE; 38 * HST - NB; 39 * HST - NS; 40 * HST - NT; 41 * HST - NF; 42 * HST - PQ; 43 * HST - YT; 44 * HST - NU; 45 * PST - BC; 46 * PST - AB; 47 * PST - SK; 48 * PST - MB; 49 * PST - ON; 50 * PST - PE; 51 * QST; 52 * Subtotal before GST; 53 * GST; 54 * Total Current Charges; 55 * Total Charges and Adjustments; ×
    #0 * 31564264; 1 * 2017-07-14; 2 * GACEQ - CIUSSS DE; 3 * L'EST-DE-L'ILE-DE-MONTREAL; 4 * ; 5 * 031564264013; 6 * C; 7 * 5142362453; 8 * IUSMM; 9 * 7340205; 10 * VILOUNHA PHANALASY; 11 * ; 12 * ; 13 * ; 14 * 0.00; 15 * 0.00; 16 * 0.00; 17 * 0.00; 18 * GACEQ voice plan; 19 * 0.75; 20 * 2.25; 21 * Under; 22 * 0.00; 23 * 0.00; 24 * 0.00; 25 * 0.00; 26 * 29.00; 27 * 0.00; 28 * 0.00; 29 * 2.00; 30 * 0.00; 31 * 0.00; 32 * 0.00; 33 * 0.00; 34 * 0.00; 35 * 0.00; 36 * 0.00; 37 * 0.00; 38 * 0.00; 39 * 0.00; 40 * 0.00; 41 * 0.00; 42 * 0.00; 43 * 0.00; 44 * 0.00; 45 * 0.00; 46 * 0.00; 47 * 0.00; 48 * 0.00; 49 * 0.00; 50 * 0.00; 51 * 3.38; 52 * 37.38; 53 * 1.70; 54 * 39.08; 55 * 39.08; ×
    #
    for rr in r:
        s+=str(i)+" * "+rr+"; "
        i+=1
    response.flash = s
    
    count = db.account_department.id.count()
    rs=db(db.account_department.account>0).select(db.account_department.account,count,groupby=db.account_department.account)
    msg="tttt"
    for r in rs:
        if r[count]>0:
            msg+=r.account_department.account+"---"+str(r[count])+";"
    response.flash =len(rs)
    
    #db(db.account_department.account>0).delete()
    """
    #db(db.account_department.id>0).update(account_nature="5315")
    
    #db.invoice_file.truncate()
    #db.invoices.truncate()
    #db(db.account_department.id>0).delete()
    #db.client_departments.truncate()
    #db.managers_to_account.truncate()
    ###db.account_department.truncate()#Cannot truncate table 'account_department' because it is being referenced by a FOREIGN KEY constraint.

    #db.cap_file.truncate()
    #db(db.client_departments.id>0).update(is_active=True)
    #import base64
    #rs=db.invoice_file.insert(user_id=1117,invoice_type='Telus facture',description='test',files='testname.txt',file_data=base64.b64encode("123456aaaa"))
    #response.flash = rs
    """
    #good example
    import os
    file_name='temp.csv'
    this_file=open(file_name, 'w')
    this_file.write("mytext "+str(now))
    this_file.close()
    this_file=open(file_name, 'r')
    rs=db.invoice_file.insert(user_id=1117,invoice_type='Telus facture',description='csv file',files=db.invoice_file.files.store(this_file,file_name),file_data=this_file.read())
    response.flash = this_file
    this_file.close()
    """
    #db(db.invoices.Bill_Number=="31564264021").delete()
    #rs=db((db.invoices.Bill_Number==invoice_number)&(db.invoices.Sub_Level_B_Name==db.account_department.account)).select(db.invoices.ALL,db.account_department.account_type,limitby=(min_rec,max_rec))          
    #rs=db((db.invoices.Bill_Number=="031564264023")&(db.invoices.Sub_Level_B_Name==db.account_department.account)).select(db.invoices.ALL,db.account_department.account_type)          
    #response.flash=len(rs)

    #db(db.account_department.id>0).update(date_begin=datetime.datetime(2000,1,1),date_end=datetime.datetime(3000,1,1))
    #db(db.client_departments.id>0).update(date_begin=datetime.datetime(2000,1,1),date_end=datetime.datetime(3000,1,1))

    #import emails
    """
    rs=db(db.managers.id>0).select()
    for r in rs:
        ss=db(db.employees.full_name==r.name).select(db.employees.email)
        email=""
        for s in ss:
            if (s.email<>"")&(s.email<>email[:-1]):
                email+=s.email+";"
        email=email[:-1]
        db(db.managers.id==r.id).update(email=email)
    ###
    rs=db(db.managers.id>0).select()
    for r in rs:
        ss=db(db.employees.full_name==r.name).select(db.employees.email)
        email=""
        for s in ss:
            if (s.email<>"")&(s.email<>email[:-1])&("cemtl" not in email):
                if ("cemtl" in s.email):
                    email=s.email
                else:
                    email+=s.email+";"
        email=email[:-1]
        db(db.managers.id==r.id).update(email=email)
    ####
    rs=db(db.managers.id>0).select()
    for r in rs:
        ss=db(db.employees.full_name.like(r.name)).select(db.employees.email)
        email=""
        for s in ss:
            if (s.email<>"")&(s.email<>email[:-1])&("cemtl" not in email):
                if ("cemtl" in s.email):
                    email=s.email
                else:
                    email+=s.email+";"
        email=email[:-1]
        db(db.managers.id==r.id).update(email=email)

    #db(db.invoices.id>=319686).delete()

    if True:
        number=40
        invoice_file_date=datetime.datetime.strptime('2018-11-30','%Y-%m-%d').date()
        qry=(db.managers.id==1365)&(db.managers.id==db.managers_to_account.manager)&\
            (db.managers_to_account.account==db.account_department.id)&(db.account_department.account==db.invoices.Sub_Level_B_Name)\
            &(db.invoices.Total_Charges_and_Adjustments>=number)&(db.invoices.Bill_Date==invoice_file_date)
        this_rs=db(qry).select(
            db.account_department.account,
            db.invoices.Additional_Local_Airtime.sum(),
            db.invoices.Phone_Long_Distance_Charges.sum(),
            db.invoices.Roaming_Charges.sum(),
            db.invoices.Data_and_Other_Services.sum(),
            db.invoices.Value_Added_Services.sum(),
            db.invoices.Total_Charges_and_Adjustments.sum(),
            groupby=db.account_department.account)
        #response.flash=this_rs.first()[db.invoices.Total_Charges_and_Adjustments.sum()]
        #response.flash=this_rs.first()[db.account_department.account]
        response.flash=this_rs.last()[db.account_department.account]
    """



    #rs=db((db.invoices.Bill_Number=='031564264029')&(db.invoices.Sub_Level_B_Name==db.account_department.account)).select(db.invoices.ALL,db.account_department.account_type,limitby=(0,5000))          
    #rs=db((db.invoices.Bill_Number=='031564264029')).select(db.invoices.ALL,db.account_department.account_type,left=db.account_department.on(db.invoices.Sub_Level_B_Name==db.account_department.account),limitby=(0,5000))          


    #rs=db((db.client_departments.date_end==datetime.datetime(3000,1,1))&(db.client_departments.account==8597)).select()
    #for r in rs:
    #    db((db.client_departments.id==r.id)).update(account=13887)

    #rs=db((db.client_departments.date_end==datetime.datetime(3000,1,1))&(db.client_departments.account==8597)).select()
    #for r in rs:
    #    db((db.client_departments.id==r.id)).update(account=13887)

    #rs=db(db.client_departments.client_number.like('%-%')).select()
    #for r in rs:
    #    db((db.client_departments.id==r.id)).update(client_number=r.client_number.replace('-',''))
    
    #response.flash = len(rs)
    #db(db.client_departments.device_type=='Téléphones cellulaires').update(device_type='Téléphone cellulaire')
    #rs=db((db.client_departments.client_name.like('%ABONNE%')&(db.client_departments.account_type=='données')&(db.client_departments.date_end.year()==3000))).update(device_type='Portable avec carte SIM intégrée')
    #response.flash = rs
    #rs=db((db.client_departments.date_begin.year()>=2019)&(db.client_departments.date_end.year()==3000)).select()
    #response.flash = len(rs)
    #rs=db((db.client_departments.client_name.like('%ABONNE%')&(db.client_departments.account_type=='données')&(db.client_departments.date_end.year()==3000))).update(client_name="À ajouter",employee_number="À ajouter",job_tilte="À ajouter")
    #rs=db((db.client_departments.job_tilte=="à ajouter")).update(job_tilte="À ajouter")#,employee_number="À ajouter",job_tilte="À ajouter"
    #response.flash = rs
    
    #dept=(        6601201	,        6601202	,    )
    #rs=db(db.account_department.account.belongs(dept)).select(db.account_department.id)
    #response.flash = rs
    #for i in rs:
    #    db.managers_to_account.insert(manager=2652,account=i.id)
    #ids=(
    #    34867,
    #    35219,
    #)
    #rs=db(db.managers_to_account.id.belongs(ids)).update(manager=2654)
    #response.flash = rs

        


    return dict(grid=grid)


#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_edit')|auth.has_membership(role='gestion_factures_edit_add'))
@auth.requires_login()
def invoice_browser():

    if auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_read'):
        menu_navigator=[
            #(T('Navigateur de facture'), False, URL( f='invoice_browser'),[]),
            (T('Selection des gestionaires'), False, URL( f='manager_select'),[]),
        ]       
        response.menu = [
        (response.menu[0]), #Home - Page d'accueil
        (response.menu[1]), #Navigateur de facture
        (T("Navigateur de facture"), False, '#',menu_navigator),
        ]
    else:
        response.menu+=[
            (T('Navigateur de facture'), False, URL( f='invoice_browser'),[]),
            ]

    create=False
    deletable=False
    editable=False
    user_signature=False
    searchable=True
    details=True
    session.browser='invoice'
    if auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_read'):          
        if session.this_manager: #from manager_select
            if type(session.this_manager)==str:
                qry1=(db.managers.name==session.this_manager)
            else: #list
                qry1=(db.managers.name.belongs(tuple(session.this_manager)))
            depts=db(qry1&(db.managers.id==db.managers_to_account.manager)&(db.managers_to_account.account==db.account_department.id))._select(db.account_department.account)
            qry=db.invoices.Sub_Level_B_Name.belongs(depts)            
        else:
            qry=(db.invoices.id>0)
    else:
        #check if windows_code in managers table
        if not db(db.managers.windows_code==session.auth.user.username).count():
            import subprocess,os
            script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_factures\find_managers_names.ps1'
            arg1=session.auth.user.username
            #arg1="godi8300"
            p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output,error = p1.communicate()
            #output=output.decode('utf-8', 'ignore')
            output=output.replace('\r\n','').upper()
            output=escape(output)
            ls=output.split(";")
            this_tuple=()
            for l in ls:
                if l<>'': 
                    this_tuple+=(l,)
            r=db(db.managers.name.belongs(this_tuple)).select(db.managers.id).first()
            if r:
                db(db.managers.id==r.id).update(windows_code=session.auth.user.username)
            else:
                response.flash="Votre nom du AD "+str(this_tuple)+" n'est pas listé dans notre liste des gestionnaires ou n'est pas indentique. Contactez SVP le pilote du module 'GESTION DES FACTURES'"
            #response.flash = this_tuple
        # create qry
        depts=db((db.managers.windows_code==session.auth.user.username)&\
        (db.managers.id==db.managers_to_account.manager)&(db.managers_to_account.account==db.account_department.id))._select(db.account_department.account)
        qry=db.invoices.Sub_Level_B_Name.belongs(depts)

    fields=[db.invoices.Client_Number,db.invoices.Bill_Date,db.invoices.Bill_Number,db.invoices.User_Number,db.invoices.Sub_Level_B_Name,db.invoices.User_Name,db.invoices.Total_Current_Charges,db.invoices.Total_Charges_and_Adjustments]
    grid = SQLFORM.grid(qry,fields=fields,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    
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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_read'))
def manager_select():
    response.menu+=[
        (T('Selection des gestionaires'), False, URL( f='manager_select'),[]),
        ]    
    qry=db(db.managers.is_active==True)
    fields=[
        Field("manager",type='text',label=T('Getionnaire: '),comment=T("Selectionnez un ou plusieurs getionnaires !"),requires=IS_IN_DB(qry,'managers.name',multiple=True)),
    ]
    form=SQLFORM.factory(*fields)
    session.this_manager=False
    if form.accepts(request.vars,session,keepvalues=True):#pour eviter dernier ligne vide il viens de Powershell        
        session.this_manager=request.vars.manager
        if session.browser=='phone':
            redirect(URL('phone_browser'))    
        else:
            redirect(URL('invoice_browser'))    
    #response.flash = msg
    return dict(form=form)

@auth.requires_login()
def phone_browser():

    if auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_read'):
        menu_navigator=[
            #(T('Navigateur de facture'), False, URL( f='invoice_browser'),[]),
            (T('Selection des gestionaires'), False, URL( f='manager_select'),[]),
        ]       
        response.menu = [
        (response.menu[0]), #Home - Page d'accueil
        (response.menu[1]), #Navigateur de facture
        (T("Navigateur de téléphone"), False, '#',menu_navigator),
        ]
    else:
        response.menu+=[
            (T('Navigateur de téléphone'), False, URL( f='invoice_browser'),[]),
            ]

    create=False
    deletable=False
    editable=False
    user_signature=False
    searchable=True
    details=True
    session.browser='phone'
    if auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_read'):          
        if session.this_manager: #from manager_select
            if type(session.this_manager)==str:
                qry1=(db.managers.name==session.this_manager)
            else: #list
                qry1=(db.managers.name.belongs(tuple(session.this_manager)))
            depts=db(qry1&(db.managers.id==db.managers_to_account.manager)&(db.managers_to_account.account==db.account_department.id))._select(db.account_department.id)
            qry=db.client_departments.account.belongs(depts)            
        else:
            qry=(db.client_departments.id>0)
    else:
        #check if windows_code in managers table
        if not db(db.managers.windows_code==session.auth.user.username).count():
            import subprocess,os
            script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_factures\find_managers_names.ps1'
            arg1=session.auth.user.username
            #arg1="godi8300"
            p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output,error = p1.communicate()
            #output=output.decode('utf-8', 'ignore')
            output=output.replace('\r\n','').upper()
            output=escape(output)
            ls=output.split(";")
            this_tuple=()
            for l in ls:
                if l<>'': 
                    this_tuple+=(l,)
            r=db(db.managers.name.belongs(this_tuple)).select(db.managers.id).first()
            if r:
                db(db.managers.id==r.id).update(windows_code=session.auth.user.username)
            else:
                response.flash="Votre nom du AD "+str(this_tuple)+" n'est pas listé dans notre liste des gestionnaires ou n'est pas indentique. Contactez SVP le pilote du module 'GESTION DES FACTURES'"
            #response.flash = this_tuple
        # create qry
        depts=db((db.managers.windows_code==session.auth.user.username)&\
        (db.managers.id==db.managers_to_account.manager)&(db.managers_to_account.account==db.account_department.id))._select(db.account_department.id)
        qry=db.client_departments.account.belongs(depts)
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
def import_file():
    response.menu+=[
        (T('Entrepôt des fichiers'), False, URL( f='import_file'),[]),
        ]
    grid = SQLFORM.grid(db.invoice_file,orderby=~db.invoice_file.invoice_number,maxtextlength=70,\
    deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    response.flash = session.msg
    session.msg=None
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
def accounts_replacement():
    menu_url=[]
    tables={"Code budgétaire":"account_department","Numero de téléphone":"client_departments","Gestionaires aux code budgétaires":"managers_to_account","Gestionaires":"managers","Facture - détails":"invoices"}
    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]
    menu_url+=[(T('Remplacement de code budgétaire'), False, URL( f='accounts_replacement'),[]),]
    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    msg=""
    fields=[
        Field('accounts',type='text',label=T("Liste de code budgétaire"),length=30000,requires=IS_NOT_EMPTY(),\
        comment=T("On peut avoir environ 200 lignes de code budgétaire. Format: ancien code;nouveau code;date effective (example 2018-01-01 ou vide = aujourd'hui). Les deux codes budgétaires doivent être active. Les numéros de téléphone seront transférés vers le nouveau code budgétaire."),represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
    ]
    #. Format: ancien code;nouveau code;département;catégorie;date effective
    form = SQLFORM.factory(
        *fields,
        buttons=[]
    )
    buttons=[
        TD(INPUT(_type='submit',_value='remplacer',_id='remplacer',_name='remplacer',_style='background-color:#0066ff')),
    ]
    elements=TR(buttons)
    form[0][-1][1].insert(5,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        actions=[]
        accounts=request.vars.accounts.split('\r\n')
        for a in accounts:
            account=a.split(';')
            if len(account)==3:
                try:
                    if account[2]=="":
                        date_eff=today
                    else:
                        date_eff=datetime.datetime.strptime(account[2],'%Y-%m-%d')
                    #check account
                    source=db((db.account_department.account==account[0])&(db.account_department.is_active==True)).select(db.account_department.id).first().id
                    target=db((db.account_department.account==account[1])&(db.account_department.is_active==True)).select(db.account_department.id).first().id
                    date_end=date_eff-datetime.timedelta(days=1)
                    #this check if source & target exist if no will be exception error, and update source & target account
                    db(db.account_department.id==source).update(date_end=date_end,is_active=False)
                    db(db.account_department.id==target).update(date_begin=date_eff,is_active=True)
                    #find all client number with source account
                    rs=db((db.client_departments.account==source)).select()
                    new_numbers=[]
                    #create new number record
                    for r in rs:
                        new_numbers+=[{'account':target,'client_number':r.client_number,'client_name':r.client_name,'date_begin':date_eff,'date_end':datetime.datetime(3000,1,1),'is_active':r.is_active},]
                    db.client_departments.bulk_insert(new_numbers)
                    #update old client number
                    #db(db.client_departments.account==source).update(date_end=date_end,is_active=False)
                    db(db.client_departments.account==source).update(date_end=date_end)

                    this_action="FAIT;REMPLACEMENT DE CODE BUDGETAIRE;"+account[0]+";"+account[1]+";"+str(date_eff)
                except:
                    this_action="DONNEES-NON CONFORME;REMPLACEMENT DE CODE BUDGETAIRE;"+a
            else:
                this_action="FORMAT-NON CONFORME;REMPLACEMENT DE CODE BUDGETAIRE;"+a
                
            actions+=[{'edit_by':session.auth.user.id,'edit_time':now,'actions':this_action},]
        #insert tracking
        db.ads_actions_tracking.bulk_insert(actions)
        #msg=actions
    fields=[db.ads_actions_tracking.edit_time,db.ads_actions_tracking.actions]
    qry=(db.ads_actions_tracking.edit_by==session.auth.user.id)&(db.ads_actions_tracking.actions.like("%REMPLACEMENT DE CODE BUDGETAIRE%"))
    grid = SQLFORM.grid(qry,fields=fields,orderby=~db.ads_actions_tracking.id,maxtextlength=250,deletable=False,editable=False,create=False)
    response.flash=msg
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(role='admin'))
def import_data():
    response.menu+=[
        (T('Importation des données'), False, URL( f='import_data'),[]),
        ]
    #This good for importation
    fs=db(db.invoice_file.imported==False).select(db.invoice_file.id,db.invoice_file.file_data)
    #db(db.invoices.id>0).delete()
    #fs=db(db.invoice_file.id>0).select(db.invoice_file.file_data)
    msg="---"
    for f in fs:
        #db(db.invoice_file.id==f.id).update(imported=True)
        ls=f.file_data.split('\r\n')
        ls=ls[1:]
        i=0
        j=0
        not_found=""
        for l in ls:
            cs=l.split('\t')
            if len(cs)==3:  #>2 >1              
                """
                #use for importation first time code budgétaire
                #.strip() # to delete space
                name=cs[0]
                d=cs[1].split(' ')
                acc=d[1]
                dep=' '.join(d[3:])
                tacc=d[0]
                a=db(db.account_department.account==acc).select(db.account_department.id).first()
                if a: a=a.id
                else: a=db.account_department.insert(account=acc,department=dep,account_type=tacc,is_active=True)

                m=db(db.managers.name==name).select(db.managers.id).first()
                if m: m=m.id
                else: m=db.managers.insert(name=name,is_active=True)

                ma=db((db.managers_to_account.manager==m)&(db.managers_to_account.account==a)).select(db.managers_to_account.id).first()
                if not ma: ma=db.managers_to_account.insert(manager=m,account=a)    

                #update client_departments
                acc_id=db(db.account_department.account==cs[1]).select(db.account_department.id).first()
                if acc_id:
                    i+=1
                    db(db.client_departments.client_number==cs[2]).update(account=acc_id.id)

                #update client_departments
                acc_id=db(db.account_department.account==cs[1]).select(db.account_department.id).first()
                if acc_id:
                    i+=1
                    #db(db.client_departments.client_number==cs[2]).update(account=acc_id.id)
                else:
                    db(db.client_departments.client_number==cs[2]).update(old_account=cs[1])


                #Update code budget
                acc=cs[1]
                a=db(db.account_department.account==acc).select(db.account_department.id).first()
                if a: a=a.id
                else: a=db.account_department.insert(account=acc,department=cs[0],account_type="100171",is_active=True)
                
                #Update code budget 2 from GRF
                acc=cs[1]
                a=db(db.account_department.account==acc).select(db.account_department.id).first()
                if a: a=a.id
                else:
                    i+=1
                    a=db.account_department.insert(account=acc,department=cs[2],account_type=cs[0],is_active=True)
                
                ###Update_2018-03-14
                cs_0=cs[0].strip()
                cs_1=cs[1].strip()
                cs_2=cs[2].strip()
                #cs_0=cs[0]
                #cs_1=cs[1]
                #cs_2=cs[2]
                found_account=db(db.account_department.account==cs_1).select(db.account_department.id).first()
                if found_account: # account=code bugetaire exist
                    i+=1
                    #not_found+=[(i,cs_0,cs_1),]
                    found_number=db(db.client_departments.client_number==cs_0).select()
                    if found_number:
                        db(db.client_departments.client_number==cs_0).update(account=found_account.id,client_name=cs_2)
                    else:
                        db.client_departments.insert(account=found_account.id,client_number=cs_0,client_name=cs_2)
                else: #account=code bugetaire not exist
                    j-=1
                    not_found+=cs_0+"/t"+cs_1+"/t"+cs_2+"/r/n"
                    found_number=db(db.client_departments.client_number==cs_0).select()
                    if found_number:
                        db(db.client_departments.client_number==cs_0).update(account=9679,client_name=cs_2)
                    else:
                        db.client_departments.insert(account=9679,client_number=cs_0,client_name=cs_2)
                """
                
                



                #response.flash = str(not_found)   


    #i=0
    #rs=db(db.account_department.id>0).select()
    #for r in rs:
    #    if r.account<>(r.account).strip(): i+=1            
    #response.flash = str(i)
    
    grid=""    
    return dict(grid=str(not_found))

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_edit')|auth.has_membership(role='gestion_factures_edit_add'))
def invoice_import():
    grid =""
    #invoice importation
    fs=db((db.invoice_file.imported==False)&(db.invoice_file.invoice_type=='Telus facture')).select(db.invoice_file.id,db.invoice_file.file_data,orderby=db.invoice_file.dates)
    msg=""
    i=0
    for f in fs:
        #db(db.invoice_file.id==f.id).update(imported=True)
        ls=f.file_data.split('\r\n')
        ls=ls[1:]
        #check invoice# date and lenght>53
        ls0=ls[0].split('\t')
        Bill_Date1=ls0[1]
        Bill_Number=ls0[5]
        can_import=False
        if len(ls0)>53:
            if Bill_Number.isdigit():
                can_import=True
                try: Bill_Date=datetime.datetime.strptime(Bill_Date1, '%Y-%m-%d')
                except: can_import=False
        #msg+=str(can_import)+str(Bill_Number)+str(Bill_Date)
        if can_import:
            db(db.invoice_file.id==f.id).update(invoice_number=Bill_Number,dates=Bill_Date,imported=True)
            #Cleaning this invoice
            #db((db.invoices.Bill_Number==Bill_Number)&(db.invoices.Bill_Date==Bill_Date1)).delete()
            db((db.invoices.Bill_Number==Bill_Number)).delete()
            #db.commit()
            for l in ls:
                if l<>"":
                    cs=l.split('\t')

                    Client_Number=cs[0]
                    Bill_Date=cs[1]
                    Bill_Number=cs[5]
                    Product_Type=cs[6]
                    User_Number=cs[7].strip()
                    Sub_Level_A_Name=cs[8]
                    Sub_Level_B_Name=cs[9].strip()
                    #Sub_Level_B_Name=str(int(cs[9][1:]))
                    User_Name=cs[10]#.decode()
                    Reference_1=cs[12]
                    try:Service_Plan_Price=float(cs[19].replace(",","."))
                    except:Service_Plan_Price=0
                    try:Additional_Local_Airtime=float(cs[20].replace(",","."))
                    except:Additional_Local_Airtime=0
                    try:Phone_Long_Distance_Charges=float(cs[23].replace(",","."))
                    except:Phone_Long_Distance_Charges=0
                    try:Private_Group_Long_Distance_Charges=float(cs[24].replace(",","."))
                    except:Private_Group_Long_Distance_Charges=0
                    try:Roaming_Charges=float(cs[25].replace(",","."))
                    except:Roaming_Charges=0
                    try:Data_and_Other_Services=float(cs[26].replace(",","."))
                    except:Data_and_Other_Services=0
                    try:Value_Added_Services=float(cs[29].replace(",","."))
                    except:Value_Added_Services=0
                    try:QST=float(cs[51].replace(",","."))
                    except:QST=0
                    try:Subtotal_before_GST=float(cs[52].replace(",","."))
                    except:Subtotal_before_GST=0
                    try:GST=float(cs[53].replace(",","."))
                    except:GST=0
                    try:Total_Current_Charges=float(cs[54].replace(",","."))
                    except:Total_Current_Charges=0
                    try:Total_Charges_and_Adjustments=float(cs[55].replace(",","."))
                    except:Total_Charges_and_Adjustments=0


                    qry_client_active=(db.client_departments.date_begin<=Bill_Date)&(db.client_departments.date_end>=Bill_Date)&(db.client_departments.is_active==True)

                    number_exist=db((qry_client_active)&(db.client_departments.client_number==User_Number)&(db.client_departments.account==db.account_department.id))\
                    .select(db.client_departments.client_name,db.account_department.id,db.account_department.account,orderby=db.client_departments.id).last()
                    if number_exist: #client User_Number exist in table client_department (old phone number)
                        Sub_Level_B_Name=number_exist.account_department.account
                        User_Name=number_exist.client_departments.client_name
                    else: #client not exist in table client_department #new client  (new phone number)
                        i+=1
                        db.client_departments.insert( 
                            account=9679,
                            client_number=User_Number,
                            client_name=User_Name,
                            #date_begin=datetime.datetime(today.year,today.month,today.day),# not good replace by Bill_Date.date()
                            #date_begin=Bill_Date.date(), bad
                            date_begin=datetime.datetime.strptime(Bill_Date,'%Y-%m-%d'),
                            date_end=datetime.datetime(3000,1,1),
                            is_active=True,
                            )
                        Sub_Level_B_Name="xxx "+Sub_Level_B_Name
               
                    db.invoices.insert(
                        Client_Number=Client_Number,
                        Bill_Date=Bill_Date,
                        Bill_Number=Bill_Number,
                        Product_Type=Product_Type,
                        User_Number=User_Number,
                        Sub_Level_A_Name=Sub_Level_A_Name,
                        Sub_Level_B_Name=Sub_Level_B_Name,
                        User_Name=User_Name,
                        Reference_1=Reference_1,
                        Service_Plan_Price=Service_Plan_Price,
                        Additional_Local_Airtime=Additional_Local_Airtime,
                        Phone_Long_Distance_Charges=Phone_Long_Distance_Charges,
                        Private_Group_Long_Distance_Charges=Private_Group_Long_Distance_Charges,
                        Roaming_Charges=Roaming_Charges,
                        Data_and_Other_Services=Data_and_Other_Services,
                        Value_Added_Services=Value_Added_Services,
                        QST=QST,
                        Subtotal_before_GST=Subtotal_before_GST,
                        GST=GST,
                        Total_Current_Charges=Total_Current_Charges,
                        Total_Charges_and_Adjustments=Total_Charges_and_Adjustments,
                    )

                    #response.flash = len(cs)
               
    if i>0:
       session.msg = "Il y a "+str(i)+" numéros sans le code budgétaire"
    
    import_airtime()
 
    redirect(URL('import_file'))
    return dict(grid=grid)

def import_airtime():
    f=db((db.invoice_file.imported==False)&(db.invoice_file.invoice_type=='Telus AirtimeDetail')).select(db.invoice_file.id,db.invoice_file.file_data,orderby=~db.invoice_file.id).first()
    if f:
        ls=f.file_data.split('\r\n')
        ls=ls[1:]
        #check invoice# date and lenght>53
        ls0=ls[0].split('\t')
        Bill_Date1=ls0[1]
        Bill_Number=ls0[5]
        can_import=False
        if len(ls0)>27:
            if Bill_Number.isdigit():
                can_import=True
                try: Bill_Date=datetime.datetime.strptime(Bill_Date1, '%Y-%m-%d')
                except: can_import=False
            if can_import:
                db(db.invoice_file.id==f.id).update(invoice_number=Bill_Number,dates=Bill_Date,imported=True,exported=True,sent=True)
                #Cleaning this invoice
                #db((db.airtime_invoices.id>0)).delete()
                db.airtime_invoices.truncate()
                #ls=ls.replace('\t0\t','\t\t')
                for l in ls:
                    if l<>"":
                        cs=l.split('\t')
                        db.airtime_invoices.insert(
                            Numero_facture=cs[5],
                            Date_facturation=cs[1],
                            Numero_appareil=cs[8],
                            Nom_utilisateur=cs[9],
                            appel=cs[14],
                            Dates=cs[15],
                            Heure=cs[16],
                            Periode_appel=cs[17],
                            De=cs[18],
                            Numero_appele=cs[19],
                            A_=cs[20],
                            Type_appel=cs[21],
                            Duree=cs[22],
                            Frais_temps_antenne=cs[23],
                            Frais_temps_antenne_local=cs[24],
                            Frais_interurbain=cs[25],
                            Frais_appels_additionnels=cs[26],
                            Total=cs[27],
                        )                              

        session.msg=len(ls0)
    return

#one file
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
def export_csv():
    import os
    file_name='facture_telus_'+str(now).replace('.','').replace(':','').replace(' ','')+'.csv'
    this_file=open(file_name, 'w')
    #this_file.write(str(db(db.cap_file.id).select())) #just one line with head and number
    rs=db(db.cap_file.id).select()
    for r in rs:
        line=\
        r.Type_transaction+';'+\
        r.Nombre_enregistrements+';'+\
        r.No_founisseur+';'+\
        r.No_facture+';'+\
        r.Entite_principale+';'+\
        r.Description_facture+';'+\
        r.Entite_principale2+';'+\
        r.Periode_financiere+';'+\
        r.Date_facture+';'+\
        r.Date_echeance+';'+\
        r.Date_escompte+';'+\
        r.Montant_total+';'+\
        r.Reference_externe+';'+\
        r.Description_article+';'+\
        r.Entite_legale_CF+';'+\
        r.Entite_legale_article+';'+\
        r.Compte_GL_Financier+';'+\
        r.Code_primaire+';'+\
        r.Code_secondaire+';'+\
        r.Montant+';'+\
        r.Unites+';'+'\r\n'
        this_file.write(line)       
    this_file.close()
    this_file=open(file_name, 'r')
    #rs=db.invoice_file.insert(user_id=1117,invoice_type='Telus facture',description='csv file',files_csv=db.invoice_file.files_csv.store(this_file,file_name),file_data_csv=this_file.read())
    r=db(db.invoice_file.invoice_number==rs[0].No_facture).update(files_csv=db.invoice_file.files_csv.store(this_file,file_name),file_data_csv=this_file.read())
    #response.flash=r
    this_file.close()
    #delete the file
    os.remove(file_name)
    redirect(URL('import_file'))    
    return dict()
#zip and more files
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
def export_csvs_zip():
    import os
    rs=db(db.cap_file.id).select()
    i=1
    file_names=()
    if rs:
        this_date_facture=rs[0].Date_facture
        no_facture=rs[0].No_facture
        file_name=no_facture+'_'+str(i)+'.csv'
        this_file=open(file_name, 'w')
    j=0
    len_rs=len(rs)
    for r in rs:
        j+=1
        if r.No_facture<>"":
            No_facture=r.No_facture+'_'+str(i)
        else:
            No_facture=r.No_facture
        if j==1:
            number_invoice=';;;;;;'+r.No_facture
        else:
            number_invoice=''
            
        r_Montant=r.Montant.replace('.',',')
        line=\
        r.Type_transaction+';'+\
        r.Nombre_enregistrements+';'+\
        r.Date_echeance+';'+\
        r.Entite_principale2+';'+\
        r.Periode_financiere+';'+\
        r.Date_facture+';'+\
        r.Entite_principale+';'+\
        r.Date_escompte+';'+\
        r.Montant_total+';'+\
        r.Description_article+';'+\
        r.Entite_legale_article+';'+\
        r.Compte_GL_Financier+';'+\
        r.Code_primaire+';'+\
        r.Code_secondaire+';;;'+\
        r_Montant+';'+\
        r.Unites+';'+number_invoice+'\n'
        this_file.write(line)
        #end of file
        if r.Type_transaction=="99":
            this_file.close()
            file_names+=(file_name,)
            if j<len_rs:
                i+=1
                file_name=no_facture+'_'+str(i)+'.csv'
                this_file=open(file_name, 'w')
    #create zip file
    this_path= r'C:\Users\unificace\unificace\web2py'               
    file_name=no_facture+'_'+str(i)+'.zip'
    from os.path import basename
    import zipfile
    zf=zipfile.ZipFile(file_name, mode='w')
    try:
        for f in file_names:
            zf.write(this_path+'\\'+f,basename(this_path+'\\'+f))
    finally:
        zf.close()                    
    #this_file.close()
    this_file=open(file_name, 'rb')
    r=db(db.invoice_file.invoice_number==rs[0].No_facture).update(files_csv=db.invoice_file.files_csv.store(this_file,file_name),file_data_csv=this_file.read())
    #response.flash=r
    this_file.close()
    #delete the files zip and csvs
    os.remove(file_name)
    print file_names
    for f in file_names:
        os.remove(f)
        
    redirect(URL('import_file'))    
    return dict()

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
    
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
def export():
    
    rs=db((db.invoice_file.imported==True)&(db.invoice_file.exported==False)&(db.invoice_file.invoice_type=='Telus facture')).select(db.invoice_file.invoice_number,db.invoice_file.dates,db.invoice_file.description,db.invoice_file.id)
    menu_export=[]
    for r in rs:
        #menu_export+=[(T('Préparation la facture # '+r.invoice_number+' Date: '+str(r.dates)), False, URL( f='export_file',args=[r.invoice_number,r.description,str(r.dates),str(r.id),])),]
        menu_export+=[(T('Préparation la facture # '+r.invoice_number+' Date: '+str(r.dates)), False, URL( f='export',args=[r.invoice_number,r.description,str(r.dates),str(r.id),])),]
    #menu_export+=[(T("Exportation le CSV vers l'entrepôt des fichiers"), False, URL( f='export_csv'),[]),]#export_csvs_zip
    menu_export+=[(T("Exportation le CSV vers l'entrepôt des fichiers"), False, URL( f='export_csvs_zip'),[]),]
    response.menu = [
    (response.menu[0]), #Home - Page d'accueil
    (response.menu[1]), #Gestion des factures
    (T("Exportation"), False, '#',menu_export),
    ]
    
    invoice_number=request.args(0) or '0'
    invoice_description=request.args(1) or 'Besoin une description de la facture dans le menu CHARGEMNET DE FICHIER'
    invoice_dates=request.args(2) or 'Besoin une description de la facture dans le menu CHARGEMNET DE FICHIER'
    #invoice_id=request.args(3)
    if invoice_number<>'0':
        
        db(db.invoice_file.id==long(request.args(3))).update(exported=True)# do not export again
        db.cap_file.truncate()#delete and count reset for cap_file
        min_rec=0
        #max_rec=900
        max_rec=5000
        #rs=db(db.invoices.Bill_Number==invoice_number).select(db.invoices.ALL,limitby=(min_rec,max_rec))
        #rs=db((db.invoices.Bill_Number==invoice_number)&(db.invoices.Sub_Level_B_Name==db.account_department.account)).select(db.invoices.ALL,db.account_department.account_type,limitby=(min_rec,max_rec))          
        rs=db((db.invoices.Bill_Number==invoice_number)).select(db.invoices.ALL,db.account_department.account_type,db.account_department.account_nature,left=db.account_department.on(db.invoices.Sub_Level_B_Name==db.account_department.account),limitby=(min_rec,max_rec))          
        while rs:
            export_to_3(rs,invoice_dates,invoice_number,invoice_description)
            #min_rec+=900
            min_rec+=5000
            #max_rec+=900
            max_rec+=5000
            #rs=db(db.invoices.Bill_Number==invoice_number).select(db.invoices.ALL,limitby=(min_rec,max_rec))
            #rs=db((db.invoices.Bill_Number==invoice_number)&(db.invoices.Sub_Level_B_Name==db.account_department.account)).select(db.invoices.ALL,db.account_department.account_type,limitby=(min_rec,max_rec))          
            rs=db((db.invoices.Bill_Number==invoice_number)).select(db.invoices.ALL,db.account_department.account_type,left=db.account_department.on(db.invoices.Sub_Level_B_Name==db.account_department.account),limitby=(min_rec,max_rec))          
 
    qry=db.cap_file.id>0
    #just for remove the id from export file
    fields=(
        db.cap_file.Type_transaction,
        db.cap_file.Nombre_enregistrements,
        db.cap_file.No_founisseur,
        db.cap_file.No_facture,
        db.cap_file.Entite_principale,
        db.cap_file.Description_facture,
        db.cap_file.Entite_principale2,
        db.cap_file.Periode_financiere,
        db.cap_file.Date_facture,
        db.cap_file.Date_echeance,
        db.cap_file.Date_escompte,
        db.cap_file.Montant_total,
        db.cap_file.Reference_externe,
        db.cap_file.Description_article,
        db.cap_file.Entite_legale_CF,
        db.cap_file.Entite_legale_article,
        db.cap_file.Compte_GL_Financier,
        db.cap_file.Code_primaire,
        db.cap_file.Code_secondaire,
        db.cap_file.Montant,
        db.cap_file.Unites,
        )

    grid = SQLFORM.grid(qry,fields=fields,maxtextlength=70,\
    deletable=False,editable=False,create=False,user_signature=user_signature,searchable=searchable,details=False)

    #redirect(URL('export_csvs_zip'))    
    return dict(grid=grid)

def export_to_3(rs,invoice_dates,invoice_number,invoice_description):
    if True:
        amount=0
        tps=0
        tvq=0
        date_faturation=invoice_dates.split('-')
        date_faturation=datetime.date(int(date_faturation[0]),int(date_faturation[1]),int(date_faturation[2]))
        date_finan=date_financial(date_faturation)
        line0=db.cap_file.insert(\
            Type_transaction="10",\
            No_founisseur="1013786",\
            No_facture=invoice_number,\
            Entite_principale="1001",\
            Description_facture=invoice_description,\
            Entite_principale2=str(date_finan[0]),\
            Periode_financiere=str(date_finan[1]),\
            Date_facture=invoice_dates.replace('-',''),\
            Date_echeance=session.auth.user.username,\
            Date_escompte="G20",\
            Montant_total="Repartition frais cellulaires",\
            # 12 total de facture  can be update in the end
            )
        
        #line1
        #d[19]=""# can be update in the end
        #line1=db.cap_file.insert(\
        #    Type_transaction="20",\
        #    Description_article="TPS a payer",\
        #    Entite_legale_article="1001",\
        #    Compte_GL_Financier="100141220040",\
        #    # 20 can be update in the end
        #    )

        #line2
        #line2=db.cap_file.insert(\
        #    Type_transaction="20",\
        #    Description_article="TVQ a payer",\
        #    Entite_legale_article="1001",\
        #    Compte_GL_Financier="100141220045",\
        #    # 20 can be update in the end
        #    )

        void_number=0
        for r in rs:
            account_code=r.invoices.Sub_Level_B_Name
            depense=r.invoices.Total_Current_Charges
            tps1=round((0.036094833*depense),2)
            tps+=tps1
            tvq1=round((0.044680402*depense),2)
            tvq+=tvq1
            #amount+=depense#before
            depense=depense-tps1-tvq1
            amount+=depense
            User_Number=r.invoices.User_Number
            if not User_Number:
                void_number+=1

            #rs=db((db.invoices.Bill_Number==invoice_number)&(db.invoices.Sub_Level_B_Name==db.account_department.account)).select(db.invoices.ALL,db.account_department.account_type,limitby=(min_rec,max_rec))          
            #define Entite_legale_article according to account_department.account_type #Field('account_type',label=T('Catégorie'),requires=IS_IN_SET(('','100171','100175'))),
            if r.account_department.account_type=='100175':
                Entite_legale_article="1005"
            elif r.account_department.account_type=='100172':
                Entite_legale_article="1002"
            elif r.account_department.account_type==None:
                Entite_legale_article="xxx"
            else:
                Entite_legale_article="1001"
            #r.account_department.account_nature     "5315"
            try:
                r_account_department_account_nature=r.account_department.account_nature
            except:
                r_account_department_account_nature="5315"

            db.cap_file.insert(\
                Type_transaction="20",\
                #Description_article=User_Number+'_'+r.invoices.User_Name,\
                Description_article=User_Number+'_'+invoice_dates.replace('-','')+'_'+r.invoices.User_Name,\
                Entite_legale_article=Entite_legale_article,\
                Code_primaire=account_code,\
                Code_secondaire=r_account_department_account_nature,\
                Montant=str(depense),\
                )
        #tps=round(amount*0.036094833,2)
        #tvq=round(amount*0.044680402,2)
        #db(db.cap_file.id==line0).update(Montant_total=str(amount))
        db.cap_file.insert(\
            Type_transaction="20",\
            Description_article="Repartition frais cellulaires",\
            Entite_legale_article="1001",\
            Compte_GL_Financier="100111131030",\
            Montant=str(-amount),\
            )
        #db(db.cap_file.id==line1).update(Montant=str(tps))
        #db(db.cap_file.id==line2).update(Montant=str(tvq))
        #db.cap_file.insert(Type_transaction="99",Nombre_enregistrements=str(len(rs)+4))#with 1 this record
        db.cap_file.insert(Type_transaction="99",Nombre_enregistrements=str(len(rs)+2))#with 1 this record
        if void_number>0:response.flash="Il y a "+str(void_number)+" ligne(s) sans numero"

    return True
#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_edit')|auth.has_membership(role='gestion_factures_edit_add'))
def tables():
    menu_url=[]
    tables={"Code budgétaire":"account_department","Numero de téléphone":"client_departments","Gestionaires aux code budgétaires":"managers_to_account","Gestionaires":"managers","Facture - détails":"invoices","Temps d'antenne - détails":"airtime_invoices"}
    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]
    menu_url+=[(T('Remplacement de code budgétaire'), False, URL( f='accounts_replacement'),[]),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]
    if request.args(0):
        #table = request.args(0) or 'managers'
        #if not table in db.tables(): redirect(URL('error'))
        table = request.args(0)
        if (table=="account_department"):
            grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,onvalidation=onvalidation_account_department)
        elif (table=="client_departments"):
            grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,onvalidation=onvalidation_client_departments)
        else:
            grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    else:
        grid = ""
    return dict(grid=grid)

def onvalidation_account_department(form):
    if request.vars.id:#good for add new too
        if form.vars.account<>db(db.account_department.id==request.vars.id).select(db.account_department.account).first().account:
            form.errors.account="Ce champ n'est pas éditable. Mais on peut ajouter un autre."
            form.errors= True
    return

def onvalidation_client_departments(form):
    #check record must be unique with his number and period (period can not overlap)

    if request.vars.id:
        source_account=db(db.client_departments.id==request.vars.id).select(db.client_departments.account).first().account
        account_changed=form.vars.account<>source_account

        client_number_changed=form.vars.client_number<>db(db.client_departments.id==request.vars.id).select(db.client_departments.client_number).first().client_number

        source_client_name=db(db.client_departments.id==request.vars.id).select(db.client_departments.client_name).first().client_name
        client_name_changed=form.vars.client_name<>source_client_name

        source_date_begin=db(db.client_departments.id==request.vars.id).select(db.client_departments.date_begin).first().date_begin
        date_begin_changed=form.vars.date_begin<>source_date_begin

        source_date_end=db(db.client_departments.id==request.vars.id).select(db.client_departments.date_end).first().date_end
        date_end_changed=form.vars.date_end<>source_date_end

        source_is_active=db(db.client_departments.id==request.vars.id).select(db.client_departments.is_active).first().is_active
        ##
        source_account_type=db(db.client_departments.id==request.vars.id).select(db.client_departments.account_type).first().account_type
        account_type_changed=form.vars.account_type<>source_account_type        

        source_device_type=db(db.client_departments.id==request.vars.id).select(db.client_departments.device_type).first().device_type
        device_type_changed=form.vars.device_type<>source_device_type

        source_infos=db(db.client_departments.id==request.vars.id).select(db.client_departments.infos).first().infos
        infos_changed=form.vars.infos<>source_infos        

        source_employee_number=db(db.client_departments.id==request.vars.id).select(db.client_departments.employee_number).first().employee_number
        employee_number_changed=form.vars.employee_number<>source_employee_number
        
        source_job_tilte=db(db.client_departments.id==request.vars.id).select(db.client_departments.job_tilte).first().job_tilte
        job_tilte_changed=form.vars.job_tilte<>source_job_tilte        
        ###

        #for detect is_active_changed
        if (form.vars.is_active==None)|(form.vars.is_active=='off'):
            form.vars.is_active=False
        else:
            form.vars.is_active=True
        is_active_changed=form.vars.is_active<>source_is_active

        if client_number_changed:
            form.errors.client_number="Ce champ n'est pas éditable. Mais on peut ajouter un autre."
            form.errors= True
        elif (account_changed & date_begin_changed)|(date_begin_changed & client_name_changed):
            if (date_end_changed|is_active_changed):
                if date_end_changed:
                    form.errors.date_end="Ce champ n'est pas éditable en même temps avec 'Code budgétaire', 'Date effective' ou 'Nom d'utilisateur'. Date l'original: "+ str(source_date_end)
                if is_active_changed:
                    form.errors.is_active="Ce champ n'est pas éditable en même temps avec 'Code budgétaire', 'Date effective' ou 'Nom d'utilisateur'."
                #form.errors.date_end=request.vars.is_active
                #form.errors.is_active=form.vars.is_active
                form.errors= True
            else:                    
                #create new record
                db.client_departments.insert(account=form.vars.account,client_number=form.vars.client_number,client_name=form.vars.client_name,date_begin=form.vars.date_begin,date_end=form.vars.date_end,is_active=form.vars.is_active,account_type=form.vars.account_type,device_type=form.vars.device_type,infos=form.vars.infos,employee_number=form.vars.employee_number,job_tilte=form.vars.job_tilte)
                #update this record
                form.vars.account=source_account
                form.vars.client_name=source_client_name
                form.vars.date_end=form.vars.date_begin-datetime.timedelta(days=1)
                form.vars.date_begin=source_date_begin
                ###
                form.vars.account_type=source_account_type
                form.vars.device_type=source_device_type
                form.vars.infos=source_infos
                form.vars.employee_number=source_employee_number
                form.vars.job_tilte=source_job_tilte
                ###
        elif account_changed:
            form.errors.account="Pour changer le code budgétaire, il faut aussi changer la date effective!"
            form.errors= True
        elif client_name_changed:
            form.errors.client_name="Pour changer le nom d'utilisateur, il faut aussi changer la date effective!"
            form.errors= True
        #form.errors.client_number=request.vars
        #form.errors= True
    return

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
def sending_messages_link():    

    rs=db((db.invoice_file.imported==True)&(db.invoice_file.sent==False)&(db.invoice_file.invoice_type=='Telus facture')).select(db.invoice_file.invoice_number,db.invoice_file.dates,db.invoice_file.description,db.invoice_file.id)
    menu_sent=[]
    for r in rs:
        menu_sent+=[(T('Envoi la facture # '+r.invoice_number+' Date: '+str(r.dates)), False, URL( f='sending_messages_link',args=[str(r.dates),])),]
    #if rs:#test
    #    menu_sent+=[(T('Envoi un courriel de test de la facture # '+'031564264043'+' Date: '+str('2019-12-31')), False, URL( f='sending_messages_link',args=[str('2019-12-31'),"test",])),]
    response.menu = [
        (response.menu[0]), #Home - Page d'accueil
        (response.menu[1]), #Gestion des factures
        (T('Envoi de messages aux gestionnaires'), False, '#',menu_sent),
    ]
    if session.amount==None:session.amount=32.00
    if session.message==None:session.message="<b>Vous trouverez ci-joint le fichier et les détails de facturation.</b>"
    if session.message_account==None:session.message_account="<b>Voici la liste des numéros et les noms des personnes associés aux centres de coûts.</b>"
    if session.message_detail==None:session.message_detail="<b>Voici les coûts totaux par centre de coût.</b>"
    fields=[
        Field('amount','double',label=T("Montant minimal:"),default=session.amount,comment=T("")),
        #Field('message',type='text',label=T("Message au CS:"),length=1024,requires=IS_NOT_EMPTY(),default=session.message,\
        #comment=T("Pour la section: Détails sur utilisation. Syntaxe des messages (syntaxe html): <b> gras </b> <i> italique </i> <p> paragraphe </p>"),represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
        #Field('message_account',type='text',label=T("Message au CS:"),length=1024,requires=IS_NOT_EMPTY(),default=session.message_account,\
        #comment=T("Pour la section: Numéros et les noms des personnes associés aux centres de coûts. 1024 caractères maximum."),represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
        #Field('message_detail',type='text',label=T("Message au DA:"),length=1024,requires=IS_NOT_EMPTY(),default=session.message_detail,\
        #comment=T("Détails sur utilisation. 1024 caractères maximum."),represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
        ]
    buttons=[
            #TD(INPUT(_type="submit",_value="Appliquer",_id="Appliquer",_name="Appliquer",_style="background-color:#0066ff")),
        ]
    grid=SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    grid[0][-1][1].insert(9,elements)

    if grid.accepts(request.vars,session,keepvalues=True):
        session.amount=request.vars.amount
        session.message=request.vars.message
        session.message_account=request.vars.message_account
        session.message_detail=request.vars.message_detail
        session.msg="Les modifications sont validées et prêt à envoyer."
        redirect(URL('sending_messages_link'))
    invoice_date=request.args(0) or '0'
    if invoice_date<>'0':
        import subprocess,json,uuid
        test=request.args(1) or '0'            
        data=dict(test=test,invoice_date=invoice_date,user_id=session.auth.user.id,number=float(session.amount),message=session.message,message_account=session.message_account,message_detail=session.message_detail)
        publish_id=uuid.uuid4().hex
        #insert data for subprocess
        db.app2app.insert(
            publish_id=publish_id,
            subscribe_id='',
            app='gestion_factures',
            status='new',
            command=json.dumps(data),
            response='',
        )
        db.commit()
        #"""
        ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_factures\gestion_factures_sending_messages_link.ps1'
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx])
        #marked as sent
        if test!='test':   
            db((db.invoice_file.dates==invoice_date)&(db.invoice_file.imported==True)&(db.invoice_file.invoice_type=='Telus facture')).update(sent=True)
        #"""
        session.msg="Envoi de messages en arrière-plan."
        #session.msg=request.args(1)
        redirect(URL('sending_messages_link'))
    #session.msg=session.amount
    response.flash=session.msg
    session.msg=None
    return dict(grid=grid)

def read_messages_link():
    grid=""
    msg=""
    #message_id=request.args(0) or '0'
    #passcode=request.args(1) or '0'
    message_id=request.vars.msg or '0'
    passcode=request.vars.send_id or '0'
    if((message_id=='1')|(message_id=='2'))&(passcode<>'0'):
        r=db((db.ads_actions_tracking.actions.like('%'+passcode+'%'))).select().first()
        if r:           
            passcode=passcode.split('_')
            r_id=int(passcode[1])
            invoice_file_date=passcode[2]
            invoice_file_date=datetime.datetime.strptime(invoice_file_date,'%Y-%m-%d').date()
            amount_max=float(passcode[3])
            msg=str(r_id)+"---"+str(invoice_file_date)
            if message_id=='1':
                #read Détails sur l’utilisation >30$
                qry=(db.managers.id==r_id)&(db.managers.id==db.managers_to_account.manager)&\
                (db.managers_to_account.account==db.account_department.id)&(db.account_department.account==db.invoices.Sub_Level_B_Name)\
                &(db.invoices.Total_Charges_and_Adjustments>amount_max)&(db.invoices.Bill_Date==invoice_file_date)
                fields=(db.invoices.Bill_Date,db.account_department.account,db.invoices.User_Number,db.invoices.User_Name,\
                db.invoices.Additional_Local_Airtime,db.invoices.Phone_Long_Distance_Charges,db.invoices.Roaming_Charges,\
                db.invoices.Data_and_Other_Services,db.invoices.Value_Added_Services,db.invoices.Total_Charges_and_Adjustments)
            elif message_id=='2':
                #read Les numéros et les noms des personnes associés aux centres de coûts
                qry=(db.managers.id==r_id)&(db.managers.id==db.managers_to_account.manager)&(db.managers_to_account.account==db.account_department.id)&\
                (db.account_department.id==db.client_departments.account)&\
                (db.client_departments.date_begin<=invoice_file_date)&(db.client_departments.date_end>=invoice_file_date)&(db.client_departments.is_active==True)
                fields=(db.account_department.account,db.client_departments.client_number,db.client_departments.client_name)
            grid = SQLFORM.grid(qry,fields=fields,maxtextlength=70,deletable=False,editable=False,create=False,user_signature=user_signature,searchable=searchable,details=False)
    else:
        pass
    #response.flash=request.vars   
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
def actions_tracking():
    response.menu+=[
        (T('Historique'), False, URL( f='actions_tracking'),[]),
        ]
    qry=(db.ads_actions_tracking.actions.like("%REMPLACEMENT DE CODE BUDGETAIRE%"))|(db.ads_actions_tracking.actions.like("%Message envoyé à%"))
    #fields=[db.ads_actions_tracking.edit_by,db.ads_actions_tracking.edit_time,db.ads_actions_tracking.actions]
    #,fields=fields
    grid = SQLFORM.grid(qry,orderby=~db.ads_actions_tracking.id,maxtextlength=250,deletable=False,editable=False,create=False,details=False)

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
