# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import datetime
today=datetime.date.today()
now=datetime.datetime.now()

ads_menu=(T("Gestion ADs"), False, '#', [
        #(T('Liste des comptes'), False, URL(c='gestion_ads', f='index'),[]),
        (T('Gestion des utilisateurs'), False, URL( f='management_users',args=['users',]),[]),
        (T('Gestion des groups'), False, URL( f='management_users',args=['groups',]),[]),
        (T('Gestion des ordinateurs'), False, URL( f='management_pcs'),[]),
        (T('Liste des dernières connexions'), False, URL( f='list_last_logon'),[]),
        (T('Historique'), False, URL( f='actions_tracking'),[]),
        (T("Entrepôt des fichiers"), False, URL( f='csv_files'),[]),
        (T('Tables de configuration'), False, URL( f='tables'),[]),
        (T('Gestion des accès au module'), False, URL( f='module_access_create'),[]),
        ])

response.menu += [
    #(response.menu[0]), #Home - Page d'accueil
    ads_menu,
    ]
ads_groups=(4,9,20,19,1023,1035)
def index():
    form = ""
    grid=""
    """
    access_key={
                1:"CEMTL - ",
                2:"IUSMM - ",
                3:"HSCO - ",
                4:"PDI - ",
                5:"HMR - ",
                6:"LTEAS - ",
                7:"ICPBE - ",
                8:"SLSM - ",
                9:" - "
            }
    rs=db(db.domains_security_group.id>0).select()
    #rs=db(db.domains_security_group.description.like('%Profil utilisateur%')).select()

    for r in rs:
        #description=access_key[r.domain_id]+r.group_name
        #db(db.domains_security_group.id==r.id).update(description=description)
        if r.department_id==None:
            db(db.domains_security_group.id==r.id).update(department_id=7)
        
    
    response.flash =len(rs)
    """
    #response.flash =ord("'".decode("utf8").encode("windows-1252"))
    #response.flash = chr(39)=="'"
        
    

    #response.flash = T(u'Bievenue au module de gestion des ADs ')
    return dict(form=form,grid=grid,request=request,session=session)


#################################
def autopostback():
    script = SCRIPT("""
                    $('document').ready(function(){
                        $('#mycombo').change(function(){
                            $('#myform').submit();
                        });
                    });
                    """)
    form = SQLFORM.factory(Field("access",label="access",requires=IS_IN_DB(db(db.access_octopus.id>0),'access_octopus.id','access_octopus.title',error_message="Please pick a project from the list")))
    
    form.attributes['_id'] = 'myform'
    form.element('select').attributes['_id'] = 'mycombo'
    
    if form.accepts(request.vars, keepvalues=True):
        response.flash = 'populate with %s' % form.vars.access #populate powertable
    
    return dict(script=script,form=form)

#############################################
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads')|auth.has_membership(role='gestion_ads_list_last_logon'))
#all ADs
def list_last_logon():
    response.menu+=[
        (T('Liste des dernières connexions'), False, URL( f='list_last_logon'),[]),
        ]
    import subprocess 
    #from subprocess import Popen
    import os

    form = SQLFORM.factory(
        #Field('prenom',label=T('Prénom'),length=10,requires=IS_NOT_EMPTY()),
        #Field('nom',label=T('Nom'),length=30,requires=IS_NOT_EMPTY()),
        Field('keyword',label=T('Mot-clé'),length=30,requires=IS_NOT_EMPTY(),comment=T('Prénom ou nom ou nom au complet ou code de windows (au complet ou partiel)')),
        )
    grid=""
    if form.accepts(request.vars,session,keepvalues=True):

        #this_user=db(db.auth_user.id==auth_id).select()
        keyword=(request.vars.keyword).split(" ")
        arg1=keyword[0]
        if len(keyword)>1:
            arg2=keyword[1]
        else:
            arg2="None"
        arg3=""
            
        script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\list_last_logon.ps1'
        #good
        #psxmlgen = Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1, arg2, arg3], cwd=os.getcwd())
        #result = psxmlgen.wait()
        
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1, arg2, arg3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p1.communicate()
        #output="Dernière connexion;Prénom et nom;Code Windows;*"+output
        #output=output.decode('utf-8', 'ignore')
        output=output.replace('\r\n',"")
        #output=output.decode('utf-8', 'ignore') # why can use this convertion
        lns=output.split("*")
        lns.sort()
        lns.insert(0," Dernière connexion;Prénom et nom;Code Windows;") #add espace for sorting on frist place
        #lns.reverse()
        
        
        
        #lns.reverse()#sorting reversing or lns.sort() lns.reverse()
        
        grid='<body class="web2py_htmltable" style="width:100%;overflow-x:auto;-ms-overflow-x:scroll"><table>'
        i=0
        for ln in lns:
            if len(ln)>2: #pour eviter dernier ligne vide il viens de Powershell
                grid+="<tr>"
                if i:
                    tdb="<td>";tde="<td>"
                    cns=str(i)+";"+ln
                else:
                    tdb="<th>";tde="<th>"
                    cns="#;"+ln
                cns=cns.split(";")
                for cn in cns:
                    grid+=tdb+cn+tde
                grid+="</tr>"
            i+=1
            
        grid+="</table></body>"

        
        #response.flash = str(grid)
        response.flash = T(u'terminé')
        

    
    return dict(form=form,grid=grid,request=request,session=session)





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


