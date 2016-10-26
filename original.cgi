#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import subprocess
import cgi
import cgitb 
#cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

print """
<html>

<head><title>Sample CGI Script</title></head>

<body>

  <h3> Sample CGI Script </h3>
"""

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

output = subprocess.check_output("ssh noether \'nproc\'", shell=True)
print output 


print """

  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="test.cgi">
    <p>message: <input type="text" name="message"/></p>
  </form>

</body>

</html>
""" % cgi.escape(message)
