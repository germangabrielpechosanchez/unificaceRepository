LAYOUT = """<!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js ie6" lang="zh-CN"> <![endif]-->
<!--[if IE 7]> <html class="no-js ie7" lang="zh-CN"> <![endif]-->
<!--[if IE 8]> <html class="no-js ie8" lang="zh-CN"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="zh-CN"> <!--<![endif]-->
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>%(title)s</title>
    <meta name="Description" content="%(description)s" />
    <meta name="Keywords" content="%(keywords)s" />
    <meta name="author" content="%(author)s">
    <meta name="viewport" content="width=1024, user-scalable=no">
    <!-- Core and extension CSS files -->
    <link rel="stylesheet" href="http://imakewebthings.github.com/deck.js/core/deck.core.css">
    <link rel="stylesheet" href="http://imakewebthings.github.com/deck.js/css/common.css">
    <link rel="stylesheet" href="http://imakewebthings.github.com/deck.js/css/home.css">
    <link rel="stylesheet" href="http://imakewebthings.github.com/deck.js/extensions/goto/deck.goto.css">
    <link rel="stylesheet" href="http://imakewebthings.github.com/deck.js/extensions/navigation/deck.navigation.css">
    <link rel="stylesheet" href="http://imakewebthings.github.com/deck.js/extensions/status/deck.status.css">
    <link rel="stylesheet" href="http://imakewebthings.github.com/deck.js/extensions/hash/deck.hash.css">
    <!-- End core and extension CSS files -->
    <!-- Underlying JavaScript files -->
    <script src="http://imakewebthings.github.com/deck.js/modernizr.custom.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.3/jquery.min.js"></script>
    <!-- End underlying JavaScript files -->
    <!-- Core and extension JavaScript files -->
    <script src="http://imakewebthings.github.com/deck.js/core/deck.core.js"></script>
    <script src="http://imakewebthings.github.com/deck.js/extensions/goto/deck.goto.js"></script>
    <script src="http://imakewebthings.github.com/deck.js/extensions/navigation/deck.navigation.js"></script>
    <script src="http://imakewebthings.github.com/deck.js/extensions/status/deck.status.js"></script>
    <script src="http://imakewebthings.github.com/deck.js/extensions/hash/deck.hash.js"></script>
    <!-- End core and extension JavaScript files -->
  </head>
  <body class="deck-container">
    
    %(body)s
    
<script src="http://imakewebthings.github.com/deck.js/home.js"></script> 
  </body>
</html>
"""

def SLIDE(body,title='title',description='',keywords='',author='',extra={}):
    from cgi import escape
    html = str(MARKMIN(body,extra=extra))
    html = html.replace('<h1>','<div class="slide" id="title-slide"><h1>')
    html = html.replace('<h2>','</div><div class="slide"><h2>')
    html = html+'</div>'
    d = dict(title=escape(title,True),             
             description=escape(description,True),
             keywords=escape(keywords,True),
             author=escape(author,True),
             body=html)
    return LAYOUT % d

