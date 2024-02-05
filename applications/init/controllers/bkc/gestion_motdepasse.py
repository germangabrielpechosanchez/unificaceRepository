# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


# myutils.py from module folder
#from myutils import crypt as MYCRYPT
#db.employees.unificace.filter_in = lambda data: CRYPT('encrypt', data, iv_random=False)
#db.employees.unificace.filter_out = lambda data: CRYPT('decrypt', data, iv_random=False)



import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()


response.menu = [
    (response.menu[0]), #Home - Page d'accueil

    (T("Libre-service - Réinitialiser mon mot de passe"), False, '#', [
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]),
        (T('Historique'), False, URL( f='actions_tracking'),[]), 
        #(T('Tables de configuration'), False, URL( f='tables'),[]),
        (T('Gestion des accès au module'), False, URL( f='module_access_create'),[]),
        (T('Gestion des utilisateurs'), False, URL( f='users_data'),[]),
        ]),
    
    ]

motdepasse_groups=(1037,1038,1039)


if auth.is_logged_in():
    if (auth.has_membership(role='admin')): #auth.has_membership(role='gestion_motdepasse_edit_add')
        create=True
        deletable=True
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_motdepasse')): #auth.has_membership(role='gestion_motdepasse_edit_add')
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_motdepasse_edit_add')):
        create=True
        deletable=False
        editable=True
        user_signature=False
        searchable=True
        details=True
    elif (auth.has_membership(role='gestion_motdepasse_edit')):
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

#@auth.requires_login()
def index():
    """
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    """
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]

    grid=""

    #db(db.employees.id>0).delete()
    #elimine 2016 doublon w/o email
    """
    i=0
    for r in rs:
        #fs=db((db.employees.email=="")&((db.employees.full_name==r.full_name)|((db.employees.first_name==r.first_name)&(db.employees.last_name==r.last_name)))).select()
        fs=db((db.employees.email=="")&((db.employees.full_name.like(r.full_name))|((db.employees.first_name.like(r.first_name))&(db.employees.last_name.like(r.last_name))))).select()
        for f in fs:
            db(db.employees.id==r.id).update(logon=r.logon+';'+f.logon)
            db(db.employees.id==f.id).delete()
            i+=1
    
    #elimine 4127 doublons w email
    rs=db(db.employees.email<>"").select()

    i=0
    for r in rs:
        #fs=db((db.employees.email=="")&((db.employees.full_name==r.full_name)|((db.employees.first_name==r.first_name)&(db.employees.last_name==r.last_name)))).select()
        fs=db((db.employees.id<>r.id)&((db.employees.full_name.like(r.full_name))|((db.employees.first_name.like(r.first_name))&(db.employees.last_name.like(r.last_name)))).select()
        for f in fs:
            if r.email<>f.email:
                db(db.employees.id==r.id).update(email=r.email+';'+f.email,logon=r.logon+';'+f.logon)
            else:
                if f.employee_number<>"":employee_number=';'+f.employee_number
                else:employee_number=''
                if f.job_title<>"":job_title=';'+f.job_title
                else:job_title=''
                if f.phone_extesion<>"":phone_extesion=';'+f.phone_extesion
                else:phone_extesion=''
                if f.mobile_phone<>"":mobile_phone=';'+f.mobile_phone
                else:mobile_phone=''
                if f.office<>"":office=';'+f.office
                else:office=''
                db(db.employees.id==r.id).update(logon=r.logon+';'+f.logon,employee_number=r.employee_number+employee_number,job_title=r.job_title+job_title,phone_extesion=r.phone_extesion+phone_extesion,mobile_phone=r.mobile_phone+mobile_phone,office=r.office+office)
                i+=1
            db(db.employees.id==f.id).delete()
    
    i=0
    for r in rs:
        fs=db((db.employees.email=="")&((db.employees.full_name==r.full_name)|((db.employees.first_name==r.first_name)&(db.employees.last_name==r.last_name)))).select()
        #fs=db((db.employees.email=="")&((db.employees.full_name.like(r.full_name))|((db.employees.first_name.like(r.first_name))&(db.employees.last_name.like(r.last_name))))).select()
        for f in fs:
            if f.employee_number<>"":employee_number=';'+f.employee_number
            else:employee_number=''
            if f.job_title<>"":job_title=';'+f.job_title
            else:job_title=''
            if f.phone_extesion<>"":phone_extesion=';'+f.phone_extesion
            else:phone_extesion=''
            if f.mobile_phone<>"":mobile_phone=';'+f.mobile_phone
            else:mobile_phone=''
            if f.office<>"":office=';'+f.office
            else:office=''
            db(db.employees.id==r.id).update(logon=r.logon+';'+f.logon,employee_number=r.employee_number+employee_number,job_title=r.job_title+job_title,phone_extesion=r.phone_extesion+phone_extesion,mobile_phone=r.mobile_phone+mobile_phone,office=r.office+office)
            db(db.employees.id==f.id).delete()
            i+=1
    """

    #rs=db(db.employees.id>0).select()
    #rs=db(db.employees.email<>"").select()
    #rs=db((db.employees.email_checked==True)).select() #&(db.employees.email_checked==True)
    #my=rs[0].unificace.strip()
    #mi=rs[0].email.strip()
    #if  mi==my:
    #    msg="True" 
    #else:
    #    msg="NO"
         
    #response.flash=msg
