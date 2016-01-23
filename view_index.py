#!/usr/bin/python

HTML_HEADER = '\
<!DOCTYPE html>\r\
<html lang="en">\r\
  <head>\r\
    <meta charset="utf-8">\r\
    <meta http-equiv="X-UA-Compatible" content="IE=edge">\r\
    <meta name="viewport" content="width=device-width, initial-scale=1">\r\
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->\r\
    <meta name="description" content="">\r\
    <meta name="author" content="">\r\
    <link rel="icon" href="../../favicon.ico">\r\
\r\
    <title>Bj&aumllleberg grisvakt</title>\r\
\r\
    <!-- Bootstrap core CSS -->\r\
    <link href="/assets/css/bootstrap.min.css" rel="stylesheet">\r\
\r\
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->\r\
    <link href="./assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet">\r\
\r\
    <!-- Custom styles for this template -->\r\
    <link href="./assets/css/grid.css" rel="stylesheet">\r\
\r\
    <!-- Just for debugging purposes. Don\'t actually copy these 2 lines! -->\r\
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->\r\
    <script src="./assets/js/ie-emulation-modes-warning.js"></script>\r\
\r\
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->\r\
    <!--[if lt IE 9]>\r\
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>\r\
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>\r\
    <![endif]-->\r\
  </head>\r\
  \r\
  <body>\r\
\r\
    <nav class="navbar navbar-inverse navbar-fixed-top">\r\
      <div class="container">\r\
        <div class="navbar-header">\r\
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">\r\
            <span class="sr-only">Toggle navigation</span>\r\
            <span class="icon-bar"></span>\r\
            <span class="icon-bar"></span>\r\
            <span class="icon-bar"></span>\r\
          </button>\r\
          <a class="navbar-brand" href="#">Bj&aumlllebergs GrisVakt</a>\r\
        </div>\r\
      </div>\r\
    </nav>\r\
'

HTML_FOOTER = "\r\
    <!-- Bootstrap core JavaScript\r\
    ================================================== -->\r\
    <!-- Placed at the end of the document so the pages load faster -->\r\
    <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js\"></script>\r\
    <script>window.jQuery || document.write('<script src=\"../../assets/js/vendor/jquery.min.js\"><\/script>')</script>\r\
    <script src=\"../../dist/js/bootstrap.min.js\"></script>\r\
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->\r\
    <script src=\"../../assets/js/ie10-viewport-bug-workaround.js\"></script>\r\
  </body>\r\
</html>\r\
"
