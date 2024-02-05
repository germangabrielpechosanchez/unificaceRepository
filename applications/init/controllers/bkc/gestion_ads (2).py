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
        (T('Liste des comptes'), False, URL(c='gestion_ads', f='index',args=['ADS']),[]),
        (T('Creation des comptes'), False, URL(c='gestion_ads', f='creation_comptes',args=['ADS']),[]),
        (T('Liste des dernières connexions'), False, URL(c='gestion_ads', f='list_last_logon',args=['ADS']),[]),

        

        ]),
    
    ]




@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads'))
#all ADs
def index():
    response.menu+=[
        (T('Liste des comptes'), False, URL(c='gestion_ads', f='index',args=['ADS']),[]),
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
        

    
    return dict(form=form,grid=grid,request=request,session=session)
#########################
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads'))
#all ADs
def creation_comptes():
    response.menu+=[
        (T('Creation des comptes'), False, URL(c='gestion_ads', f='creation_comptes',args=['ADS']),[]),
        ]

     
    import subprocess 
    #from subprocess import Popen
    import os

    form = SQLFORM.factory(
        #Field('users','textarea',label=T('List des tilisateurs'),length=1000,if len(ln)>2:requires=IS_NOT_EMPTY(),comment=T("FORMAT : Prénom1 nom1;titre d'emploi1***Prénom2 nom2;titre d'emploi2")),
        Field('users',type='text',label=T('Liste des utilisateurs à créer'),length=20000, notnull=True,comment=T("FORMAT : Prénom nom;titre d'emploi (On peut avoir plus que 100 lignes )"),represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
        Field('Domain',type='text',label=T('Domaine'),default="hlhl.rtss.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca","cemtl.gouv.qc.ca",])),
        

        #Field('text1', type='text', length=1000, notnull=True,represent=lambda text, row: XML(text.replace('\n', '<br />'),sanitize=True, permitted_tags=['br/'])),
        )

    grid=""

    if form.accepts(request.vars,session,keepvalues=True):#pour eviter dernier ligne vide il viens de Powershell
        
        arg1=request.vars.users #adaptation to send args " " and ";" to Powershell
        arg1=arg1.replace("'"," ")
        arg1=arg1.replace(","," ")
        arg1=arg1.replace(";","_.._")
        arg1=arg1.replace('\r\n',"***")
        arg1=arg1.replace(' ',"_._")
        #arg1=arg1.replace('\n',"")
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
        #
        #response.flash = str(output)
        #response.flash = str(ord(request.vars.users[1]))
        #response.flash = str(len(ln))
    return dict(form=form,grid=grid,request=request,session=session)

#########################
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_ads'))
#all ADs
def list_last_logon():
    response.menu+=[
        (T('Liste des dernières connexions'), False, URL(c='gestion_ads', f='list_last_logon',args=['ADS']),[]),
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
        lns.insert(0,"Dernière connexion;Prénom et nom;Code Windows;")
        
        
        
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