#    if session.count:session.count+=1
#    else: session.count=1
#    response.flash=session.count


    
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin'))
def working():
    response.menu+=[
        (T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    grid=""
    ########encrypt
    #rs=db(db.employees.email<>"").select(db.employees.id,db.employees.email)
    #for r in rs:
    #    email=CRYPT('encrypt',r.email, iv_random=False)
    #    db(db.employees.id==r.id).update(email=email)

    ########decrypt
    #rs=db(db.employees.email<>"").select(db.employees.id,db.employees.email)
    #for r in rs:
    #    email=CRYPT('decrypt',r.email, iv_random=False)
    #    db(db.employees.id==r.id).update(email=email)
        
    #update unificace
    #rs=db(db.employees.id>0).select(db.employees.id,db.employees.email)
    #for r in rs:
    #    db(db.employees.id==r.id).update(unificace=str(r.id)+r.email)

    #rs=db(db.employees.id>0).select(db.employees.id,db.employees.email)
    #for r in rs:
    #    unificace=CRYPT('encrypt',str(r.id)+r.email, iv_random=False)
    #    db(db.employees.id==r.id).update(unificace=unificace)

    #with CRYPT dans DB
    #rs=db(db.employees.id>0).select(db.employees.id,db.employees.email)
    #for r in rs:
        #db(db.employees.first_name=="VILOUNHA").update(unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')('123456')[0]))#good
    #    unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(str(r.id)+r.email)[0])
    #    db(db.employees.id==r.id).update(unificace=unificace)
    
    #db(db.employees.first_name=="VILOUNHA").update(unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')('149569;vphanalasy@ssss.gouv.qc.ca')[0]))
    #response.flash=db.employees.unificace.validate("149569;vphanalasy@ssss.gouv.qc.ca") == (db(db.employees.first_name=="VILOUNHA").select().first().unificace, None)
    #response.flash=str(CRYPT(key='sha512:thisisthekey')('123456')[0])

    #response.flash=db.employees.unificace.validate("149569;vphanalasy@ssss.gouv.qc.ca") == (db(db.employees.id==149569).select().first().unificace, None)
    
    #db((db.employees.email<>"")&(db.employees.is_active==True)).update(email_checked=True)

    #with CRYPT dans DB
    #rs=db(db.employees.id>0).select(db.employees.id,db.employees.email)
    #for r in rs:
    #    unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(str(r.id)+r.email)[0])
    #    db(db.employees.id==r.id).update(unificace=unificace)

    #with CRYPT dans DB
    #rs=db(db.employees.id>0).select()#rs.full_name+rs.first_name+rs.last_name
    #for r in rs:
    #    unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(r.full_name+r.first_name+r.last_name+r.logon+r.email)[0])
    #    db(db.employees.id==r.id).update(unificace=unificace)




    
    return dict(grid=grid)

@auth.requires_login() #this is in production
#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse'))
# old version need to change encription
def inscription_old():
    msg=""
    response.menu+=[
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    username=db(db.auth_user.id==auth_id).select()[0].username
    fields=[
        Field('account',label=T('Compte Windows'),default=username,writable=False),
        Field('domain',type='text',label=T('Domaine'),comment=T("Selectioner le bon domaine de ce compte"),default="hmr.hmr.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",],multiple=False)),
        Field('email',label=T('Courriel'),default='@ssss.gouv.qc.ca',requires = IS_EMAIL(error_message='Doit etre un courriel valide!'),comment=T("Ce courriel sera utiliser pour envoyer le mot de passe")),
    ]
    if session.confirmation_code:
        fields.insert(3,Field('confirmation_code',label=T('Code de confirmation'),comment=T("Entrer le code de confirmation que vous avez recu par ce courreil"),default=""))
        bt='Inscrire au Libre-service'
    else:
        bt='Continuer'    
    buttons=[
        TD(INPUT(_type='submit',_value=bt,_id=bt,_name=bt,_style='background-color:#0066ff')),
    ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(5,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        #generate code
        if not session.confirmation_code:
            import random
            session.confirmation_code=random.randint(10001,99999)
        #send email
        if (not session.last_email_sent)|(session.last_email_sent<>request.vars.email):
            from gluon.tools import Mail
            mail = Mail()
            mail.settings.server = 'smtp.rtss.qc.ca:25'
            mail.settings.sender = 'unificace@ssss.gouv.qc.ca'
            status=mail_send(
                to=[request.vars.email,],
                subject='Code de confirmation du "Libre-service -Inscription"',
                reply_to='unificace@ssss.gouv.qc.ca',
                #message='Utiliser ce code de confirmation de quatres chiffres pour finaliser votre inscription de inscrire votre compte au Libre-service - Code de confirmation: '+str(session.confirmation_code)
                message=str(session.confirmation_code)
                )
            if status:
                msg+="Le code de confirmation a été envoyé. SVP consultez votre courriel (Sujet: Libre-service -Inscription) et continuez sur cette page pour finaliser votre inscription!"
                session.last_email_sent=request.vars.email
        elif str(session.confirmation_code)==request.vars.confirmation_code:
            rs=db(db.employees.email.like('%'+request.vars.email+'%')).select()
            if rs: #need check security logic
                #if len(rs)==1: #verify name with ad email checked and add logon
                this_logon=(';'+username+"@"+request.vars.domain).lower()                    
                logon=rs[0].logon.lower().replace(this_logon,'')#cleaning
                logon=logon+this_logon
                ##############################
                if len(rs)==1:
                    #db(db.employees.email.like('%'+request.vars.email+'%')).update(logon=logon,is_active=True,unificace=str(rs[0].id)+rs[0].email,email_checked=True)
                    unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(str(rs[0].id)+rs[0].email)[0])
                    #db(db.employees.id==rs[0].id).update(logon=logon,is_active=True,unificace=str(rs[0].id)+rs[0].email,email_checked=True)
                    db(db.employees.id==rs[0].id).update(logon=logon,is_active=True,unificace=unificace,email_checked=True)

                else:
                    maxlen=0
                    for r in rs:
                        #check len of record
                        thislen=r.job_title+r.phone_extesion+r.mobile_phone+r.office
                        if thislen>maxlen:
                            maxlen=thislen
                            rest_id=r.id
                        for r in rs:
                            if r.id==rest_id:
                                unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(str(r.id)+r.email)[0])
                                db(db.employees.id==r.id).update(logon=logon,is_active=True,unificace=unificace,email_checked=True)
                            else:
                                db(db.employees.id==r.id).delete()
                #clean 
                msg+="Terminé avec succès. Maintenant vous pouvez utiliser votre courriel pour réinitialiser vos mots de passe"
            else:
                import subprocess
                arg1="*checkname*"+username+"*"+request.vars.domain+"*"
            
                ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_motdepasse\gestion_motdepasse.ps1'
                p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output,error = p1.communicate()
                output=output.decode('utf-8', 'ignore')
                #";$this_user;$this_password;$status;$this_user_GivenName4;$this_user_Surname5;$this_user_Name6;"
                output=output.split(';')
                if output[3]=='checked':
                    rs=db(db.employees.full_name.like('%'+output[6]+'%')|(db.employees.first_name.like('%'+output[4]+'%')&db.employees.last_name.like('%'+output[5]+'%'))).select()
                    if rs:
                        new_logon=';'+output[1].lower()
                        logon=rs[0].logon.lower().replace(new_logon,'')
                        logon=logon+new_logon
                        new_email=';'+request.vars.email.lower()
                        email=rs[0].email.lower().replace(new_email,'')
                        email=email+new_email
                        #########################
                        #db(db.employees.id==rs[0].id).update(full_name=output[6].upper(),first_name=output[4].upper(),last_name=output[5].upper(),logon=logon,email=email,unificace=str(rs[0].id)+email,is_active=True,email_checked=True)
                        unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(str(rs[0].id)+email)[0])
                        db(db.employees.id==rs[0].id).update(logon=logon,email=email,unificace=unificace,is_active=True,email_checked=True)
                    else:
                        #########################
                        this_id=db.employees.insert(full_name=output[6].upper(),first_name=output[4].upper(),last_name=output[5].upper(),logon=output[1].lower(),email=request.vars.email,is_active=True,email_checked=True)
                        unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(str(this_id)+request.vars.email)[0])
                        #must use this new one
                        #unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(form.vars.full_name+form.vars.first_name+form.vars.last_name+form.vars.logon+form.vars.email)[0])

                        db(db.employees.id==this_id).update(unificace=unificace)
                    msg+="Terminé avec succès. Maintenant vous pouvez utiliser votre courriel pour réinitialiser vos mots de passe"
                else:
                    msg+="Veuillez revérifier le domaine"

        else:
            msg+="Le code de confirmation a deja envoyé. SVP consultez votre courriel et continuez sur cette page et entrer le code de confirmation pour finaliser votre inscription"
    response.flash =  msg
    return dict(form=form,grid="")

