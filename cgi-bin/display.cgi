#!/usr/bin/env ruby

require 'cgi'
require_relative '../lib/docs_stat_formatter'
require_relative '../lib/docs_stat_controller'

params = CGI.new

year = params['year']
form = params['format']

case form
when "csv" then
  docs_stat = DocsStatController::read(year)
  docs_stat_csv = DocsStatFormatter::csv(docs_stat)
  file_name = "document_stat_#{year}.csv"
  print <<-EOS
Content-Type: text/csv; charset=UTF-8
Content-Disposition: attachment; filename=#{file_name}

#{docs_stat_csv}
  EOS

when "html" then
  docs_stat = DocsStatController::read(year)
  docs_stat_html = DocsStatFormatter::html(docs_stat)
  print <<-EOS
Content-Type: text/csv; charset=UTF-8

#{docs_stat_html}
<form action="display.cgi" mathod="post">
  <input type="hidden" name="year" value="#{year}">
  <input type="hidden" name="format" value="csv">
  <button type="submit">CSVで保存</button>
</form>
  EOS

when "figure" then
  print <<-EOS
Content-Type: text/plain; charset=UTF-8

現在そのフォーマットはサポートされていません
  EOS

else
  print <<-EOS
Content-Type: text/plain; charset=UTF-8

無効なフォーマットが指定されています
  EOS
end
