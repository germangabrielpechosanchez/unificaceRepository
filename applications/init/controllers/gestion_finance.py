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

    (T("Calendrier financier"), False, '#', [
        (T("Calendrier financier"), False, URL( f='index'),[]), 
        ]),
    
    ]
import datetime
today=datetime.date.today()
this_year=today.year
this_month=today.month
this_day=today.day
now=datetime.datetime.now()



#@auth.requires(auth.has_membership(role='admin'))
#@auth.requires_login()
def index():
    response.menu+=[
        (T('Calendrier financier'), False, URL( f='index'),[]),
        ]
    if request.vars.dates:
        try:
            d=request.vars.dates.split('-')
            this_date=datetime.date(int(d[0]),int(d[1]),int(d[2]))
        except:
            this_date=today
    else:
        this_date=today
    d=date_financial(this_date)
    request.vars.period=str(d[0])+" / "+str(d[1])
    fields=[Field('dates','date',default=this_date,label=T('Date')),]
    fields.insert(3,Field('period',default=request.vars.period,label=T('Période financière'),comment=T("")))
    #response.flash=request.vars.period
    
    form = SQLFORM.factory(*fields)

    return dict(grid=form)




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