#############################################
@auth.requires_login() #this is in production
#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse'))
def inscription():
    msg=""
    """
    response.menu+=[
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    """
    response.menu=[
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        #(T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    username=db(db.auth_user.id==auth_id).select()[0].username
    fields=[
        Field('account',label=T("Compte Windows."),comment=" Ce compte sera encore demander dans la prochaine etape de confirmation.",default=username,writable=False),
        Field('domain',type='text',label=T('Domaine'),comment=T("Selectioner le bon domaine de ce compte"),default="hmr.hmr.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",],multiple=False)),
        Field('email',label=T('Courriel'),default='@ssss.gouv.qc.ca',requires = IS_EMAIL(error_message='Doit etre un courriel valide!'),comment=T("Ce courriel sera utilisé pour envoyer le lien pour confirmation et aussi pour changer votre mot de passe. Si les 3 informations sont valides, la page sera redirigée directement vers votre page de courriel. Le délai de réception peut prendre quelques minutes.")),
    ]
    bt='Inscrire au Libre-service'
    buttons=[
        TD(INPUT(_type='submit',_value=bt,_id=bt,_name=bt,_style='background-color:#0066ff')),
    ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(5,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        arg1="*hasacount*"+username+"*"+request.vars.domain+"*"
        import subprocess
        arg1=arg1.replace(' ','5_')
        ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_motdepasse\gestion_motdepasse.ps1'
        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,error = p1.communicate()
        output=output.decode('utf-8', 'ignore')
        client_email=request.vars.email
        actions=output
        output=output.split(';')
        status=False
        if output[3]=='toreset':
            import uuid
            reset_id=uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex
            from gluon.tools import Mail
            mail = Mail()
            mail.settings.server = 'smtp.rtss.qc.ca:25'
            mail.settings.sender = 'unificace@ssss.gouv.qc.ca'
            status=mail_send(
                to=[request.vars.email,],
                subject='Confirmation du "Libre-service -Inscription"',
                reply_to='unificace@ssss.gouv.qc.ca',
                message="Pour finaliser votre inscription, cliquez sur ce lien: https://"+request.env.http_host+"/init/gestion_motdepasse/inscription_receive/"+reset_id
                )
            if status:
                #";$this_user_name;$this_password;$status;$this_user_GivenName;$this_user_Surname;$this_user_FullName;"
                ip_source=""
                if request.env.remote_addr:ip_source+="|"+request.env.remote_addr
                if request.env.http_x_forwarded_for:ip_source+="|"+request.env.http_x_forwarded_for
                if request.vars.client:ip_source+="|"+request.vars.client
                actions=actions.replace('toreset','inscription')
                db.ads_actions_tracking.insert(edit_by=1072,edit_time=now,actions=client_email+ip_source+actions+reset_id)#by unificace
                url_email=client_email.split('@')[1]
                if url_email=="ssss.gouv.qc.ca":url_email="https://outlook.office.com/owa/"
                else:url_email="https://"+url_email
                #redirect('http://www.web2py.com')
                #redirect(URL('index', args=(1, 2, 3), vars=dict(a='b')))
                #prepaire session count for confirmation
                session.count=0
                redirect(url_email)
                #msg+="Le lien pour confirmation a été envoyé. SVP consultez votre courriel (Sujet: Libre-service -Inscription)!"
        else:
            msg+="Vos données ne sont pas valides, vous pouvez encore réessayer ou contacter le CSI"
    response.flash =  msg
    return dict(form=form,grid="")
##########################################
def inscription_receive():
    response.menu=[
        #(T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        #(T('Inscrire au Libre-service'), False, URL( f='inscription'),[])
        (T("Libre-service"), False, URL( f=''),[]),
        #(T("Copiez votre mot de passe temporaire et le changer sur le Portail Citrix"), False, 'http://storefront.cemtl.rtss.qc.ca/Citrix/CEMTLWeb/'), 
        ]
    msg=""
    form=XML("<b>Votre lien actuel est expiré.</b><br/><br/><i><a href='https://"+request.env.http_host+"/init/gestion_motdepasse/inscription'>Vous pouvez encore commencer à inscrire au Libre-service en cliquant ici</a></i>")
    grid=""
    this_args=request.args(0) or "noargs"
    if session.count:session.count+=1
    else: session.count=1
    # 5x max
    if (this_args<>"noargs")&(session.count<=5):
        r=db((db.ads_actions_tracking.actions.like('%'+this_args+'%'))).select().first()
        if r:
            #60*60*24*2. 2 jours
            if (now-r.edit_time).total_seconds()<172800.0:
                form = SQLFORM.factory(
                    Field("username",label=T("Votre nom d'utilisateur"),length=15,requires=IS_NOT_EMPTY(),comment=T("Nom d'utilisateur de Windows")),
                    buttons=[]
                )
                buttons=[
                    TD(INPUT(_type='submit',_value='Confirmer mon inscription',_id='Confirmer mon inscription',_name='Confirmer mon inscription',_style='background-color:#0066ff')),
                ]
                elements=TR(buttons)
                form[0][-1][1].insert(5,elements)
                if form.process().accepted:
                    r_actions=r.actions
                    username_full=r_actions.split(";")[1].lower()
                    username_simple=username_full.split("@")[0]
                    this_username=request.vars.username.lower()
                    #assured for only inscrtiption not for toreset
                    this_operation=r_actions.split(";")[3]
                    if ((this_username==username_full)|(this_username==username_simple))&(this_operation=='inscription'):
                        #vphanalasy@ssss.gouv.qc.ca|10.49.26.246;aphvi8300@cemtl.rtss.qc.ca;;checked;VILOUNHA;PHANALASY;VILOUNHA PHANALASY 8300;43e30e9
                        output=r_actions.split(';')
                        rs=db((db.employees.first_name.like('%'+output[4]+'%')&db.employees.last_name.like('%'+output[5]+'%'))).select().first()
                        #save email
                        if rs:
                            new_logon=output[1].lower()
                            rs_logon=rs.logon.lower()
                            logon=rs_logon.replace(';'+new_logon,'')
                            logon=logon.replace(new_logon,'')
                            logon=logon+';'+new_logon
                            new_email=output[0].split('|')[0].lower()
                            rs_email=rs.email.lower()
                            email=rs_email.replace(';'+new_email,'')
                            email=rs_email.replace(new_email,'')
                            email=email+';'+new_email
                            unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(rs.full_name+rs.first_name+rs.last_name+logon+email)[0])
                            db(db.employees.id==rs.id).update(logon=logon,email=email,unificace=unificace,is_active=True,email_checked=True)
                        else:
                            logon=output[1].lower()
                            email=output[0].split('|')[0].lower()
                            rs_full_name=(output[4]+" "+output[5]).upper()
                            rs_first_name=output[4].upper()
                            rs_last_name=output[5].upper()
                            unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(rs_full_name+rs_first_name+rs_last_name+logon+email)[0])
                            db.employees.insert(full_name=rs_full_name,first_name=rs_first_name,last_name=rs_last_name,logon=logon,email=email,unificace=unificace,is_active=True,email_checked=True)
                        #save action
                        r_actions=r_actions.replace(this_args,'')
                        r_actions=r_actions+' inscription_received at '+str(now)
                        db(db.ads_actions_tracking.id==r.id).update(edit_time=now,actions=r_actions)
                        form=XML("<b>Votre courriel a été enregistré avec succès</b>")
                    else:
                        msg+="Veuillez réessayer avec bon nom d'utilisateur ou contacter le CSI!"
    elif (this_args<>"noargs")&(session.count>5):
        r=db((db.ads_actions_tracking.actions.like('%'+this_args+'%'))).select().first()
        if r:
            r_actions=r.actions
            r_actions=r_actions.replace(this_args,'')
            r_actions=r_actions+' inscription_5_counts_more at '+str(now)
            db(db.ads_actions_tracking.id==r.id).update(edit_time=now,actions=r_actions)
        

    response.flash =msg    
    return dict(form=form,grid=grid)

