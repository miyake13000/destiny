#!/usr/bin/ruby

require 'cgi'

params = CGI.new

print "Content-Type: text/html\n\n"
print "<html>\n"
print "<body>\n"
print "It Works\n"
print "</body>\n"
print "</html>\n"
