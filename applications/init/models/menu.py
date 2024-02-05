# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

#response.logo = A(B('web', SPAN(2), 'py'), XML('&trade;&nbsp;'),
response.logo = A(B('Unificace'),
                  _class="navbar-brand", _href="https://unificace.cemtl.rtss.qc.ca",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T("Menu"), False, '#', [
        (T('Accueil'), False, URL('default', 'index'), []),
        (T('Actualisation des inventaires'), False, URL('actualisation_inventaires', 'index'), []),
        #(T('Libre-service - Réinitialiser mon mot de passe'), False, URL('gestion_motdepasse','index'),[]),
        #(T('Gestion des absences - infra'), False, URL('gestion_absence','index',args=["INFRA ABSENCE",]),[]),
        #(T('Gestion des absences - ops'), False, URL('gestion_absence','index',args=["OPERA ABSENCE",]),[]),
        (T('Gestion des absences'), False, URL('gestion_absence', 'absences_menu'), []),
        (T('Gestion des ADs'), False, URL('gestion_ads', 'index'), []),
        (T('Gestion des inventaires'), False, URL('gestion_inventaires', 'index'), []),
        (T("Gestion des écrans d'affichage"), False, URL('gestion_affichage','index'),[]),
        (T('Gestion de capacité RH (projet)'), False, URL('gestion_ressources','index'),[]),
        (T('Gestion des accès générique'), False, URL('gestion_acces_generique','index'),[]),
        (T('Calendrier des changements'), False, URL('gestion_temps','index'),[]),
        (T('Gestion des courriels'), False, URL('gestion_courriels','index'),[]),
        (T('Gestion de fichiers'), False, URL('gestion_fichiers', 'index'), []),
        (T('Gestion des factures (Telus)'), False, URL('gestion_factures', 'index'), []),
        (T('Gestion des importations vers Octopus'), False, URL('gestion_octopus', 'index'), []),
        (T("Gestion d'impression"), False, URL('gestion_impression', 'index'), []),
        (T("L'inventaire des serveurs"), False, URL('gestion_serveurs', 'index'), []),
        (T('Gestion de mappage (utilisateur au lecteur réseau)'), False, URL('mappage_reseau', 'index'), []),
        (T('Gestion de mappage (imprimante au client léger)'), False, URL('gestion_imprimantes', 'index'), []),
        (T('Gestion du proxy'), False, URL('gestion_proxy', 'index'), []),
        (T('Gestion des PVS'), False, URL('gestion_pvs', 'index'), []),
        (T('Gestion RDM & RDP'), False, URL('gestion_rdm_rdp', 'index'), []),
        (T('Gestion des serveurs'), False, URL('gestion_vms', 'index'), []),
        (T('Rétrofacturation du compte bilan'), False, URL('gestion_retrofacturation', 'index'), []),
        (T('Réclassement du compte projects'), False, URL('gestion_retrofacturation_projects', 'index'), []),
        (T('Calendrier financier'), False, URL('gestion_finance', 'index'), []),
        (T('Nomenclature pour des alias'), False, URL('gestion_nomenclature', 'index'), []),
        (T("Surveillance des alertes"), False, URL('alerts_monitoring', 'index'), []),
        (T("Base de données"), False, URL('database', 'index'), []),
        (T("Gestion des accès"), False, URL('gestion_acces', 'index'), []),
        (T('À propos'), False, URL('about', 'index'), []),
        ]),
]

#DEVELOPMENT_MENU = True
DEVELOPMENT_MENU = False


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, '#', [
            (T('Design'), False, URL('admin', 'default', 'design/%s' % app)),
            LI(_class="divider"),
            (T('Controller'), False,
             URL(
                 'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
            (T('View'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
            (T('DB Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/db.py' % app)),
            (T('Menu Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/menu.py' % app)),
            (T('Config.ini'), False,
             URL(
                 'admin', 'default', 'edit/%s/private/appconfig.ini' % app)),
            (T('Layout'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/layout.html' % app)),
            (T('Stylesheet'), False,
             URL(
                 'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % app)),
            (T('Database'), False, URL(app, 'appadmin', 'index')),
            (T('Errors'), False, URL(
                'admin', 'default', 'errors/' + app)),
            (T('About'), False, URL(
                'admin', 'default', 'about/' + app)),
        ]),
        ('web2py.com', False, '#', [
            (T('Download'), False,
             'http://www.web2py.com/examples/default/download'),
            (T('Support'), False,
             'http://www.web2py.com/examples/default/support'),
            (T('Demo'), False, 'http://web2py.com/demo_admin'),
            (T('Quick Examples'), False,
             'http://web2py.com/examples/default/examples'),
            (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
            (T('Videos'), False,
             'http://www.web2py.com/examples/default/videos/'),
            (T('Free Applications'),
             False, 'http://web2py.com/appliances'),
            (T('Plugins'), False, 'http://web2py.com/plugins'),
            (T('Recipes'), False, 'http://web2pyslices.com/'),
        ]),
        (T('Documentation'), False, '#', [
            (T('Online book'), False, 'http://www.web2py.com/book'),
            LI(_class="divider"),
            (T('Preface'), False,
             'http://www.web2py.com/book/default/chapter/00'),
            (T('Introduction'), False,
             'http://www.web2py.com/book/default/chapter/01'),
            (T('Python'), False,
             'http://www.web2py.com/book/default/chapter/02'),
            (T('Overview'), False,
             'http://www.web2py.com/book/default/chapter/03'),
            (T('The Core'), False,
             'http://www.web2py.com/book/default/chapter/04'),
            (T('The Views'), False,
             'http://www.web2py.com/book/default/chapter/05'),
            (T('Database'), False,
             'http://www.web2py.com/book/default/chapter/06'),
            (T('Forms and Validators'), False,
             'http://www.web2py.com/book/default/chapter/07'),
            (T('Email and SMS'), False,
             'http://www.web2py.com/book/default/chapter/08'),
            (T('Access Control'), False,
             'http://www.web2py.com/book/default/chapter/09'),
            (T('Services'), False,
             'http://www.web2py.com/book/default/chapter/10'),
            (T('Ajax Recipes'), False,
             'http://www.web2py.com/book/default/chapter/11'),
            (T('Components and Plugins'), False,
             'http://www.web2py.com/book/default/chapter/12'),
            (T('Deployment Recipes'), False,
             'http://www.web2py.com/book/default/chapter/13'),
            (T('Other Recipes'), False,
             'http://www.web2py.com/book/default/chapter/14'),
            (T('Helping web2py'), False,
             'http://www.web2py.com/book/default/chapter/15'),
            (T("Buy web2py's book"), False,
             'http://stores.lulu.com/web2py'),
        ]),
        (T('Community'), False, None, [
            (T('Groups'), False,
             'http://www.web2py.com/examples/default/usergroups'),
            (T('Twitter'), False, 'http://twitter.com/web2py'),
            (T('Live Chat'), False,
             'http://webchat.freenode.net/?channels=web2py'),
        ]),
    ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