##########################################

#@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse')) #in production must be disable
def password_reset():
    """
    response.menu+=[
        (T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    """
    response.menu=[
        #(T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        #(T('Inscrire au Libre-service'), False, URL( f='inscription'),[]),
        (T("Réinitialiser mon mot de passe"), False, URL( f='password_reset'),[]), 
        ]
    grid=""
    msg=""
    fields=[
            Field('account',label=T('Compte Windows'),default="",requires=IS_NOT_EMPTY(),writable=True,comment=T("Mettre votre nom d'utilisateur (par exemple : robm3). Ce compte sera encore demander dans la prochaine etape.")),
            Field('domain',type='text',label=T('Domaine'),comment=T("Selectioner le domaine de ce compte."),default="hlhl.rtss.qc.ca",requires=IS_IN_SET(["hlhl.rtss.qc.ca","cemtl.rtss.qc.ca","hsco.net","pdi.rtss.qc.ca","hmr.hmr.qc.ca","lteas.rtss.qc.ca","icpbe.local","csssslsm.rtss.qc.ca",],multiple=False)),
            Field('email',label=T('Courriel'),default='@ssss.gouv.qc.ca',requires = IS_EMAIL(error_message='Doit etre un courriel valide!'),comment=T("Ce courriel sera utilisé pour envoyer le lien du mot de passe. Si les 3 informations sont valides, la page sera redirigée directement vers votre page de courriel. Le délai de réception peut prendre quelques minutes.")),
    ]

    buttons=[
        TD(INPUT(_type='submit',_value='Recevoir mon mot de passe par couriel',_id='Recevoir mon mot de passe par couriel',_name='Recevoir mon mot de passe par couriel',_style='background-color:#0066ff')),
    ]
    form = SQLFORM.factory(*fields,buttons=[])
    elements=TR(buttons)
    form[0][-1][1].insert(5,elements)
    if form.accepts(request.vars,session,keepvalues=True):
        can_reset=False
        rs=db((db.employees.email.like('%'+request.vars.email+'%'))&(db.employees.logon.like('%'+request.vars.account+"@"+request.vars.domain+'%'))&(db.employees.email_checked==True)).select().first()
        if rs:
            #Has email and  cheched in db, Check with account
            arg1="*hasacount*"+request.vars.account+"*"+request.vars.domain+"*"
            #if rs.unificace.strip()==(str(rs.id)+rs.email).strip():#check encrypt
            #disable check hash
            #if db.employees.unificace.validate(str(rs.id)+rs.email)==(rs.unificace, None):#check hash
            #r.full_name+r.first_name+r.last_name+r.logon+r.email
            if db.employees.unificace.validate(rs.full_name+rs.first_name+rs.last_name+rs.logon+rs.email)==(rs.unificace, None):#check hash
                #check the email exacte math
                this_email=request.vars.email.lower().replace(' ','')#.strip()
                db_email=rs.email.lower().replace(' ','').split(";")
                if this_email in db_email:can_reset=True
                #msg+="hasacount"
        else:
            #Has email in db, Check with name
            rs=db((db.employees.email.like('%'+request.vars.email+'%'))&(db.employees.email_checked==True)).select().first()
            if rs:
                arg1="*hasname*"+request.vars.account+"*"+request.vars.domain+"*"+rs.full_name+"*"+rs.first_name+"*"+rs.last_name+"*"
                #response.flash=db.employees.unificace.validate("149569vphanalasy@ssss.gouv.qc.ca;vphanalasy@gmail.com") == (db(db.employees.first_name=="VILOUNHA").select().first().unificace, None)
                #if rs.unificace.strip()==(str(rs.id)+rs.email).strip():#check encrypt
                #disable check hash
                #if db.employees.unificace.validate(str(rs.id)+rs.email)==(rs.unificace, None):#check hash
                if db.employees.unificace.validate(rs.full_name+rs.first_name+rs.last_name+rs.logon+rs.email)==(rs.unificace, None):#check hash
                    this_email=request.vars.email.lower().replace(' ','')#.strip()
                    db_email=rs.email.lower().replace(' ','').split(";")
                    if this_email in db_email:can_reset=True
                    #msg+="hasname"
        if can_reset:
            import subprocess
            arg1=arg1.replace(' ','5_')
            ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_motdepasse\gestion_motdepasse.ps1'
            p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output,error = p1.communicate()
            output=output.decode('utf-8', 'ignore')
            client_email=request.vars.email
            #save action      
            #db.ads_actions_tracking.insert(edit_by=1072,edit_time=now,actions=client_email+output)#by unificace
            #dispaly action
            #qry=(db.ads_actions_tracking.actions.like('%'+client_email+'%'))
            #fields=[db.ads_actions_tracking.edit_time,db.ads_actions_tracking.actions]
            #grid = SQLFORM.grid(qry,fields=fields,orderby=~db.ads_actions_tracking.id,maxtextlength=250,deletable=False,editable=False,create=False,details=False)
            grid=""
            #send email
            actions=output
            output=output.split(';')
            status=False
            #if output[3]=='reseted':
            if output[3]=='toreset':
                import uuid
                reset_id=uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex
                message="Si vous souhaitez changer votre mot de passe, cliquez sur ce lien: https://"+request.env.http_host+"/init/gestion_motdepasse/password_receive/"+reset_id
                status=mail_send(
                    to=[request.vars.email,],
                    #subject='Libre-service - mon mot de passe',
                    #reply_to='unificace@ssss.gouv.qc.ca',
                    #message='Voici le mot de passe temporaire: '+str(output[2])
                    subject='Libre-service',
                    reply_to='unificace@ssss.gouv.qc.ca',
                    #message=str(output[2])
                    message=message
                )
            if status:
                #";$this_user_name;$this_password;$status;$this_user_GivenName;$this_user_Surname;$this_user_FullName;"
                ip_source=""
                if request.env.remote_addr:ip_source+="|"+request.env.remote_addr
                if request.env.http_x_forwarded_for:ip_source+="|"+request.env.http_x_forwarded_for
                if request.vars.client:ip_source+="|"+request.vars.client
                db.ads_actions_tracking.insert(edit_by=1072,edit_time=now,actions=client_email+ip_source+actions+reset_id)#by unificace
                url_email=client_email.split('@')[1]
                if url_email=="ssss.gouv.qc.ca":url_email="https://outlook.office.com/owa/"
                else:url_email="https://"+url_email
                #redirect('http://www.web2py.com')
                #redirect(URL('index', args=(1, 2, 3), vars=dict(a='b')))
                #prepaire session count for password changing 
                session.count=0
                redirect(url_email)
                #msg+="Le mot de passe temporaire a été envoyé. SVP consultez votre courriel "+request.vars.email+" (Sujet: Libre-service)!"
            else:
                #msg+="Veuillez revérifier votre compte Windows et domaine!"
                msg+="Vos données ne sont pas valides, vous pouvez encore réessayer ou contacter le CSI"#account or domain is incorrect
        else:
            #msg+="Pour utiliser ce service securisé, il faut  d'abord s'inscrire votre couriel au Libre-service en utilisant l'un de vos comptes Windows valides!. Si vous n'avez pas dexieme compte Windows valide, vous devez contatcter le CSI pour réinitialiser votre mot de passe et finalement s'inscrire au Libre-service"        
            msg+="Vos données sont inconnus, vous pouvez encore réessayer ou contacter le CSI"#email is not the list        
        response.flash =msg
    return dict(form=form,grid=grid)

