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
        (T('Gestion des factures'), False, URL( f='index'),[]), 
        (T('Navigateur de facture'), False, URL( f='invoice_browser'),[]),
        (T('Navigateur du téléphone'), False, URL( f='phone_browser'),[]),
        #(T('Téléversement du fichier'), False, URL( f='import_file'),[]),
        (T('Entrepôt des fichiers'), False, URL( f='import_file'),[]),
        (T('Importation'), False, URL( f='invoice_import'),[]),
        (T('Exportation'), False, URL( f='export_file'),[]),
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
        deletable=False
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

#@auth.requires(auth.has_membership(role='admin'))
@auth.requires_login()
def index():
    response.menu+=[
        (T('Gestion des factures'), False, URL( f='index'),[]),
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
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    
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
    return dict(grid=grid)

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
        for l in ls:
            cs=l.split('\t')
            if len(cs)>2:  #>2 >1              
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
                """

                
                



        response.flash = str(i)    


    #i=0
    #rs=db(db.account_department.id>0).select()
    #for r in rs:
    #    if r.account<>(r.account).strip(): i+=1            
    #response.flash = str(i)
    
    grid=""    
    return dict(grid=grid)

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_edit')|auth.has_membership(role='gestion_factures_edit_add'))
def invoice_import():
    grid =""
    fs=db(db.invoice_file.imported==False).select(db.invoice_file.id,db.invoice_file.file_data)
    #db(db.invoices.id>0).delete()
    #fs=db(db.invoice_file.id>0).select(db.invoice_file.file_data)
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
            db((db.invoices.Bill_Number==Bill_Number)&(db.invoices.Bill_Date==Bill_Date1)).delete()
            #db.commit()
            for l in ls:
                if l<>"":
                    cs=l.split('\t')

                    Client_Number=cs[0]
                    Bill_Date=cs[1]
                    Bill_Number=cs[5]
                    Product_Type=cs[6]
                    User_Number=cs[7]
                    Sub_Level_A_Name=cs[8]
                    Sub_Level_B_Name=cs[9]
                    User_Name=cs[10]
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

                    """
                    #This logic is : Telus's invoices are the the source of departments 
                    #Department
                    account_department=db(db.account_department.account==Sub_Level_B_Name).select(db.account_department.id)
                    if not account_department:
                        account_id=db.account_department.insert(
                            account=Sub_Level_B_Name,
                            department=''
                        )
                    else:
                        account_id=account_department[0].id

                    #This logic is : Telus's invoices are the the source of clients 
                    #Clients
                    if not db((db.client_departments.account==account_id)&(db.client_departments.client_number==User_Number)&(db.client_departments.client_name==User_Name)).select(db.client_departments.id):
                        
                        db.client_departments.insert(
                            account=account_id,
                            client_number=User_Number,
                            client_name=User_Name
                        )

                    #This logic is : Telus's invoices are not the the source of departments 
                    #Department
                    #This logic is : Telus's invoices are not the the source of clients 
                    #Clients
                    r=db((db.client_departments.is_active==True)&(db.client_departments.client_number==User_Number)&(db.client_departments.account==db.account_department.id))\
                    .select(db.client_departments.client_name,db.account_department.account,orderby=db.client_departments.id).last()
                    if r:
                        Sub_Level_B_Name=r.account_department.account
                        User_Name=r.client_departments.client_name

                    #import for first time

                    account_department=db(db.account_department.account==Sub_Level_B_Name).select(db.account_department.id).first()
                    if account_department:
                        account_id=account_department.id
                    else: # not exist in table account_department
                        account_id=9679
                        Sub_Level_B_Name="xxx"
                    #####to work here
                    client_department=db((db.client_departments.account==account_id)&(db.client_departments.client_number==User_Number)&\
                    (db.client_departments.client_name==User_Name)).select(db.client_departments.id).first()
                    if not client_department:
                        db.client_departments.insert( account=account_id,client_number=User_Number,client_name=User_Name)
                    
                    """
                    ad=db((db.client_departments.is_active==True)&(db.client_departments.client_number==User_Number)&\
                    (db.client_departments.account==db.account_department.id))\
                    .select(db.client_departments.client_name,db.account_department.account,orderby=db.client_departments.id).last()
                    if ad:
                        Sub_Level_B_Name=ad.account_department.account
                        User_Name=ad.client_departments.client_name
                    else: # not exist in table client_department
                        i+=1
                        db.client_departments.insert( account=9679,client_number=User_Number,client_name=User_Name)
                        Sub_Level_B_Name="xxx "+Sub_Level_B_Name

                    

                    #Invoices                 
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
        response.flash = "Il y a "+str(i)+" numéros sans le code budgétaire"

    redirect(URL('import_file'))
    return dict(grid=grid)

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
def export_file():
    
    rs=db((db.invoice_file.imported==True)&(db.invoice_file.exported==False)).select(db.invoice_file.invoice_number,db.invoice_file.dates,db.invoice_file.description,db.invoice_file.id)
    menu_export=[]
    for r in rs:
        #menu_export+=[(T('Exporter la facture # '+r.invoice_number+' Date: '+str(r.dates)), False, URL( f='export_file',args=[r.invoice_number,r.description,str(r.dates),str(r.id),])),]
        menu_export+=[(T('Préparation la facture # '+r.invoice_number+' Date: '+str(r.dates)), False, URL( f='export_file',args=[r.invoice_number,r.description,str(r.dates),str(r.id),])),]
    menu_export+=[(T("Exportation le CSV vers l'entrepôt des fichiers"), False, URL( f='export_csv'),[]),]
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
        #rs=db((db.invoices.Bill_Number==invoice_number)&((db.invoices.User_Number<>"")|(db.invoices.User_Number<>None))).select()
        #rs=db(db.invoices.id==long(request.args(3))).select()
        rs=db(db.invoices.Bill_Number==invoice_number).select()

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
            # 12 total de facture  can be update in the end
            )
        
        #line1
        #d[19]=""# can be update in the end
        line1=db.cap_file.insert(\
            Type_transaction="20",\
            Description_article="TPS a payer",\
            Entite_legale_article="1001",\
            Compte_GL_Financier="100141220040",\
            # 20 can be update in the end
            )

        #line2
        line2=db.cap_file.insert(\
            Type_transaction="20",\
            Description_article="TVQ a payer",\
            Entite_legale_article="1001",\
            Compte_GL_Financier="100141220045",\
            # 20 can be update in the end
            )

        void_number=0
        for r in rs:
            account_code=r.Sub_Level_B_Name
            """
            # old calcule
            #if True:
            #if account_code<>'xxx':
            try:gst=float(r.GST)
            except:gst=0.
            gst1=round((gst-(gst*.17)),2)
            try:qst=round((float(r.QST)),2)
            except:qst=0.
            qst1=round((qst-(qst*.485)),2)
            #depense=round((r.Total_Charges_and_Adjustments-gst1-qst1),2)
            depense=round((r.Total_Current_Charges-gst1-qst1),2)
            amount+=depense
            #amount+=r.Total_Charges_and_Adjustments
            tps+=gst1
            tvq+=qst1
            """
            #depense=round((r.Total_Current_Charges),2)
            #amount+=depense
            depense=r.Total_Current_Charges
            tps1=round((0.036094833*depense),2)
            tps+=tps1
            tvq1=round((0.044680402*depense),2)
            tvq+=tvq1
            amount+=depense
            depense=depense-tps1-tvq1

            User_Number=r.User_Number
            if not User_Number:
                void_number+=1
            db.cap_file.insert(\
                Type_transaction="20",\
                Description_article=User_Number+'_'+r.User_Name,\
                Entite_legale_article="1001",\
                Code_primaire=account_code,\
                Code_secondaire="5315",\
                Montant=str(depense),\
                )
        #tps=round(amount*0.036094833,2)
        #tvq=round(amount*0.044680402,2)
        db(db.cap_file.id==line0).update(Montant_total=str(amount))
        db(db.cap_file.id==line1).update(Montant=str(tps))
        db(db.cap_file.id==line2).update(Montant=str(tvq))
        db.cap_file.insert(Type_transaction="99",Nombre_enregistrements=str(len(rs)+4))#with 1 this record
        if void_number>0:response.flash="Il y a "+str(void_number)+" ligne(s) sans numero"
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
    #grid = SQLFORM.grid(qry,fields=fields,maxtextlength=70,\
    #deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
    grid = SQLFORM.grid(qry,fields=fields,maxtextlength=70,\
    deletable=False,editable=False,create=False,user_signature=user_signature,searchable=searchable,details=False)
        
        
    return dict(grid=grid)

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures'))
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_factures')|auth.has_membership(role='gestion_factures_edit')|auth.has_membership(role='gestion_factures_edit_add'))
def tables():
    menu_url=[]
    #tables=["account_department","client_departments","manager_to_account","invoice_file","invoices"]
    #tables={"Départements":"account_department","Clients":"client_departments","Gestionaires":"managers_to_account","Fichiers de facture":"invoice_file","Factures":"invoices"}
    tables={"Départements":"account_department","Clients":"client_departments","Gestionaires aux départements":"managers_to_account","Gestionaires":"managers"}

    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]

    #table = request.args(0) or 'invoice_file'
    table = request.args(0) or 'managers'
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