#########################111
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads')|auth.has_membership(role='gestion_ads_management_users_administrators')|auth.has_membership(role='gestion_ads_management_users_csi')|auth.has_membership(role='gestion_ads_management_users_base')|auth.has_membership(role='gestion_ads_management_users_read'))
#all ADs
def management_users():
    if request.args[:1]:
        manage_type=request.args[:1][0]
    else:
        manage_type='users'   
    this_menu={
        'users':(
            'Gestion des utilisateurs',
            'Utilisateur(s)',
            (
                "Mots clés (minimum 3 caracteres) comme une partie de nom, prénom, nom d'utilisateur ou description; utilisez le mot clés abcd;abcd pour une liste complète de utilisateus",
                "Prénom;Nom;Titre d'emploi;Groupe ou Accès ou Profil;Courriel;No. d'employé;Date de fin (format: 2030-01-31)",
                "Nom d'utilisateur@domain.name;Prénom;Nom;Titre d'emploi;Groupe ou Accès ou Profil;Courriel;No. d'employé;Date de fin (format: 2030-01-31)",
            ),
            "Domain;Code Windows;Nom dans AD;Description;Information*",
            ),
        'groups':(
            'Gestion des groupes',
            'Groupe(s)',
            (
                "Nom (On peut avoir environ 200 lignes-groupes)",
                "Nom (On peut avoir environ 200 lignes-groupes)",
                "Nom (On peut avoir environ 200 lignes-groupes)",
            ),
            #"Domain;Code Windows;Nom dans AD;Groupe;CN*",
            "Domain;Code Windows;Nom dans AD;Description;Information*",
            ),
        }
    if manage_type not in this_menu.keys():
         manage_type='users'

    response.menu+=[
            (T(this_menu[manage_type][0]), False, URL( f='management_users',args=[manage_type,]),[]),
        ]

    import subprocess,os
    
    msg=""

    if auth.has_membership(role='gestion_ads_management_users_administrators'):
        admin_role=True
    else:
        admin_role=False
    
    if not request.vars.domain:
        request.vars.domain="selectionner un domaine"
    if not request.vars.group_model:
        request.vars.group_model="Sans liste des groupes"
    user_depts=db(db.user_to_department.user_id==session.auth.user.username)._select(db.user_to_department.department_id)   
    groups={}
    group_list=[]
    can_copy_account=False
    if not (type(request.vars.domain)==list): #group for one domain
        one_domain=True
        if auth.has_membership(role='gestion_ads_creation_comptes_copier_utilisateur'):
            can_copy_account=True
        else:
            can_copy_account=False
    else:
        one_domain=False
    # Pas de accents ni caractères spéciaux.
    fields=[
        Field('users',type='text',label=T(this_menu[manage_type][1]),length=30000,requires=IS_NOT_EMPTY(),\
        comment=T("On peut avoir environ 200 lignes-utilisateurs."),represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
        Field('search_format',label="",default='[RECHERCHER] '+this_menu[manage_type][2][0],writable=False),
        Field('create_format',label="",default='[CRÉER] '+this_menu[manage_type][2][1],writable=False),
        Field('edit_format',label="",default='[MODIFIER] '+this_menu[manage_type][2][2],writable=False),
        Field('domain',type='text',label=T('Domaine(s)'),comment=T("On peut selectioner plusieurs domaines avec CTRL+Bouton gauche"),default="selectionner un domaine",requires=IS_IN_SET(["selectionner un domaine","hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",],multiple=True)),#,"cemtl.gouv.qc.ca"
        #Field('group',type='text',label=T('Groupe(s)'),comment=T("On peut selectioner plusieurs groupes avec CTRL+Bouton gauche"),requires=IS_IN_SET(group_list,multiple=True),writable=one_domain,readable=one_domain),
    ]
    #Field("access",label="access",requires=IS_IN_DB(db(db.access_octopus.id>0),'access_octopus.id','access_octopus.title',error_message="Please pick a project from the list"))
    if one_domain:
        fields.insert(4,Field('group_model',type='text',label=T('Modèle'),comment=T("Modèle pour une liste des groupes"),default="Sans liste des groupes",requires=IS_IN_SET(["Sans liste des groupes","Accès informatique/applicatif (Octopus)","Profiles des utilisateurs","Utilisateur modèle",],multiple=False)))
            
        if request.vars.group_model=="Profiles des utilisateurs":
            #read groups from database
            if admin_role:
                row_query=(db.domains.fqdn==request.vars.domain)&(db.domains.id==db.domains_security_group.domain_id)
            else:
                row_query=(db.domains.fqdn==request.vars.domain)&(db.domains.id==db.domains_security_group.domain_id)&(db.domains_security_group.protected<>True)\
                &(db.domains_security_group.department_id.belongs(user_depts))
            rows=db(row_query).select(db.domains_security_group.description,db.domains_security_group.group_name,orderby=db.domains_security_group.description)
            for row in rows:
                #db.domains_security_group.description,db.domains_security_group.group_name
                g=row.description+" ------ "+row.group_name
                groups[g]=row.group_name
                group_list+=[g,]

        elif request.vars.group_model=="Accès informatique/applicatif (Octopus)":
            access_key={
                "selectionner un domaine":"selectionner un domaine",
                "cemtl.rtss.qc.ca":"CEMTL - ",
                "hlhl.rtss.qc.ca":"IUSMM - ",
                "hsco.net":"HSCO - ",
                "pdi.rtss.qc.ca":"PDI - ",
                "hmr.hmr.qc.ca":"HMR - ",
                "lteas.rtss.qc.ca":"LTEAS - ",
                "icpbe.local":"ICPBE - ",
                "csssslsm.rtss.qc.ca":"SLSM - ",
                #"cemtl.gouv.qc.ca":" - "
            }
            qry=db(db.access_octopus.title.like("%"+access_key[request.vars.domain]+"%"))
            fields.insert(3,Field("access",type='text',label=T('Accès'),comment=T("Accès pour une liste des groupes"),requires=IS_IN_DB(qry,'access_octopus.id','access_octopus.title'))) #,error_message="Please pick a project from the list"
            row_query=(db.access_octopus.id==request.vars.access)&(db.access_octopus.id==db.access_to_domains_security_group.access_id)&(db.access_to_domains_security_group.group_id==db.domains_security_group.id)
            rows=db(row_query).select(db.domains_security_group.description,db.domains_security_group.group_name,orderby=db.domains_security_group.description)
            for row in rows:
                #db.domains_security_group.description,db.domains_security_group.group_name
                g=row.description+" ------ "+row.group_name
                groups[g]=row.group_name
                group_list+=[g,]

        elif request.vars.group_model=="Utilisateur modèle":
            fields.insert(5,Field('user_model',label=T('Utilisateur modèle'),default="phvi8300",comment=T("Nom utilisateur du domaine par example: abcd8300")  ))#,writable=can_copy_account,readable=can_copy_account
            if not request.vars.user_model:
                request.vars.user_model=""
            arg1=request.vars.user_model+"@"+request.vars.domain
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_management_users_user_model.ps1'
            p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output,error = p1.communicate()
            output=output.decode('utf-8', 'ignore')
            rows=output.split("*")
            for row in rows:
                if row<>"":
                    g=row.lower()
                    groups[g]=row
                    #exeption adm
                    if admin_role:
                        group_list+=[g,]
                    else:
                        if "adm" not in g:
                            group_list+=[g,]

        else:
            pass
        #group_list filter

        if not (request.vars.group_model=="Sans liste des groupes"):
            if group_list:
                fields.insert(6,Field('group',type='text',label=T('Groupe(s)'),comment=T("CTRL+A : Selectionner tout; Pour ATTACHER ou DÉTACHER le(s) goupe(s) au(x) utilisateur(s) il faut d'abord selectionner le(s) utilisateur(s) puis le(s) groupe(s)) "),requires=IS_IN_SET(group_list,multiple=True),writable=one_domain,readable=one_domain))

    form = SQLFORM.factory(
        *fields,
        buttons=[]
    )
    can_search='hidden'
    if request.vars.users:
        if request.vars.domain<>"selectionner un domaine":
            can_search='submit'
    can_create='hidden'
    #can_attach='hidden'
    if one_domain:
        if request.vars.users:
            if request.vars.domain<>"selectionner un domaine":
                if not auth.has_membership(role='gestion_ads_management_users_read'):
                    # temporary no creation pour group
                    if manage_type=='users':
                        can_create='submit'

    buttons=[
        TD(INPUT(_type='hidden',_id='lines_count',_name='lines_count')),
        TD(INPUT(_type='submit',_value='actualiser',_id='actualiser',_name='actualiser',_style='background-color:#0066ff')),
        TD(INPUT(_type=can_search,_value='rechercher',_id='rechercher',_name='rechercher',_style='background-color:#00cccc')),
        TD(INPUT(_type=can_create,_value='créer',_id='créer',_name='créer',_style='background-color:#00cc66')),
        #TD(INPUT(_type=can_create,_value='modifier',_id='modifier',_name='modifier',_style='background-color:#00cc66')),
        TD(INPUT(_type='submit',_class='to_users',_value='supprimer',_id='supprimer',_name='supprimer',_style='background-color:#ff4d94')),
    ]

    if auth.has_membership(role='gestion_ads_management_users_administrators')|auth.has_membership(role='gestion_ads_management_users_csi'):
        buttons+=[
            #TD(INPUT(_type='submit',_class='to_users',_value='modifier',_id='modifier',_name='modifier',_style='background-color:#00cc66')),
            TD(INPUT(_type=can_create,_value='créer & réinitialiser',_id='créer & réinitialiser',_name='créer & réinitialiser',_style='background-color:#00aa66')),
            #TD(INPUT(_type=can_create,_value='création spéciale',_id='création spéciale',_name='création spéciale',_style='background-color:#00aa00')),
            TD(INPUT(_type='submit',_class='to_users',_value='infos',_id='infos',_name='infos',_style='background-color:#00cccc')),
            TD(INPUT(_type='submit',_class='to_attach',_value='attacher',_id='attacher',_name='attacher',_style='background-color:#00cccc')),
            TD(INPUT(_type='submit',_class='to_attach',_value='détacher',_id='détacher',_name='détacher',_style='background-color:#00ccff')),
            TD(INPUT(_type='submit',_class='to_users',_value='réactiver',_id='réactiver',_name='réactiver',_style='background-color:#009999')),
            TD(INPUT(_type='submit',_class='to_users',_value='désactiver',_id='désactiver',_name='désactiver',_style='background-color:#ff1ac6')),
            TD(INPUT(_type='submit',_class='to_users',_value='réinitialiser',_id='réinitialiser',_name='réinitialiser',_style='background-color:#f04d94')),
            ]

    if auth.has_membership(role='gestion_ads_management_users_administrators'):
        buttons+=[TD(INPUT(_type='submit',_class='to_users',_value='supprimer tout',_id='supprimer_tout',_name='supprimer_tout',_style='background-color:#ff0000')),]

    elements=TR(buttons)
    form[0][-1][1].insert(5,elements)
    if form.element('input',_name='réinitialiser'):
        form.element('input',_name='réinitialiser')['_onclick']="return confirm('Réinitialiser les comptes?');"
    if form.element('input',_name='supprimer'):
        form.element('input',_name='supprimer')['_onclick']="return confirm('Supprimer les comptes?');"
    if form.element('input',_name='supprimer_tout'):
        form.element('input',_name='supprimer_tout')['_onclick']="return confirm('Allez-vous supprimer les comptes DEJA UTILISES ???');"



    #autopostback():
    script = SCRIPT("""
                    $('document').ready(function(){
                        //auto search with id of recherche
                        /*
                        //disable
                        $('#to_search').change(function(){
                            $('#this_form').append('<input type="hidden" name="rechercher" value="on" />');
                            $('#this_form').submit();
                        });
                        */
                        //auto submit the form
                        $('.to_submit').change(function(){
                            $('#this_form').submit();
                        });
                        //count selected users for customize button
                        var count=0;
                        $('.to_users').hide()
                        $('.to_count').change(function(){
                            if ($(this).is(':checked'))
                                count+=1;
                            else
                                count-=1;                            
                            //alert(count);
                            if (count>0){
                                $('.to_users').show();
                            }
                            else{
                                $('.to_users').hide();
                                $('.to_attach').hide();
                            }
                        });
                        //auto search with id of recherche
                        $('.to_attach').hide();
                        //$('#to_attach').change(function(){
                        $('#to_attach').click(function(){
                            if (count>0)
                                $('.to_attach').show();
                            else
                                $('.to_attach').hide();
                        });                    
                        //select_all
                        $('#select_all').change(function(){
                            if ($('#select_all').is(':checked')){
                                $('.to_count').prop('checked', true);
                                //cout=lines_count interger
                                count=parseInt($('#lines_count').val(), 10);
                                }
                            else{
                                $('.to_count').prop('checked', false);
                                $('.to_users').hide();
                                $('.to_attach').hide();
                                count=0;
                            }
                            //alert(count);
                        });

                    });
                    
                    """)
    form.attributes['_id'] = 'this_form'
    #form.element('input',_name='users').attributes['_class'] = 'to_submit'
    #form.element('select',_name='domain').attributes['_class'] = 'to_submit'
    form.element('select',_name='domain').attributes['_id'] = 'to_search'
    if form.element('select',_name='group_model'):
        form.element('select',_name='group_model').attributes['_class'] = 'to_submit'
    if form.element('select',_name='access'):
        form.element('select',_name='access').attributes['_class'] = 'to_submit'
    if form.element('input',_name='user_model'):
        form.element('input',_name='user_model').attributes['_class'] = 'to_submit'
    if form.element('select',_name='group'):
        form.element('select',_name='group').attributes['_id'] = 'to_attach'
    #form.element('input',_name='supprimer').attributes['_class'] = 'to_users'
    
    grid=""
    
    if form.accepts(request.vars,session,keepvalues=True):#pour eviter dernier ligne vide il viens de Powershell
        
        arg1=create_arg1(request.vars.domain,request.vars.group,groups,session.auth.user.username,request.vars.selected_users,request.vars.users)        
        #msg+=arg1
        arg2=""
        arg3=""
        ps_tx=""
        output=""
        if request.vars.has_key('actualiser'):
            msg+='actualiser'
        elif request.vars.has_key('rechercher'):
            if manage_type=='users':
                ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_search.ps1'
            elif manage_type=='groups':
                ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_groups_management_search.ps1'
        elif request.vars.has_key('réactiver'):
            #msg+='réactiver'
            arg2="reactivate"
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
        elif request.vars.has_key('désactiver'):
            #msg+='désactiver'
            arg2="deactivate"
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
        elif request.vars.has_key('réinitialiser'):
            #msg+='réinitialiser'
            arg2="reset"
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
        elif request.vars.has_key('supprimer'):
            #msg+='supprimer'
            arg2="delete"
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
        elif request.vars.has_key('supprimer_tout'):
            #msg+='supprimer tout'
            arg2="delete_all"
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
            #ps_tx=""
        elif request.vars.has_key('infos'):
            arg2="infos"
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
        elif request.vars.has_key('modifier'):
            arg2="edit"
            #response.flash =  "Cette fonctionalité est encore en dévelopement!"
            response.flash =  arg1,arg2
            #ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
            ps_tx=""
        elif one_domain:
            if request.vars.has_key('créer')|request.vars.has_key('créer & réinitialiser'):
                if request.vars.has_key('créer'):
                    arg2="create"
                else:
                    arg2="createreset"
                if manage_type=='users':
                    ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_create.ps1'
                elif manage_type=='groups':
                    #need to activate can_create
                    #ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_groups_management_create.ps1'
                    pass
            elif request.vars.has_key('attacher'):
                arg2="attach"
                ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
            elif request.vars.has_key('détacher'):
                arg2="detach"
                ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_ADRDD.ps1'
            elif request.vars.has_key('création spéciale'):
                arg2="creation_special"
                ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_users_management_creation_special.ps1'


        if  ps_tx<>"":               
            p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1, arg2, arg3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output,error = p1.communicate()

        output=this_menu[manage_type][3]+output
        output=output.decode('utf-8', 'ignore')
        lns=output.split("*")
        grid='<body class="web2py_htmltable" style="width:100%;overflow-x:auto;-ms-overflow-x:scroll"><table>'
        i=0
        actions=[]
        if arg2 in ('create','createreset',):
            #create csv file
            to_csv=True
            file_name=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\octopus\user_csv.csv'
            this_file=open(file_name, 'w')
        else:
            to_csv=False
            
        for ln in lns:
            if len(ln)>2:
                #save users actions
                if (i>0)&(not(request.vars.has_key('actualiser')|request.vars.has_key('rechercher'))):
                    actions+=[{'edit_by':session.auth.user.id,'edit_time':now,'actions':ln},]
                #create output table
                grid+="<tr>"
                if i:
                    tdb="<td>";tde="</td>" #td_begin;td_end
                    cns=str(i)+";"+ln
                else:
                    tdb="<th>";tde="</th>"
                    cns="#;"+ln
                cns=cns.split(";")
                j=0
                for cn in cns:
                    if (j==0):
                        if (i==0):
                            cn='<input type="checkbox" class="to_count" id="select_all" name="selected_users" value="'+cns[2]+'">'+cn
                        else: #if (i<>0)&(j==0):
                            cn='<input type="checkbox" class="to_count" name="selected_users" value="'+cns[2]+'">'+cn
                    grid+=tdb+cn+tde
                    j+=1
                grid+="</tr>"
                #create csv file
                #to_csv=False 
                if to_csv:
                    if i:
                        #if "create] ce compte existe deja" not in ln:
                        names=cns[3].split('|')
                        #line=(names[0]+";"+names[1]+";"+cns[2]+";"+cns[4]+";"+names[3]+";"+names[4]+";"+names[5][:10]+"\r\n").decode('utf8').encode('ISO-8859-1')
                        #line=(names[0]+";"+names[1]+";;"+cns[4]+";"+names[3]+";"+names[4]+";"+names[5][:10]+"\r\n").decode('utf8').encode('ISO-8859-1')
                        #line=(names[0]+";"+names[1]+";"+cns[2]+";"+cns[4]+";"+names[3]+";"+names[4]+"\r\n").decode('utf8').encode('ISO-8859-1')#good but without date de depart
                        line=(names[0]+";"+names[1]+";"+cns[2]+";"+cns[4]+";"+names[3]+";"+names[4]+";"+names[5][:10]+"\r\n").decode('utf8').encode('ISO-8859-1')
                    else:
                        #line=("Prénom;Nom;UtilisateurWindows;Titre;NuméroEmployé;Courriel;Date de départ\r\n").decode('utf8').encode('ISO-8859-1')
                        #line=("Prénom;Nom;UtilisateurWindows;Titre;NuméroEmployé;Courriel\r\n").decode('utf8').encode('ISO-8859-1')#good but without date de depart
                        line=("Prénom;Nom;UtilisateurWindows;Titre;NuméroEmployé;Courriel;Date de départ\r\n").decode('utf8').encode('ISO-8859-1')
                    this_file.write(line)

                    

            i+=1
        #save csv file to file's depot
        if to_csv:
            this_file.close()
            this_file=open(file_name, 'r')
            author=db(db.auth_user.id==auth_id).select(db.auth_user.username).first().username
            db.oct_importation_files.insert(user_id=auth_id,team=1,types='USER',dates=now,description="Generé par module Gestion des ADs by "+author,imported=True,files=db.oct_importation_files.files.store(this_file,file_name),file_data=this_file.read())
            this_file.close()
            
        #request.vars.lines_count=str(i)
        form.element('input',_name='lines_count').attributes['_value'] = str(i-2)


            
        grid+="</table></body>"
        form.insert(9,XML(grid))
        #insert actions
        db.ads_actions_tracking.bulk_insert(actions)
        #response.flash = output
        #response.flash =  arg1
        #response.flash =  arg1,arg2
        #response.flash =names[5][:10]
    
        #response.flash =  str(actions)
        #response.flash =  msg
    #response.flash =  request.vars
    
    #response.flash ="test11"
    #response.flash =  request.vars.group

    
    return dict(script=script,form=form,grid=grid,request=request,session=session)    
###########end management_users##############

def create_arg1(this_domains,this_groups,groups,this_ou,selected_users,this_users):# request.vars.domain,request.vars.group,session.auth.user.username,(request.vars.users).split(';')
    d_list=""
    if type(this_domains)==list:
        for g in this_domains:
            d_list+=g+";"
    else:
        d_list+=this_domains
        
    g_list=""
    try:
        if not (type(this_domains)==list):
            if type(this_groups)==list:
                for g in this_groups:
                    g_list+=groups[g]+";"
            elif (this_groups==None)|(this_groups==""):
                g_list+=";"
            else:
                g_list+=groups[this_groups]+";"
    except:
        pass
    #g_list=str(this_groups)
    g_list=g_list.replace('\r\n',"")

    u_list=""
    if selected_users:
        if type(selected_users)==list:
            for g in selected_users:
                u_list+=g+";"
        else:
            u_list+=selected_users


    #arg1= d_list+"*"+g_list+"*"+session.auth.user.username+"*"+u_list+"*"+this_users
    arg1= d_list.decode("utf8")+"*"+g_list.decode("utf8")+"*"+session.auth.user.username+"*"+u_list.decode("utf8")+"*"+this_users.decode("utf8") 
    #arg1=arg1.lower()

    """
    arg1=arg1.replace("'"," ")
    arg1=arg1.replace(","," ")
    arg1=arg1.replace(";","_.._")
    arg1=arg1.replace('\r\n',"*")
    arg1=arg1.replace('('," ")
    arg1=arg1.replace(')'," ")
    arg1=arg1.replace(' ',"_._")
    """
    arg1=escape(arg1)
    arg1=arg1.replace('\r\n',"*")

    return arg1

def escape(arg1):
    arg1=arg1.lower()
    #arg1=arg1.decode("utf8")
    arg1=arg1.encode("windows-1252")
    arg1=arg1.replace("à","a")
    arg1=arg1.replace("â","a")
    arg1=arg1.replace("ä","a")
    arg1=arg1.replace("ç","c")
    arg1=arg1.replace("é","e")
    arg1=arg1.replace("è","e")
    arg1=arg1.replace("ê","e")
    arg1=arg1.replace("ë","e")
    arg1=arg1.replace("ï","i")
    arg1=arg1.replace("î","i")
    arg1=arg1.replace("ô","o")
    arg1=arg1.replace("ù","u")
    arg1=arg1.replace("û","u")
    arg1=arg1.replace("ü","u")
    arg1=arg1.replace(".","0_")
    arg1=arg1.replace(",","1_")
    arg1=arg1.replace(";","2_")
    arg1=arg1.replace('(',"3_")
    arg1=arg1.replace(')',"4_")
    arg1=arg1.replace(' ',"5_")
    arg1=arg1.replace('{',"6_")
    arg1=arg1.replace('}',"7_")
    arg1=arg1.replace("'","8_")
    arg1=arg1.replace(":","9_")
    arg1=arg1.replace("#","0-_")
    arg1=arg1.replace("@","1-_")


    return arg1

def descape(arg1):
    arg1=arg1.replace("0_",".")
    arg1=arg1.replace("1_",",")
    arg1=arg1.replace("2_",";")
    arg1=arg1.replace("3_",'(')
    arg1=arg1.replace("4_",')')
    arg1=arg1.replace("5_",' ')
    arg1=arg1.replace("6_",'{')
    arg1=arg1.replace("7_",'}')
    arg1=arg1.replace("8_","'")
    arg1=arg1.replace("9_",":")
    arg1=arg1.replace("0-_","#")
    arg1=arg1.replace("1-_","@")
    return arg1

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads')|auth.has_membership(role='gestion_ads_management_users_administrators')|auth.has_membership(role='gestion_ads_management_users_csi')|auth.has_membership(role='gestion_ads_management_users_base'))
#all ADs
def actions_tracking():
    response.menu+=[
        (T('Historique'), False, URL( f='actions_tracking'),[]),
        ]
    qry=(db.ads_actions_tracking.edit_by==session.auth.user.id)
    fields=[db.ads_actions_tracking.edit_time,db.ads_actions_tracking.actions]
    grid = SQLFORM.grid(qry,fields=fields,orderby=~db.ads_actions_tracking.id,maxtextlength=250,deletable=False,editable=False,create=False)
    #deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)

    #grid = SQLFORM.grid(db[table],args=request.args[:1],user_signature=False)
    #response.flash = T(u'terminé')
    return dict(grid=grid)

@auth.requires_login()
def management_pcs():
    management_pcs=[
            (T('Copier des groupesde securité'), False, URL( f='management_pcs_copy_groups'),[]),
            (T("Historique"), False, URL( f='actions_tracking'),[]),
        ]       
    response.menu += [
        (T("Gestion des ordinateurs"), False, '#',management_pcs),
        (T("Guide d'utilisation du module"), False, URL( f='management_pcs'),[]),
        ]

    return dict(form="",grid="")

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads_pcs'))
def management_pcs_copy_groups():
    response.menu+=[
        (T('Gestion des ordinateurs'), False, URL( f='management_pcs'),[]),
        ]
    management_pcs=[
            (T('Copier des groupesde securité'), False, URL( f='management_pcs_copy_groups'),[]),
            (T("Historique"), False, URL( f='actions_tracking'),[]),
        ]       
    response.menu += [
        (T("Gestion des ordinateurs"), False, '#',management_pcs),
        (T('Copier des groupesde securité'), False, URL( f='management_pcs_copy_groups'),[]),
        ]

    grid=""
    fields=[
        Field('account_source',label=T('Ordinateur source'),default="",requires=[IS_NOT_EMPTY(),IS_UPPER()]),
        Field('account_destination',label=T('Ordinateur destination'),default="",requires=[IS_NOT_EMPTY(),IS_UPPER()]),
        Field('domain',type='text',label=T('Domaine'),comment=T("Selectioner le domaine de ce compte"),default="pdi.rtss.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",],multiple=False)),
    ]
    buttons=[
        TD(INPUT(_type='submit',_value='copier ses groupes',_id='copier ses groupes',_name='copier ses groupes',_style='background-color:#0066ff')),
    ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(5,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        import subprocess
        arg1=request.vars.account_source+"*"+request.vars.account_destination+"*"+request.vars.domain
        ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\ads_management_pcs_copy_groups.ps1'
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p1.communicate()
        output=output.decode('utf-8', 'ignore')        
        db.ads_actions_tracking.insert(edit_by=auth_id,edit_time=now,actions=output)
        qry=(db.ads_actions_tracking.edit_by==session.auth.user.id)
        fields=[db.ads_actions_tracking.edit_time,db.ads_actions_tracking.actions]
        grid = SQLFORM.grid(qry,fields=fields,orderby=~db.ads_actions_tracking.id,maxtextlength=250,deletable=False,editable=False,create=False,details=False)
        
        #response.flash =arg1

    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads'))
def tables():
    menu_url=[]
    #tables=["department","user_to_department","domains","domains_security_group","access_octopus","access_to_domains_security_group","ads_actions_tracking"]
    tables={"Historique":"ads_actions_tracking","Département":"department","Utilisateur par département":"user_to_department","Domaines":"domains","Groupe de securité par domaine ":"domains_security_group","Accès applicatif dans Octopus":"access_octopus","Groupe de securité par accès":"access_to_domains_security_group","Historique":"ads_actions_tracking"}

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

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads'))
def module_access_create():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Créer un accès'), False, URL(f='module_access_create'),[]),
    ]    
    grid=""    
    qry=(db.pre_user_to_group.group_id.belongs(ads_groups))
    #qry=(db.auth_membership.group_id.belongs(ads_groups))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads'))
def module_access_edit():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
    ]    
    grid=""    
    #qry=(db.pre_user_to_group.group_id.belongs(ads_groups))
    qry=(db.auth_membership.group_id.belongs(ads_groups))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

def access_onvalidation(form):
    #form.vars.group_id
    if form.vars.group_id not in ads_groups:
        rs=db(db.auth_group.id.belongs(ads_groups)).select(db.auth_group.role)
        form.errors.group_id="Le groupe doit être dans cette liste: "+((str(rs).replace("auth_group.role","")).replace("gestion_ads",", gestion_ads"))
        form.errors= True
    return

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads')|auth.has_membership(role='gestion_ads_management_users_administrators')|auth.has_membership(role='gestion_ads_management_users_csi'))
def csv_files():    
    response.menu+=[
        (T("Entrepôt des fichiers"), False, URL( f='csv_files'),[]),
        ]
    qry=db.oct_importation_files.id>0
    orderby=db.oct_importation_files.imported|~db.oct_importation_files.dates
    grid = SQLFORM.grid(qry,orderby=orderby,maxtextlength=70,deletable=False,editable=False,create=False,user_signature=True,searchable=True,details=True,csv=False)
    return dict(grid=grid)