def password_receive():
    response.menu=[
        #(T("Guide d'utilisation du module"), False, URL( f='index'),[]),
        #(T('Inscrire au Libre-service'), False, URL( f='inscription'),[])
        (T("Libre-service"), False, URL( f=''),[]),
        #(T("Copiez votre mot de passe temporaire et le changer sur le Portail Citrix"), False, 'http://storefront.cemtl.rtss.qc.ca/Citrix/CEMTLWeb/'), 
        ]
    msg=""
    form=XML("<b>Votre lien actuel est expiré.</b><br/><br/><i><a href='https://"+request.env.http_host+"/init/gestion_motdepasse/password_reset'>Vous pouvez encore commencer à réinitialiser votre mot de passe en cliquant ici</a></i>")
    grid=""
    this_args=request.args(0) or "noargs"

    if session.count:session.count+=1
    else: session.count=1
    # 5x max
    if (this_args<>"noargs")&(session.count<=5):
        r=db((db.ads_actions_tracking.actions.like('%'+this_args+'%'))).select().first()
        if r:
            #60*60*24*2. 2 jours
            if (now-r.edit_time).total_seconds()<172800.0:
                form = SQLFORM.factory(
                    Field("username",label=T("Votre nom d'utilisateur"),length=15,requires=IS_NOT_EMPTY(),comment=T("Nom d'utilisateur de Windows")),
                    Field('password',label=T("Mot de passe"),type='password',requires = IS_STRONG(min=8, special=0, upper=1)),
                    Field('password_again',label=T("Saisir de nouveau le mot de passe"),type='password',requires=IS_EQUAL_TO(request.vars.password)),
                    buttons=[]
                )
                buttons=[
                    TD(INPUT(_type='submit',_value='Changer mon mot de passe',_id='Changer mon mot de passe',_name='Changer mon mot de passe',_style='background-color:#0066ff')),
                ]
                elements=TR(buttons)
                form[0][-1][1].insert(5,elements)
                if form.process().accepted:
                    r_actions=r.actions
                    username_full=r_actions.split(";")[1].lower()
                    username_simple=username_full.split("@")[0]
                    this_username=request.vars.username.lower()
                    #assured for only toreset not for inscrtiption
                    this_operation=r_actions.split(";")[3]
                    #if True:#by pass username checking
                    if ((this_username==username_full)|(this_username==username_simple))&(this_operation=='toreset'):                   
                        import subprocess
                        r_actions=r.actions.split(";")
                        account_domain=r_actions[1].replace("@","*")
                        arg1="*toreset*"+account_domain+"*"+request.vars.password+"*"
                        arg1=arg1.replace(' ','5_')
                        #msg+= arg1                  
                        ps_tx=r'C:\Users\unificace\unificace\web2py\applications\init\scripts\gestion_motdepasse\gestion_motdepasse.ps1'
                        #ps_tx=""
                        p1 = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',ps_tx,arg1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                        output,error = p1.communicate()
                        output=output.decode('utf-8', 'ignore')
                        actions=output
                        output=output.split(';')
                        status=False
                        if output[3]=='reseted': #output[3]=='reseted':
                            #La réinitialisation du mot de passe peut prendre jusqu'a 15 minutes pour être effective.
                            #form=XML("<b>Voici votre mot de passe temporaire: </b><br/>"+str(output[2])+"<br/><i>Veuillez noter ou copier votre mot de passe temporaire</i><br/><a href='http://storefront.cemtl.rtss.qc.ca/Citrix/CEMTLWeb/'>Vous pouvez changer votre mot de passe temporaire en cliquant ici</a></b>")
                            #Modify action db.ads_actions_tracking.insert(edit_by=1072,edit_time=now,actions=client_email+actions+reset_id)#by unificace
                            #cleaning 
                            db(db.ads_actions_tracking.id==r.id).update(edit_time=now,actions=r.actions.split(";")[0]+";"+output[1]+";"+output[3]+";"+output[4]+";"+output[5]+";"+output[6]+";confirmation at:"+str(r.edit_time))
                            form=XML("<b>Votre mot de passe a été changé avec succès</b>")
                            #msg+=str(output)
                            #msg+="Voici votre de passe temporaire!"
                        else:
                            msg+="Action échouée, Veuillez réessayer ou contacter le CSI!"
                    else:
                        msg+="Veuillez réessayer avec bon nom d'utilisateur ou contacter le CSI!"
    elif (this_args<>"noargs")&(session.count>5):
        r=db((db.ads_actions_tracking.actions.like('%'+this_args+'%'))).select().first()
        if r:
            r_actions=r.actions
            r_actions=r_actions.replace(this_args,'')
            r_actions=r_actions+' tried_reset_5_counts_more at '+str(now)
            db(db.ads_actions_tracking.id==r.id).update(edit_time=now,actions=r_actions)

    response.flash =msg    
    return dict(form=form,grid=grid)

