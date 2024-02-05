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

    (T("Gestion ADs"), False, '#', [
        #(T('Liste des comptes'), False, URL(c='gestion_ads', f='index'),[]),
        (T('Liste des comptes'), False, URL( f='index'),[]),
        (T('Creation des comptes'), False, URL( f='creation_comptes'),[]),
        (T('Liste des dernières connexions'), False, URL( f='list_last_logon'),[]),

        

        ]),
    
    ]




@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads')|auth.has_membership(role='gestion_ads_list_comptes'))
#all ADs
def index():
    response.menu+=[
        (T('Liste des comptes'), False, URL( f='index'),[]), #,args=['ADS']
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
            
        script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\list_accounts.ps1'
        #good
        #psxmlgen = Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1, arg2, arg3], cwd=os.getcwd())
        #result = psxmlgen.wait()
        
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1, arg2, arg3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p1.communicate()
        output="Code Windows;Prenom et nom;Titre d'emploi***"+output
        output=output.decode('utf-8', 'ignore')
        lns=output.split("***")
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

        
        #os.getcwd() #C:\Users\admphav\unificatex\web2py
        #response.flash = str(os.getcwd())
        #response.flash = str(output) request.vars
        #response.flash = str(output)
        #response.flash = str(grid)
        response.flash = T(u'terminé')
        

    
    return dict(form=form,grid=grid,request=request,session=session)




    
#########################


@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads')|auth.has_membership(role='gestion_ads_creation_comptes'))
#all ADs
def creation_comptes():
    response.menu+=[
        (T('Creation des comptes'), False, URL( f='creation_comptes'),[]),
        ]

     
    import subprocess 
    #from subprocess import Popen
    import os

    msg=""
    #msg+=str(session.auth.user.id)+"---"+str(session.auth.user.username)

    if not request.vars.domain:
        request.vars.domain="hlhl.rtss.qc.ca"
    if not request.vars.user_model:
        request.vars.user_model="Groupes par domaine"
    user_depts=db(db.user_to_department.user_id==session.auth.user.username)._select(db.user_to_department.department_id)   
    #msg=str(db(db.user_to_department.user_id==session.auth.user.username).select(db.user_to_department.department_id))
    #auth.has_membership(role='gestion_ads_creation_comptes')
    if auth.has_membership(role='gestion_ads_creation_comptes_copier_utilisateur'):
        can_copy_account=True
    else:
        can_copy_account=False

    groups={"":""}
    group_list=[""]
    if request.vars.user_model=="Groupes par domaine":
        #read groups from database
        row_query=(db.domains.fqdn==request.vars.domain)&(db.domains.id==db.domains_security_group.domain_id)&(db.domains_security_group.protected==False)\
        &(db.domains_security_group.department_id.belongs(user_depts))
        rows=db(row_query).select(db.domains_security_group.description,db.domains_security_group.group_name,orderby=db.domains_security_group.description)
        for row in rows:
            #db.domains_security_group.description,db.domains_security_group.group_name
            g=row.description+" ------ "+row.group_name
            groups[g]=row.group_name
            group_list+=[g,]
    else: 
        #read groups from user's model groups AD
        arg1=request.vars.user_model
        arg2=""
        arg3=""
        script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\read_user_groups_bta.ps1'
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1, arg2, arg3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p1.communicate()
        output=output.decode('utf-8', 'ignore')
        rows=output.split("***")
        for row in rows:
            g=row+" >>> "+row
            groups[g]=row
            group_list+=[g,]
        
    

 

    form = SQLFORM.factory(
        Field('users',type='text',label=T('Liste des utilisateurs à créer'),length=20000,requires=IS_NOT_EMPTY(),\
        comment=T("FORMAT : Prénom nom;titre d'emploi;Groupe AD (On peut avoir plus que 500 lignes-utilisateurs. Pas de accents ni caractères spéciaux.)"),represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
        Field('domain',type='text',label=T('Domaine'),default="hlhl.rtss.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca","cemtl.gouv.qc.ca",])),
        Field('user_model',label=T('Utilisateur modèle'),default="Groupes par domaine",comment=T("Modèle pour une liste des groupes: Groupes par domaine ou Nom d\'utilisateur"),writable=can_copy_account,readable=can_copy_account),#writable=can_copy_account       
        Field('group',type='text',label=T('Groupes'),comment=T("On peut selectioner plusieurs groupes avec CTRL+Bouton gauche"),requires=IS_IN_SET(group_list,multiple=True)),
        buttons=[]#[INPUT(_type='Submit', _name='submit1', _value='Submit1'),INPUT(_type='Submit', _name='submit2', _value='Submit2')]
    )
    #element=TR(TD(INPUT(_type='submit',_value='actualiser',_id='actualiser',_name='actualiser',_style='background-color:#339FFF')))#,_style='background-color:red'
    #form[0].insert(5,element)

    element1=TD(INPUT(_type='submit',_value='actualiser',_id='actualiser',_name='actualiser',_style='background-color:#339FFF'))
    element2=TD(INPUT(_type='submit',_value='créer',_id='créer',_name='créer',_style='background-color:#ff9933'))
    element3=TD(INPUT(_type='submit',_value='supprimer',_id='supprimer',_name='supprimer',_style='background-color:#ff99cc'))
    element4=TD(INPUT(_type='submit',_value='réinitialiser',_id='réinitialiser',_name='réinitialiser',_style='background-color:#9999ff'))

    #elements=TR(element1,element2,element3,element4)
    elements=TR(element1,element2)
    form[0][-1][1].insert(5,elements)

    grid=""
    
    if form.accepts(request.vars,session,keepvalues=True):#pour eviter dernier ligne vide il viens de Powershell
        g_list=""
        try:
            for g in request.vars.group:
                g_list+=groups[g]+"_*_"
        except:
            try:
                g_list=groups[request.vars.group]+"_*_"
            except:
                pass

        if request.vars.has_key('créer'):
            msg+='créer'
        elif request.vars.has_key('supprimer'):
            msg+='supprimer'

       

        arg1=request.vars.domain+"***"+request.vars.users #adaptation to send args " " and ";" to Powershell
        #arg1=request.vars.users #adaptation to send args " " and ";" to Powershell
        arg1=arg1.replace("'"," ")
        arg1=arg1.replace(","," ")
        arg1=arg1.replace(";","_.._")
        arg1=arg1.replace('\r\n',"***")
        arg1=arg1.replace('('," ")
        arg1=arg1.replace(')'," ")
        arg1=arg1.replace(' ',"_._")
        arg2=""
        arg3=""
            
        script=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_ads\creation_comptes.ps1'
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',script,arg1, arg2, arg3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p1.communicate()
        output="Code Windows;Nom dans AD;Titre d'emploi;Statut***"+output
        output=output.decode('utf-8', 'ignore')
        lns=output.split("***")
        grid='<body class="web2py_htmltable" style="width:100%;overflow-x:auto;-ms-overflow-x:scroll"><table>'
        i=0
        for ln in lns:
            if len(ln)>2:
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
        #
        #response.flash = str(output)
        #response.flash = str(groups)
        response.flash = T(u'terminé')
        #response.flash = g_list
    #response.flash =msg
    return dict(form=form,grid=grid,request=request,session=session)

#########################
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
        #output="Dernière connexion;Prénom et nom;Code Windows;***"+output
        #output=output.decode('utf-8', 'ignore')
        output=output.replace('\r\n',"")
        #output=output.decode('utf-8', 'ignore') # why can use this convertion
        lns=output.split("***")
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
#################################
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


