# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

response.menu += [
    (T("Gestion des inventaires"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]), 
        (T("Réception marchandise"), False, URL( f='inventory_input'),[]),
        (T("Entrepôt des fichiers Octopus"), False, URL( f='octopus_files'),[]),
        (T("Réexportation"), False, URL( f='reexport'),[]),
        (T("Dernière log d'exportation"), False, URL( f='log_file'),[]),
        (T("Entrepôt des fichiers impression"), False, URL( f='label_files'),[]),
        (T("Réimpression"), False, URL( f='reprinting'),[]),
        (T("Historique"), False, URL( f='all_items'),[]),
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        (T('Gestion des accès au module'), False, URL( f='module_access_create'),[]),
    ])
]
inventaires_groups=(1042,1043,1044)
import datetime,time
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
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_inventaires')):
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_inventaires_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_inventaires_edit')|auth.has_membership(role='gestion_inventaires_reimpression')):
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

try: 
    auth_id=session.auth.user.id
except:
    auth_id=1

#@auth.requires(auth.has_membership(role='admin'))
#@auth.requires_login()
def index():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        ]
    grid=""
    session.this_manager=False

    #db(db.managers.id>0).update(notification="")
    #db(db.inv_supplier.id>0).update(phone="",fax="")
    #db(db.inv_cis.id>0).update(infos="")
    #db(db.inv_cis.id>0).update(
    #    importation=False,
    #    SourceDeFinancement="",
    #    TypeDeGarantie="",
    #    DureeDAmortissement="",
    #    CoutDAchat="",
    #    NoDeFacture="",
    #    ExpirationDeLaGarantie="",
    #    )      
    #db(db.inv_cis.id>0).update(impression_index=0)
    #db(db.inv_cis.id>0).update(edit_by=1072,edit_time=now)
    #db(db.inv_cis.id>0).update(imei='')
    #rs=db(db.client_departments.id>0).select()
    #for r in rs:
    #    db(db.client_departments.id==r.id).update(client_number=r.client_number.replace('-',''))
    #rs=db(db.inv_cis.Nom.like('CLM%')).update(impression=True)
    #response.flash=rs

    #phone_number="514-260-0310"
    #client_number=phone_number.replace('-','')
    #client_number=client_number.replace(' ','')
    #phone_found=db((db.client_departments.client_number==client_number)&(db.client_departments.date_end==datetime.datetime(3000,1,1))&(db.client_departments.is_active==True)).select(db.client_departments.id,orderby=db.client_departments.id).last()
    #response.flash=str(phone_found)

    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def inventory_input():
    response.menu+=[
        (T("Réception marchandise"), False, URL( f='inventory_input'),[]),
        (T("Préparation pour exportation"), False, URL( f='inventory_import'),[]),
        (T("Impression d'étiquettes"), False, URL( f='inventory_impression'),[]),
        #(T("impression d'étiquettes ( PTouch)"), False, URL( f='inventory_impression_pt'),[]),
        ]
    msg=""
    grid=""
    if request.vars.type_ci: have_type_ci=True
    else: have_type_ci=False
    if request.vars.manufacturer: have_manufacturer=True
    else: have_manufacturer=False
    if have_type_ci & have_manufacturer:
        if request.vars.type_ci in ("Ordinateur","Ordinateur portatif",):
            qry_model=db((db.inv_model.name=='_'))
        else: 
            qry_model=db((db.inv_type_ci.name==request.vars.type_ci)&(db.inv_manufacturer.name==request.vars.manufacturer)&(db.inv_model.type_ci==db.inv_type_ci.id)&(db.inv_model.manufacturer==db.inv_manufacturer.id))
        requires_model=IS_IN_DB(qry_model,'inv_model.name')
    else:
        requires_model=IS_IN_DB(db(db.inv_model.id>0),'inv_model.name')

    if session.inventory_input_mode==None:
        session.inventory_input_mode="manual"

    if session.inventory_input_mode=="manual":
        form_keepvalues=True
        if session.date_purchase==None:date_purchase=today
        else:date_purchase=datetime.datetime.strptime(session.date_purchase, '%Y-%m-%d')
        if session.bill==None:bill=''
        else:bill=session.bill
        if session.oct_sr==None:oct_sr=''
        else:oct_sr=session.oct_sr
        if session.oct_cc==None:oct_cc=''
        else:oct_cc=session.oct_cc
        if not session.status:status='En Inventaire'
        else:status=session.status
        supplier=session.supplier
        local=session.local
        type_ci=session.type_ci
        manufacturer=session.manufacturer
        grm_code=session.grm_code if session.grm_code!=None else ''
        if not session.model:model='_'
        else:model=session.model
        if session.dimension==None:dimension=''
        else:dimension=session.dimension
        commande=session.commande
        if not session.qty:qty=1
        else:qty=session.qty

        if not session.funding_source:funding_source="Informatique"
        else:funding_source=session.funding_source
        if not session.warranty_type:warranty_type="Pièces et main d'oeuvre"
        else:warranty_type=session.warranty_type
        if not session.depreciation_period:depreciation_period=36
        else:depreciation_period=session.depreciation_period
        if not session.purcharse_cost:purcharse_cost=0.0
        else:purcharse_cost=session.purcharse_cost
        if not session.invoice_number:invoice_number=""
        else:invoice_number=session.invoice_number
        if not session.warranty_end_date:warranty_end_date=""
        else:warranty_end_date=session.warranty_end_date
        


        fields=[
            Field('date_purchase','date',label=T("Date d'achat"),default=date_purchase,requires=IS_DATE()),#requires = IS_EMPTY_OR(IS_DATE())#session.date_purchase
            Field('bill',label=T('Bon de commande'),default=bill),#,requires=IS_INT_IN_RANGE(10146000, 99999999)
            Field('oct_sr',label=T('Numéro de requête Octopus'),default=oct_sr),#,requires=IS_NOT_EMPTY()
            Field('funding_source',label=T('Source de financement'),requires=IS_IN_DB(db(db.inv_funding_source.id>0),'inv_funding_source.name'),default=funding_source),
            Field('oct_cc',label=T('Centre de coûts'),default=oct_cc,comment="Pour 'Compte Bilan' ou 'Maintien des actifs (MAI)', le centre de Coûts sera assigné automatiquement. Pour 'Mobilité' il faut mettre le 7535105"),
            Field('status',label=T('État'),requires=IS_IN_DB(db(db.inv_status.id>0),'inv_status.name'),default=status),
            Field('supplier',label=T('Fournisseur'),requires=IS_IN_DB(db(db.inv_supplier.id>0),'inv_supplier.name'),default=supplier),
            Field('local',label=T('Local'),requires=IS_IN_DB(db(db.inv_location.id>0),'inv_location.name'),default=local),
            Field('type_ci',label=T('Type'),requires=IS_IN_DB(db(db.inv_type_ci.id>0),'inv_type_ci.name'),default=type_ci),
            Field('manufacturer',label=T('Fabriquant'),requires=IS_IN_DB(db(db.inv_manufacturer.id>0),'inv_manufacturer.name'),default=manufacturer),
            Field('grm_code',label=T('RF - GRM'),default=grm_code,comment="Pour 'Compte Bilan' le numéro 'RF - GRM' est demandé"),
            Field('model',label=T('Modèle'),requires=requires_model,default=model,comment="Pour odinateur et ordinateur portatif selectionner: -"),
            Field('dimension',label=T('Dimension'),default=dimension),
            Field('qty','integer',label=T('Quantité'),default=qty),
            Field('warranty_type',label=T('Type de garantie'),requires=IS_IN_DB(db(db.inv_warranty_type.id>0),'inv_warranty_type.name'),default=warranty_type),
            Field('depreciation_period',label=T("Durée d'amortissement"),requires=IS_IN_DB(db(db.inv_depreciation_period.id>0),'inv_depreciation_period.name'),default=depreciation_period),
            Field('purcharse_cost','double',label=T("Coût d'achat"),default=purcharse_cost),
            Field('invoice_number',label=T('No. de facture'),default=invoice_number),
            Field('warranty_end_date','date',label=T("Expiration de la garantie"),default=warranty_end_date),
            ]

        buttons=[
            TD(INPUT(_type='submit',_value='actualiser',_id='actualiser',_name='actualiser',_style='background-color:#0066ff')),
            TD(INPUT(_type="submit",_value="suivant",_id="suivant",_name="suivant",_style="background-color:#0066ff")),
        ]
        if session.bill:
            buttons+=[TD(INPUT(_type='submit',_value='Préparation pour exportation',_id='Préparation pour exportation',_name='Préparation pour exportation',_style='background-color:#0066ff')),]
            session.export=True
        if session.export:
            buttons+=[TD(INPUT(_type='submit',_value="Impression d'étiquettes",_id="Impression d'étiquettes",_name="Impression d'étiquettes",_style='background-color:#0066ff')),]


        script = SCRIPT("""
                    document.addEventListener('keydown', function (event) {
                    if (event.keyCode === 13 && event.target.nodeName === 'INPUT') {
                        var form = event.target.form;
                        var index = Array.prototype.indexOf.call(form, event.target);
                        form.elements[index + 1].focus();
                        var x = document.getElementById("no_table_bill");
                        event.preventDefault();
                    }
                    });  
                    $('document').ready(function(){
                        document.getElementById("no_table_bill").focus();
                    });    
                """)
    else: #'scan'
        form_keepvalues=False
        if request.vars.has_key("suivant"):
            type_ci=request.vars.type_ci
        else:
            type_ci=session.type_ci 
        if type_ci in ("Ordinateur","Moniteur","Station d'accueil",):#request.vars.
            fields=[
                Field('serial',label=T('Numéro de série'),default=''),#,writable=False,readable=False
                ]
        #elif type_ci in ("Téléphone mobile","Dispositif internet mobile",):
        elif "Mobilité équipements" in type_ci:
            fields=[
                Field('serial',label=T('Numéro de série'),default=''),
                Field('imei',label=T('IMEI'),default=''),
                ]
        #elif type_ci in ("Ligne mobile",):
        elif "Mobilité Carte SIM" in type_ci:
            fields=[
                Field('account',label=T('Centre de coûts'),default=''),
                Field('principal_contact',label=T('Contact principal'),default=''),
                Field('phone',label=T('Numéro de téléphone'),default=''),
                Field('serial',label=T('Numéro de série'),default=''),
                ]
        else:
            fields=[
                Field('serial',label=T('Numéro de série'),default=''),
                Field('mac',label=T('Adresse MAC'),default=''),
                ]

        buttons=[
            TD(INPUT(_type="submit",_value="ajouter",_id="ajouter",_name="ajouter",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="arrêter",_id="arreter",_name="arreter",_style="background-color:#0066ff")),
        ]
        script = SCRIPT("""
                    document.addEventListener('keydown', function (event) {
                    if (event.keyCode === 13 && event.target.nodeName === 'INPUT') {
                        var form = event.target.form;
                        var index = Array.prototype.indexOf.call(form, event.target);
                        var toAdd = false;
                        form.elements[index + 1].focus();
                        $(":focus").each(function() {
                            if (this.id == "ajouter") {
                                //alert("Focused Elem_id = "+ this.id );
                                toAdd = true;
                            } else {
                                toAdd = false;
                            }
                        });
                        if (!toAdd){
                            event.preventDefault();
                        }
                    }
                    });  
                    $('document').ready(function(){
                        document.getElementById("no_table_serial").focus();                       
                    });    
                """)        

    #Réception marchandise
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(9,elements)

    if form.accepts(request.vars,session,keepvalues=form_keepvalues):
        if request.vars.has_key("suivant")|request.vars.has_key("actualiser"):
            session.date_purchase=str(request.vars.date_purchase)
            session.bill=request.vars.bill
            session.oct_sr=request.vars.oct_sr
            #session.oct_cc=request.vars.oct_cc
            session.status=request.vars.status
            session.supplier=request.vars.supplier
            session.local=request.vars.local
            session.type_ci=request.vars.type_ci
            session.manufacturer=request.vars.manufacturer
            session.grm_code=request.vars.grm_code
            if request.vars.model=='_':session.model=''
            else:session.model=request.vars.model
            session.dimension=request.vars.dimension
            session.qty=int(request.vars.qty)
            session.counter=0

            session.funding_source=request.vars.funding_source
            #session.oct_cc
            if session.funding_source in ("Compte Bilan","Maintien des actifs (MAI)"):
                centre_cout={"Compte Bilan":"100111150095","Maintien des actifs (MAI)":"10013244000050510"}
                session.oct_cc=centre_cout[session.funding_source]
            else:
                session.oct_cc=request.vars.oct_cc
            session.warranty_type=request.vars.warranty_type
            session.depreciation_period=request.vars.depreciation_period
            session.purcharse_cost=request.vars.purcharse_cost
            session.invoice_number=request.vars.invoice_number
            session.warranty_end_date=request.vars.warranty_end_date


            if request.vars.has_key("actualiser"):
                session.inventory_input_mode='manual'
            else:
                session.inventory_input_mode='scan'
            redirect(URL('inventory_input'))
        elif request.vars.has_key("arreter"):
            session.inventory_input_mode='manual'
            redirect(URL('inventory_input'))
        elif request.vars.has_key("ajouter"):
            max=db.inv_cis.Nom.max()
            #if True:
            try:
                #nom=db(db.inv_cis.TypeCi==session.type_ci).select(max).first()[max]
                if ("Mobilité équipements" in session.type_ci)|("Mobilité Carte SIM" in session.type_ci):
                    session_type_ci=session.type_ci.split(';')[0]+'%'
                else:
                    session_type_ci=session.type_ci
                nom=db(db.inv_cis.TypeCi.like(session_type_ci,case_sensitive=False)).select(max).first()[max]
                nom=nom.upper()
                #ci name
                ci_name=nom[:3]+(str(int(nom[3:])+1).zfill(5))
                if request.vars.mac==None:mac=""
                else:mac=request.vars.mac

                if request.vars.imei==None:imei=""
                else:imei=request.vars.imei

                if request.vars.phone==None:phone=""
                else:phone=request.vars.phone
                if request.vars.principal_contact==None:principal_contact=""
                else:principal_contact=request.vars.principal_contact
                infos=phone+";"+principal_contact

                if (request.vars.account==None):
                    account=session.oct_cc
                elif (request.vars.account==""):
                    account="7340205"
                else:
                    account=request.vars.account
                #if session.type_ci=="Ligne mobile":
                if "Mobilité Carte SIM" in session.type_ci:
                    account_found=db((db.account_department.account==account)&(db.account_department.is_active==True)).select(db.account_department.account).first()
                    if account_found:
                        account=account_found.account
                    else:
                        account="incorrect! "+account

                session.counter+=1
                NumeroBonCommande=session.bill if session.bill!=None else ''
                grm_code=session.grm_code if session.grm_code!=None else ''
                grm_code=grm_code if account=="100111150095" else ''
                db.inv_cis.insert(
                    Nom=ci_name,
                    Compteur=session.counter,
                    Total=session.qty,
                    NumeroBonCommande=NumeroBonCommande,
                    Requete=session.oct_sr,
                    CentreDeCouts=account,
                    NumeroSerie=request.vars.serial,
                    DateAchat=session.date_purchase,
                    TypeCi=session.type_ci,
                    AdresseIP="",
                    AdresseMAC=mac,
                    imei=imei,
                    Fournisseur=session.supplier,
                    Manufacturier=session.manufacturer,
                    grm_code=grm_code,
                    Modele=session.model,
                    #Site="IUSMM | Lahaise",
                    # Site="Institut universitaire en santé mentale de Montréal|Lahaise|Étage 05",
                    # Site="Institut universitaire en santé mentale de Montréal|Lahaise|Sous-Sol|LA-005-13",
                    Site="Institut universitaire en santé mentale de Montréal|Lahaise|Sous-Sol|"+session.local,
                    # Locals=session.local,
                    Locals="",
                    Etat=session.status,
                    Dimension=session.dimension,
                    impression=False,
                    impression_index=0,
                    importation=False,
                    infos=infos,
                    SourceDeFinancement=session.funding_source,
                    TypeDeGarantie=session.warranty_type,
                    DureeDAmortissement=session.depreciation_period,
                    CoutDAchat=session.purcharse_cost,
                    NoDeFacture=session.invoice_number,
                    ExpirationDeLaGarantie=session.warranty_end_date,
                    edit_by=auth_id,
                    edit_time=now,
                    )
            except:
                session.msg="Il faut ajouter ce type de ci dans les tables de configuration (TYPE de CI) et dernière numéro de ce type de ci dans historique (numéro doit dans cette form ABC12345) OU il y a double de série de même type CI."

        #end of scannig
        if session.counter>=session.qty:
            session.inventory_input_mode='manual'
            session.counter=0
            redirect(URL('inventory_input'))
    else:
        if (session.bill==None)|(session.bill==""):
            session.bill=request.vars.bill
        if (session.local==None)|(session.local==""):
            session.local=request.vars.local

    if request.vars.has_key("Préparation pour exportation"):
        redirect(URL('inventory_import'))
    elif request.vars.has_key("Impression d'étiquettes"):
        redirect(URL(f='inventory_impression'))

    qry=((db.inv_cis.impression==False)|(db.inv_cis.importation==False))&(db.inv_cis.edit_by==auth_id)
    orderby=~db.inv_cis.id
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=False,user_signature=user_signature,searchable=searchable,details=details,buttons_placement = 'left')

    response.flash=session.msg
    session.msg=None
    return dict(script=script,form=form,grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def inventory_import():
    session.msg=""
    grid=""
    rs=db((db.inv_cis.importation==False)&(db.inv_cis.edit_by==auth_id)).select()
    if rs:
        import os,uuid
        myfile='ci_csv'+uuid.uuid4().hex+'.csv'
        file_name=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_inventaires\octopus\\'+myfile
        this_file=open(file_name, 'w')
        
        # line="Nom;Type;Catégorie;NuméroSérie;Adresse Mac;NuméroBonCommande;Manufacturier;RF - GRM;Modèle;Site;Local;État;Dimension;NuméroInventaire;IMEI;Fournisseur;DateAchat;CentreCoûts;Adresse IP;Numéro de FAX (1);SourceFinancement;TypeGarantie;DuréeAmortissement;CoûtAchat;NuméroFacture;ExpirationGarantie;Réservé pour (en inventaire);No de téléphone;Note\n".decode('utf8').encode('ISO-8859-1')
        line="Nom;Type;Catégorie;NuméroSérie;Adresse Mac;NuméroBonCommande;Manufacturier;RF - GRM;Modèle;Site;Local;État;Dimension;NuméroInventaire;IMEI;Fournisseur;DateAchat;CentreCoûts;Adresse IP;CONFIG - FAX #1 Numéro;SourceFinancement;TypeGarantie;DuréeAmortissement;CoûtAchat;NuméroFacture;ExpirationGarantie;Réservé pour (en inventaire);No de téléphone;Note\n".decode('utf8').encode('ISO-8859-1')
        
      
        this_file.write(line)
        for r in rs:
            #line=r.Nom+";"+r.TypeCi+";"+r.NumeroSerie+";"+r.AdresseMAC+";"+r.NumeroBonCommande+";"+r.Manufacturier+";"+r.Modele+";"+r.Site+";"+r.Locals+";"+r.Etat+";"+r.Dimension+";;;"+r.Fournisseur+";"+str(r.DateAchat)+";;"+r.CentreDeCouts+"\n".decode('utf8').encode('ISO-8859-1')
            #python have big problem here need r.Etat.decode('utf8').encode('ISO-8859-1') before operation +
            #line=r.Nom+";"+r.TypeCi+";"+r.NumeroSerie+";"+r.AdresseMAC+";"+r.NumeroBonCommande+";"+r.Manufacturier+";"+r.Modele+";"+r.Site+";"+r.Locals+";"+r.Etat.decode('utf8').encode('ISO-8859-1')+";"+r.Dimension+";;;"+r.Fournisseur+";"+str(r.DateAchat)+";;"+r.CentreDeCouts+"\n"
            
            #if r.AdresseIP!="":adresse_ip="` "+r.AdresseIP #for dataimporter to treat as text
            #else:adresse_ip=""
            adresse_ip=r.AdresseIP
            
            #typeci and categories
            r_TypeCi=r.TypeCi.split(';')
            TypeCi=r_TypeCi[0]
            if len(r_TypeCi)>1:Category=r_TypeCi[1]
            else:Category=""
            inventoryNumber=""
            #original <2020-03-27
            # if  TypeCi=="Téléphone mobile":#Mobilité équipements
            #     Category="Cellulaire"
            # elif TypeCi=="Dispositif internet mobile":#Mobilité équipements
            #     Category="Clé USB internet"
            # elif TypeCi=="Ligne mobile":#Mobilité Carte SIM
            #     Category="Voix"
            #     inventoryNumber=r.Compteur
            if "Mobilité Carte SIM" in TypeCi:
                inventoryNumber=r.Compteur

                
            #serial number
            r_NumeroSerie=r.NumeroSerie
            ###
            if r_NumeroSerie:
                if len(r_NumeroSerie)>14:
                    r_NumeroSerie=r_NumeroSerie+'¤'#contourner excel Exponential

            ###
            if r_NumeroSerie[:1].lower()=='s':
                r_NumeroSerie=r_NumeroSerie[1:]
            #Réservé pour (en inventaire)
            if r.SourceDeFinancement in ("Compte Bilan","Maintien des actifs (MAI)","Projet"):
                reserve_pour_inventare=r.SourceDeFinancement #on a des errers pendant importation a Octopus a cause de manque de ce attributte dans certain CIs
                #reserve_pour_inventare=""
            else:
                reserve_pour_inventare=""
            
            # insert phone number  
            r_infos=r.infos.split(";")
            if len(r_infos)>1:principal_contact=r_infos[1]
            else:principal_contact=""

            #if TypeCi=="Ligne mobile":
            if "Mobilité Carte SIM" in TypeCi:
                phone_number=r_infos[0]
                fax_number=""
                if principal_contact=="":client_name="DRT-"+inventoryNumber+" "+r.Nom
                else:client_name=principal_contact
                account_found=db((db.account_department.account==r.CentreDeCouts)&(db.account_department.is_active==True)).select(db.account_department.id).first()
                if account_found:
                    account=account_found.id
                else:
                    account=9679
                    session.msg+=client_name+" , "+phone_number+" , "+r.CentreDeCouts+" , remplacé par XXX ; "
                ####
                client_number=phone_number.replace('-','')
                client_number=client_number.replace(' ','')
                phone_found=db((db.client_departments.client_number==client_number)&(db.client_departments.date_end==datetime.datetime(3000,1,1))&(db.client_departments.is_active==True)).select(db.client_departments.id,orderby=db.client_departments.id).last()
                if phone_found:
                    db(db.client_departments.id==phone_found.id).update(
                        account=account,
                        client_number=client_number,
                        client_name=client_name.upper(),
                        date_begin=datetime.datetime(today.year,today.month,today.day),
                        #date_end=datetime.datetime(3000,1,1),
                        #is_active=True,
                    )
                else:
                    db.client_departments.insert(
                        account=account,
                        client_number=client_number,
                        client_name=client_name.upper(),
                        date_begin=datetime.datetime(today.year,today.month,today.day),
                        date_end=datetime.datetime(3000,1,1),
                        is_active=True,
                    )
            else:
                phone_number=""
                fax_number=r_infos[0]
                
            
            #line=(r.Nom+";"+TypeCi+";"+Category+";"+r_NumeroSerie+";"+r.AdresseMAC+";"+r.NumeroBonCommande+";"+r.Manufacturier+";"+r.Modele+";"+r.Site+";"+r.Locals+";"+r.Etat+";"+r.Dimension+";"+inventoryNumber+";"+r.imei+";"+r.Fournisseur+";"+str(r.DateAchat)+";"+r.CentreDeCouts+";"+adresse_ip+";"+fax_number+";"+r.SourceDeFinancement+";"+r.TypeDeGarantie+";"+r.DureeDAmortissement+";"+r.CoutDAchat+";"+r.NoDeFacture+";"+r.ExpirationDeLaGarantie+";"+reserve_pour_inventare+";"+phone_number+";"+principal_contact+"\n").decode('utf8').encode('ISO-8859-1')
            line=(r.Nom+";"+TypeCi+";"+Category+";"+r_NumeroSerie+";"+r.AdresseMAC+";"+r.NumeroBonCommande+";"+r.Manufacturier+";"+r.grm_code+";"+r.Modele+";"+r.Site+";"+r.Locals+";"+r.Etat+";"+r.Dimension+";"+inventoryNumber+";"+r.imei+";"+r.Fournisseur+";"+str(r.DateAchat)+";"+r.CentreDeCouts+";"+adresse_ip+";"+fax_number+";"+r.SourceDeFinancement+";"+r.TypeDeGarantie+";"+r.DureeDAmortissement+";"+r.CoutDAchat+";"+r.NoDeFacture+";"+r.ExpirationDeLaGarantie+";"+reserve_pour_inventare+";"+phone_number+";"+principal_contact+"\n").decode('utf8').encode('ISO-8859-1')

            this_file.write(line)

            
        this_file.close()
        this_file=open(file_name, 'r')
        author=db(db.auth_user.id==auth_id).select(db.auth_user.username).first().username
        #db.oct_importation_files.insert(user_id=auth_id,types='CI',dates=now,description="Géneré par le module de gestion des inventaires :"+author,imported=True,files=db.oct_importation_files.files.store(this_file,file_name),file_data=this_file.read())
        db.oct_importation_files.insert(user_id=auth_id,team=1,types='CI',dates=now,description="Géneré par le module de gestion des inventaires :"+author,imported=False,files=db.oct_importation_files.files.store(this_file,file_name),file_data=this_file.read())
        this_file.close()
        db((db.inv_cis.importation==False)&(db.inv_cis.edit_by==auth_id)).update(importation=True) #mark as imported
        updated=db(db.inv_cis.Nom.like('CLM%')&(db.inv_cis.edit_by==auth_id)).update(impression=True) #mark as imprinted for all CLM Ling mobile
        
        os.remove(file_name)
        #os.remove(ini_name)

        #double update CLM Ling mobile
        if updated:
            rs=db(db.client_departments.id>0).select()
            for r in rs:
                db(db.client_departments.id==r.id).update(client_number=r.client_number.replace('-',''))

        redirect(URL('octopus_files'))
    else:
        session.msg="Il y a rien à importer."
        redirect(URL('inventory_input'))
    
    #response.flash=session.msg
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires')|auth.has_membership(role='gestion_inventaires_reimpression'))
def inventory_impression():
    if True:
        response.menu+=[
            (T("Réception marchandise"), False, URL( f='inventory_input'),[]),
            (T("Préparation pour exportation"), False, URL( f='inventory_import'),[]),
            (T("impression d'étiquettes"), False, URL( f='inventory_impression'),[]),
            #(T("impression d'étiquettes ( PTouch)"), False, URL( f='inventory_impression_pt'),[]),
            ]
        msg=""
        grid=""
        #reprinting_small #request.args(0)
        if (request.args(0)=="reprinting")|(request.args(0)=="reprinting_support")|(request.args(0)=="reprinting_small")|(session.bill==None)|(session.bill==''):
            qry=(db.inv_cis.impression==False)            
        else: 
            qry=(db.inv_cis.impression==False)&(db.inv_cis.NumeroBonCommande==session.bill)
        printer=db(db.inv_location.name==session.local).select().first()
        if  printer:
            count=db.inv_cis.NumeroBonCommande.count()
            count_total=db(qry).select(count).first()[count]
            rs=db(qry&(db.inv_cis.edit_by==auth_id)).select()
            if rs:
                import socket
                #TCP_IP = '10.49.24.37'
                #TCP_IP = printer.printer
                if (request.args(0)=="reprinting_support"):
                    redirect(URL('reprinting_support'))
                elif (request.args(0)=="reprinting_small"):
                    TCP_IP=(printer.printer).split(';')[1]
                else:
                    TCP_IP=(printer.printer).split(';')[0]
                TCP_PORT = 9100
                BUFFER_SIZE = 1024
                if (request.args(0)=="reprinting_small"):
                    # zpl_template= """
                    #     CT~~CD,~CC^~CT~
                    #     ^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD25^JUS^LRN^CI0^XZ
                    #     ^XA
                    #     ^MMT
                    #     ^PW408
                    #     ^LL0128
                    #     ^LS0
                    #     ^BY3,3,48^FT1,108^BCN,,N,N
                    #     ^FD>:_Nom_^FS
                    #     ^FT1,53^A0N,53,88^FH\^FD_Nom_^FS
                    #     ^FT1,132^A0N,28,33^FH\^FD_NumeroSerie_^FS
                    #     ^PQ1,0,1,Y^XZ
                    # """
                    zpl_template= """
                        CT~~CD,~CC^~CT~
                        ^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD10^JUS^LRN^CI0^XZ
                        ^XA
                        ^MMT
                        ^PW408
                        ^LL0128
                        ^LS0
                        ^BY3,3,48^FT1,108^BCN,,N,N
                        ^FD>:_Nom_^FS
                        ^FT1,53^A0N,53,88^FH\^FD_Nom_^FS
                        ^FT1,132^A0N,28,33^FH\^FD_NumeroSerie_^FS
                        ^PQ1,0,1,Y^XZ
                    """
                else:
                    # zpl_template= """
                    #     CT~~CD,~CC^~CT~
                    #     ^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD25^JUS^LRN^CI0^XZ
                    #     ^XA
                    #     ^MMT
                    #     ^PW408
                    #     ^LL1087
                    #     ^LS0
                    #     ^BY4,3,68^FT324,394^BCB,,N,N
                    #     ^FD>;_Requete_^FS
                    #     ^BY4,3,160^FT276,908^BCB,,N,N
                    #     ^FD>:_Nom_^FS
                    #     ^BY3,3,48^FT21,1055^BCN,,N,N
                    #     ^FD>:_Nom_^FS
                    #     ^FT76,572^A0B,64,120^FH\^FD_Nom_^FS
                    #     ^FT21,994^A0N,53,88^FH\^FD_Nom_^FS
                    #     ^FT44,908^A0B,28,33^FH\^FDCommand\82 / QT\90^FS
                    #     ^FT316,908^A0B,23,52^FH\^FDSN: _NumeroSerie_^FS
                    #     ^FT21,1082^A0N,28,33^FH\^FD_NumeroSerie_^FS
                    #     ^FT92,908^A0B,28,45^FH\^FDItem : _Compteur_ / _Total_^FS
                    #     ^FT377,908^A0B,28,28^FH\^FD_DateAchat_^FS
                    #     ^FT157,394^A0B,39,50^FH\^FDPO: _NumeroBonCommande_^FS
                    #     ^FT223,394^A0B,44,64^FH\^FDSR: _Requete_^FS
                    #     ^FT376,394^A0B,28,38^FH\^FDTotal command\82: _count_total_^FS
                    #     ^PQ1,0,1,Y^XZ
                    # """
                    zpl_template= """
                        CT~~CD,~CC^~CT~
                        ^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD10^JUS^LRN^CI0^XZ
                        ^XA
                        ^MMT
                        ^PW408
                        ^LL1087
                        ^LS0
                        ^BY4,3,68^FT324,394^BCB,,N,N
                        ^FD>;_Requete_^FS
                        ^BY4,3,160^FT276,908^BCB,,N,N
                        ^FD>:_Nom_^FS
                        ^BY3,3,48^FT21,1055^BCN,,N,N
                        ^FD>:_Nom_^FS
                        ^FT76,572^A0B,64,120^FH\^FD_Nom_^FS
                        ^FT21,994^A0N,53,88^FH\^FD_Nom_^FS
                        ^FT44,908^A0B,28,33^FH\^FDCommand\82 / QT\90^FS
                        ^FT316,908^A0B,23,52^FH\^FDSN: _NumeroSerie_^FS
                        ^FT21,1082^A0N,28,33^FH\^FD_NumeroSerie_^FS
                        ^FT92,908^A0B,28,45^FH\^FDItem : _Compteur_ / _Total_^FS
                        ^FT377,908^A0B,28,28^FH\^FD_DateAchat_^FS
                        ^FT157,394^A0B,39,50^FH\^FDPO: _NumeroBonCommande_^FS
                        ^FT223,394^A0B,44,64^FH\^FDSR: _Requete_^FS
                        ^FT376,394^A0B,28,38^FH\^FDTotal command\82: _count_total_^FS
                        ^PQ1,0,1,Y^XZ
                    """
                zpl=""               
                for r in rs:
                    this_zpl=zpl_template
                    this_zpl=this_zpl.replace("_Nom_",r.Nom)
                    this_zpl=this_zpl.replace("_Compteur_",r.Compteur)
                    this_zpl=this_zpl.replace("_Total_",r.Total)
                    this_zpl=this_zpl.replace("_NumeroBonCommande_",r.NumeroBonCommande)
                    this_zpl=this_zpl.replace("_Requete_",r.Requete)
                    this_zpl=this_zpl.replace("_NumeroSerie_",r.NumeroSerie)
                    this_zpl=this_zpl.replace("_count_total_",str(count_total))
                    this_zpl=this_zpl.replace("_DateAchat_",str(r.DateAchat))
                    this_zpl=this_zpl+"\n"
                    zpl+=this_zpl
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((TCP_IP, TCP_PORT))
                    s.send(bytes(zpl))
                    s.close()
                    db((db.inv_cis.impression==False)&(db.inv_cis.edit_by==auth_id)).update(impression=True) #mark as printed
                    session.msg="Imprimé au "+printer.name
                except:
                    session.msg="Problème de connexion avec "+printer.name
                #session.msg=zpl
            else:
                session.msg="Il y a rien à imprimer."
        else:
            session.msg="Choisir un local!"

        if (request.args(0)=="reprinting_small")|(request.args(0)=="reprinting"):
            redirect(URL('reprinting'))
        else:
            redirect(URL('inventory_input'))    

    response.flash=session.msg
    session.msg=None
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def inventory_impression_pt():
    response.menu+=[
        (T("Réception marchandise"), False, URL( f='inventory_input'),[]),
        (T("Préparation pour exportation"), False, URL( f='inventory_import'),[]),
        (T("impression d'étiquettes"), False, URL( f='inventory_impression'),[]),
        #(T("impression d'étiquettes ( PTouch)"), False, URL( f='inventory_impression_pt'),[]),
        ]
    msg=""
    grid=""
    if session.bill<>None: 
        qry=(db.inv_cis.impression==False)&(db.inv_cis.NumeroBonCommande==session.bill)
    else:
        qry=(db.inv_cis.impression==False)
    if True:
        count=db.inv_cis.NumeroBonCommande.count()
        count_total=db(qry).select(count).first()[count]
        rs=db(qry).select()
        if rs:
            file_name=r'\\cemtl.rtss.qc.ca\cemtl\Ressources\Public\unificace_gestion_inventaires\data\inv_label_file.csv'
            try:
                import os
                os.remove(file_name)
            except:
                #session.msg="Le fichier <<\\cemtl.rtss.qc.ca\cemtl\Ressources\Public\unificace_gestion_inventaires\inv_label_file.csv>> est deja ouvert par le programe PTouche ou autre, il faut fermer le programe et reesayer encore!"
                redirect(URL('inventory_input')) 

            this_file=open(file_name, 'w')
            line="Nom,Compteur,Total,PO:,Requête,NuméroSérie,NB ITEM Commmande,Date d'achat\n".decode('utf8').encode('ISO-8859-1')
            this_file.write(line)
            for r in rs:
                #python have big problem here need r.Etat.decode('utf8').encode('ISO-8859-1') before operation +
                #line=(r.Nom+";"+r.Compteur+";"+r.Total+";"+r.NumeroBonCommande+";"+r.Requete+";"+r.NumeroSerie+";"+sum_total+"\n").decode('utf8').encode('ISO-8859-1')
                line=(r.Nom+","+r.Compteur+","+r.Total+","+r.NumeroBonCommande+","+r.Requete+","+r.NumeroSerie+","+str(count_total)+","+str(r.DateAchat)+"\n").decode('utf8').encode('ISO-8859-1')
                this_file.write(line)
            this_file.close()
            this_file=open(file_name, 'r')
            author=db(db.auth_user.id==auth_id).select(db.auth_user.username).first().username
            #inv_label_files
            db.inv_label_files.insert(user_id=auth_id,dates=now,description="L'étiquettes, géneré par le module de gestion des inventaires :"+author,files=db.inv_label_files.files.store(this_file,file_name),file_data=this_file.read(),impression=False)
            this_file.close()
            db((db.inv_cis.impression==False)&(db.inv_cis.edit_by==auth_id)).update(impression=True) #mark as printed
            redirect(URL('label_files'))
        else:
            session.msg="Il y a rien à imprimer."
            redirect(URL('inventory_input'))

    response.flash=session.msg
    session.msg=None
    return dict(grid=grid)

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def reprinting_support():
    msg=""
    rs=db((db.inv_cis.impression==False)&(db.inv_cis.edit_by==auth_id)&(db.inv_cis.TypeCi.like('Imprimante',case_sensitive=False))).select()
    if rs:
        import uuid,os
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, inch
        file_img=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_inventaires\affiche_support_universal.jpg'
    for r in rs:
        file_name=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_inventaires\\'+uuid.uuid4().hex+'.pdf'
        #from reportlab.lib.units import mm
        c=canvas.Canvas(file_name,pagesize=(8.5*inch,11.0*inch))
        c.drawImage(file_img,0.0*inch,0.0*inch, width=8.5*inch,height=11.0*inch,mask=None)
        c.setFont("Helvetica-Bold",22)
        c.drawString(2.25*inch,9.75*inch,"Informations techniques")
        c.drawString(2.35*inch,9.25*inch,"pour votre imprimante")

        c.setFont("Helvetica",20)

        c.drawString(1.0*inch,7.75*inch,"Nom de votre")
        c.drawString(1.0*inch,7.5*inch,"imprimante:")
        c.drawString(4.0*inch,7.5*inch,r.Nom)

        c.drawString(1.0*inch,6.75*inch,"Adresse IP:")
        c.drawString(4.0*inch,6.75*inch,r.AdresseIP)

        c.drawString(1.0*inch,6.0*inch,"Numéro de série:")
        c.drawString(4.0*inch,6.0*inch,r.NumeroSerie)

        c.drawString(1.0*inch,5.25*inch,"Numéro de fax:")
        c.drawString(4.0*inch,5.25*inch,r.infos)

        c.setFont("Helvetica-Bold",20)
        c.drawString(1.0*inch,4.5*inch,"Support Lexmark:")
        c.drawString(4.0*inch,4.5*inch,"1-800-539-6275")

        c.setFont("Helvetica",8)
        c.drawString(5.75*inch,1.25*inch,"La direction des ressources technologiques")

        c.showPage()
        c.save()
        this_file=open(file_name, 'r')
        author=db(db.auth_user.id==auth_id).select(db.auth_user.username).first().username
        #inv_label_files
        db.inv_label_files.insert(user_id=auth_id,dates=now,description="L'affiche en pdf, géneré par le module de gestion des inventaires :"+author,files=db.inv_label_files.files.store(this_file,file_name),file_data=this_file.read(),impression=False)
        this_file.close()
        os.remove(file_name)
    if rs:
        #db((db.inv_cis.impression==False)&(db.inv_cis.TypeCi.like('Imprimante',case_sensitive=False))).update(impression=True,importation=False)
        db((db.inv_cis.impression==False)&(db.inv_cis.edit_by==auth_id)&(db.inv_cis.TypeCi.like('Imprimante',case_sensitive=False))).update(impression=True)#do not reimport ,importation=False
        session.msg="Ouvrir le fichier PDF et imprimer!"
        redirect(URL('label_files'))
        
    session.msg="Il y a rien à imprimer."
    redirect(URL('reprinting'))

    #response.flash=msg
    return dict(form="",grid="")

def reprinting_support_label():
    msg=""
    #rs=db((db.inv_cis.impression==False)&(db.inv_cis.impression_index>0)&(db.inv_cis.TypeCi.like('Imprimante',case_sensitive=False))).select()
    rs=db((db.inv_cis.impression==False)&(db.inv_cis.edit_by==auth_id)&(db.inv_cis.impression_index>=1)&(db.inv_cis.TypeCi.like('Imprimante',case_sensitive=False))).select()
    #test
    #rs=db((db.inv_cis.impression_index>=1)&(db.inv_cis.TypeCi.like('Imprimante',case_sensitive=False))).select()
    if rs:
        import uuid,os
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, inch
        file_img=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_inventaires\cemtl.jpg'        
        file_name=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_inventaires\\'+uuid.uuid4().hex+'.pdf'
        #from reportlab.lib.units import mm
        c=canvas.Canvas(file_name,pagesize=(8.5*inch,11.0*inch))
    for r in rs:
        index=r.impression_index-1
        line=index/2
        col=index%2
        xbase=0.2+4.15625*col
        ybase=0.65+2.*line
        supplier=r.Fournisseur
        phone=db(db.inv_supplier.name==supplier).select()
        if phone:
            support='Téléphone de support '+supplier+': '+phone[0].phone
        else:
            support=''
        if supplier=='Lexmark':
            rate='12%'
        else:
            rate='20%'
        #file_img2=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_inventaires\Xerox.jpg'
        file_img2=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_inventaires\\'+supplier+'.jpg'
        
        c.drawImage(file_img,(xbase-0.12)*inch,(ybase+1.)*inch, width=1.8*inch,height=.9*inch,mask=None)

        c.setFont("Helvetica-Bold",10)
        c.drawString((xbase+2.2)*inch,(ybase+1.4)*inch,'IP : '+r.AdresseIP)
        if (r.infos!=None) & (r.infos!=''):
            c.setFont("Helvetica-Bold",10)
            c.drawString((xbase+2.2)*inch,(ybase+1.2)*inch,'Fax : '+r.infos)

        c.setFont("Helvetica-Bold",10)
        name="Nom de l'imprimante : "+r.Nom
        c.drawString((xbase)*inch,(ybase+.8)*inch,name)
        
        c.setFont("Helvetica-Bold",10)
        serial=r.NumeroSerie.upper().replace(' ','')
        txt=''
        for i in range(0,len(serial), 2):
            txt+=serial[i:i+2]+' '            
        serial='Numéro de série : '+txt
        
        c.drawString((xbase)*inch,(ybase+.6)*inch,serial)

        c.setFont("Helvetica-Bold",10)
        c.drawString((xbase)*inch,(ybase+.4)*inch,support)
        c.setFont("Helvetica",7)
        c.drawString((xbase)*inch,(ybase+.22)*inch,"(Cartouches envoyées automatiquement à "+rate+' de capacité restante)')
        c.drawImage(file_img2,xbase*inch,ybase*inch, width=1.1*inch,height=0.185*inch,mask=None)

    if rs:
        c.showPage()
        c.save()
        this_file=open(file_name, 'r')
        author=db(db.auth_user.id==auth_id).select(db.auth_user.username).first().username
        #inv_label_files
        db.inv_label_files.insert(user_id=auth_id,dates=now,description="L'affiche en pdf, géneré par le module de gestion des inventaires :"+author,files=db.inv_label_files.files.store(this_file,file_name),file_data=this_file.read(),impression=False)
        this_file.close()
        os.remove(file_name)
        #for test
        db((db.inv_cis.impression==False)&(db.inv_cis.edit_by==auth_id)&(db.inv_cis.TypeCi.like('Imprimante',case_sensitive=False))).update(impression=True)#do not reimport ,importation=False
        session.msg="Ouvrir le fichier PDF et imprimer!"
        redirect(URL('label_files'))
        
    session.msg="Il y a rien à imprimer."
    redirect(URL('reprinting'))

    #response.flash=msg
    return dict(form="",grid="")

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
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

    qry=db.oct_importation_files.description.like('%gestion des inventaires%')
    orderby=db.oct_importation_files.imported|~db.oct_importation_files.dates
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False,buttons_placement = 'left')
    response.flash=session.msg
    session.msg=None
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def importation():
    response.menu+=[
        (T('Importation'), False, URL( f='importation'),[]),
        ]
    import subprocess,os  
    fs=db((db.oct_importation_files.imported==False)&(db.oct_importation_files.description.like('%gestion des inventaires%'))).select(db.oct_importation_files.ALL)
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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def log_file():
    import os
    if session.function=='reprinting_support':
        session.function=None
        redirect(URL('label_files'))
    response.menu += [
        (T("Logs"), False, URL( f='log_file'),[]),
        (T("impression d'étiquettes"), False, URL( f='inventory_impression'),[]),
        (T("Impression petites étiquettes"), False, URL( f='inventory_impression',args=['reprinting_small',]),[]),
        #(T("impression d'étiquettes ( PTouch)"), False, URL( f='inventory_impression_pt'),[]),
        ] 
    grid=""

    fields=[
            Field('local',label=T("Local pour l'impression"),requires=IS_IN_DB(db(db.inv_location.id>0),'inv_location.name'),default=session.local,comment=""),
        ]    
    buttons=[
            TD(INPUT(_type="submit",_value="Impression d'étiquettes",_id="Impression d'étiquettes",_name="Impression d'étiquettes",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="Impression petites étiquettes",_id="Impression petites étiquettes",_name="Impression petites étiquettes",_style="background-color:#0066ff")),
            #TD(INPUT(_type="submit",_value="Impression d'étiquettes (PTouch)",_id="Impression d'étiquettes (PTouch)",_name="Impression d'étiquettes (PTouch)",_style="background-color:#0066ff")),
        ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(9,elements)

    if form.accepts(request.vars,session):
        if request.vars.has_key("Impression d'étiquettes"):
            session.local=request.vars.local
            redirect(URL('inventory_impression'))
        elif request.vars.has_key("Impression petites étiquettes"):
            session.local=request.vars.local
            redirect(URL( f='inventory_impression',args=['reprinting_small',]))

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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires')|auth.has_membership(role='gestion_inventaires_reimpression'))
def label_files():    
    response.menu+=[
        (T("Entrepôt des fichiers"), False, URL( f='label_files'),[]),
        #(T("Impression d'étiquettes"), False, URL( f='inventory_impression_pdf'),[]), 
        #(T("Impression d'étiquettes (PTouch)"), False, 'file://cemtl.rtss.qc.ca/cemtl/Ressources/Public/unificace_gestion_inventaires'),
        ]

    #fields=[
    #        Field('local',label=T("Local pour l'impression"),requires=IS_IN_DB(db(db.inv_location.id>0),'inv_location.name'),default=session.local,comment="Pour imprimer les étiquettes avec Chrome or Firefox, copier ce lien \\cemtl.rtss.qc.ca\cemtl\Ressources\Public\unificace_gestion_inventaires vers le Windows explorer et cliquer sur etiquettes_boite.lbx"),
    #    ]    
    #buttons=[
    #        TD(INPUT(_type="submit",_value="Impression d'étiquettes",_id="Impression d'étiquettes",_name="Impression d'étiquettes",_style="background-color:#0066ff")),
    #         TD(INPUT(_type="submit",_value="Impression d'étiquettes (PTouch)",_id="Impression d'étiquettes (PTouch)",_name="Impression d'étiquettes (PTouch)",_style="background-color:#0066ff")),
    #    ]
    #form = SQLFORM.factory(*fields,buttons=[])
    #elements=TR(buttons)
    #form[0][-1][1].insert(9,elements)
    #if form.accepts(request.vars,session):
    #    if request.vars.has_key("Impression d'étiquettes"):
    #        session.local=request.vars.local
    #        redirect(URL('inventory_impression'))

    qry=db.inv_label_files.id>0
    orderby=~db.inv_label_files.id
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False,buttons_placement = 'left')
    response.flash=session.msg
    session.msg=None
    return dict(form="",grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires')|auth.has_membership(role='gestion_inventaires_reimpression'))
def reprinting():    
    response.menu+=[
        (T("Réimpression"), False, URL( f='reprinting'),[]),
        (T("Réimpression d'étiquettes"), False, URL( f='inventory_impression',args=['reprinting',]),[]),
        (T("Impression petites étiquettes"), False, URL( f='inventory_impression',args=['reprinting_small',]),[]),
        (T("Impression affiche support"), False, URL( f='reprinting_support',args=['reprinting_support',]),[]),
        (T("Impression étiquette support"), False, URL( f='reprinting_support_label',args=['reprinting_support_label',]),[]),
        ]

    fields=[
            Field('local',label=T("Local pour l'impression"),requires=IS_IN_DB(db(db.inv_location.id>0),'inv_location.name'),default=session.local),
        ]    
    buttons=[
            TD(INPUT(_type="submit",_value="Réimpression d'étiquettes",_id="Impression d'étiquettes",_name="Impression d'étiquettes",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="Impression petites étiquettes",_id="Impression petites étiquettes",_name="Impression petites étiquettes",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="Impression affiche support",_id="Impression affiche support",_name="Impression affiche support",_style="background-color:#0066ff")),
            TD(INPUT(_type="submit",_value="Impression étiquette support",_id="Impression étiquette support",_name="Impression étiquette support",_style="background-color:#0066ff")),
        ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(9,elements)

    if form.accepts(request.vars,session):
        if request.vars.has_key("Impression d'étiquettes"):
            session.local=request.vars.local
            redirect(URL( f='inventory_impression',args=['reprinting',]))
        elif request.vars.has_key("Impression petites étiquettes"):
            session.local=request.vars.local
            redirect(URL( f='inventory_impression',args=['reprinting_small',]))
        elif request.vars.has_key("Impression affiche support"):
            session.local=request.vars.local
            redirect(URL( f='reprinting_support',args=['reprinting_support',]))
        elif request.vars.has_key("Impression étiquette support"):
            session.local=request.vars.local
            redirect(URL( f='reprinting_support_label',args=['reprinting_support_label',]))

    qry=db.inv_cis.id>0
    orderby=~db.inv_cis.id
    #orderby=~db.inv_cis.impression
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False,buttons_placement = 'left')
    response.flash=session.msg
    session.msg=None
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def reexport():    
    response.menu+=[
        (T("Réexportation"), False, URL( f='reexport'),[]),
        (T("Préparation pour exportation"), False, URL( f='inventory_import'),[]),
        ]

    qry=db.inv_cis.id>0
    orderby=~db.inv_cis.id
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False,buttons_placement = 'left')
    return dict(form="",grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def all_items():    
    response.menu+=[
        (T("Historique"), False, URL( f='all_items'),[]),
        ]
    qry=db.inv_cis.id>0
    orderby=~db.inv_cis.id
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details,csv=False,buttons_placement = 'left')
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def tables():
    menu_url=[]
    tables={"Type de CI":"inv_type_ci","État":"inv_status","Local":"inv_location","Fournisseur":"inv_supplier","Fabriquant":"inv_manufacturer","Modèle":"inv_model","Inventaires":"inv_cis","Source de financement":"inv_funding_source","Type de garantie":"inv_warranty_type","Durée d'amortissement":"inv_depreciation_period",}

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


@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def module_access_create():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Créer un accès'), False, URL(f='module_access_create'),[]),
    ]    
    grid=""    
    qry=(db.pre_user_to_group.group_id.belongs(inventaires_groups))
    #qry=(db.auth_membership.group_id.belongs(inventaires_groups))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_inventaires'))
def module_access_edit():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
    ]    
    grid=""    
    #qry=(db.pre_user_to_group.group_id.belongs(inventaires_groups))
    qry=(db.auth_membership.group_id.belongs(inventaires_groups))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

def access_onvalidation(form):
    #form.vars.group_id
    if form.vars.group_id not in inventaires_groups:
        rs=db(db.auth_group.id.belongs(inventaires_groups)).select(db.auth_group.role)
        form.errors.group_id="Le groupe doit être dans cette liste: "+((str(rs).replace("auth_group.role","")).replace("gestion_inventaires",", gestion_inventaires"))
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