def mail_send(to,subject,reply_to,message):
    from gluon.tools import Mail
    mail = Mail()
    mail.settings.server = 'smtp.rtss.qc.ca:25'
    #mail.settings.sender = 'unificace@ssss.gouv.qc.ca'
    mail.settings.sender = 'unificace@ssss.gouv.qc.ca'
    resend=True
    i=0
    while resend:
        i+=1
        status=mail.send(
            to=to,
            subject=subject,
            reply_to=reply_to,
            message=message
            )
        if status:
            resend=False
        elif i>10:
            resend=False
    return status

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse'))
def actions_tracking():
    response.menu+=[
        (T('Historique'), False, URL( f='actions_tracking'),[]),
        ]
    qry=(db.ads_actions_tracking.edit_by==1072)
    fields=[db.ads_actions_tracking.edit_time,db.ads_actions_tracking.actions]
    grid = SQLFORM.grid(qry,fields=fields,orderby=~db.ads_actions_tracking.id,maxtextlength=250,deletable=False,editable=False,create=False)

    return dict(grid=grid)

##################################
@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse'))
def module_access_create():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Créer un accès'), False, URL(f='module_access_create'),[]),
    ]    
    grid=""    
    qry=(db.pre_user_to_group.group_id.belongs(motdepasse_groups))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse'))
def module_access_edit():
    response.menu+=[
        (T("Gestion des accès au module"), False, '#', [
            (T('Créer un accès'), False, URL(f='module_access_create'),[]),
            (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
        ]),
        (T('Modifier ou supprimer un accès'), False, URL(f='module_access_edit'),[]),
    ]    
    grid=""    
    qry=(db.auth_membership.group_id.belongs(motdepasse_groups))
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,onvalidation=access_onvalidation)
    return dict(grid=grid)

def access_onvalidation(form):
    #form.vars.group_id
    if form.vars.group_id not in motdepasse_groups:
        rs=db(db.auth_group.id.belongs(motdepasse_groups)).select(db.auth_group.role)
        form.errors.group_id="Le groupe doit être dans cette liste: "+((str(rs).replace("auth_group.role","")).replace("gestion_motdepasse",", gestion_motdepasse"))
        form.errors= True
    return

@auth.requires(auth.has_membership(role='admin')|auth.has_membership(role='gestion_motdepasse'))
def users_data():
    response.menu+=[
        (T('Gestion des utilisateurs'), False, URL( f='users_data'),[]),
        ]
    grid=""    
    qry=(db.employees.id>0)
    grid = SQLFORM.grid(qry,maxtextlength=70,deletable=True,oncreate=users_data_oncreate,onupdate=users_data_onupdate)
    return dict(grid=grid)

def users_data_oncreate(form):
    unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(form.vars.full_name+form.vars.first_name+form.vars.last_name+form.vars.logon+form.vars.email)[0])
    db((db.employees.full_name==form.vars.full_name)&(db.employees.first_name==form.vars.first_name)&(db.employees.last_name==form.vars.last_name)&(db.employees.logon==form.vars.logon)&(db.employees.email==form.vars.email)).update(unificace=unificace)
    return

def users_data_onupdate(form):
    #    unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(r.full_name+r.first_name+r.last_name+r.logon+r.email)[0])
    #    db(db.employees.id==r.id).update(unificace=unificace)
    #unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(str(form.record.id)+form.vars.email)[0])
    unificace=str(CRYPT(key='sha512:canada+laos',salt='canada+laos')(form.vars.full_name+form.vars.first_name+form.vars.last_name+form.vars.logon+form.vars.email)[0])
    db(db.employees.id==form.record.id).update(unificace=unificace)
    return
##################################

@auth.requires(auth.has_membership(role='admin'))
def tables():
    menu_url=[]
    tables={"Courriel -> Accès":"employees"}
    for table in tables.keys():
        #menu_url+=[(T(table), False, URL(f='tables',args=[table])),]
        menu_url+=[(T(table), False, URL(f='tables',args=[tables[table]])),]

    response.menu += [(T("Tables de configuration"), False, '#', menu_url)]
    if request.args(0):
        table = request.args(0)
        grid = SQLFORM.grid(db[table],args=request.args[:1],maxtextlength=70,deletable=deletable,editable=editable,create=create,user_signature=user_signature,searchable=searchable,details=details)
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
