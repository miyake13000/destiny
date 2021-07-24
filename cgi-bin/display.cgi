#!/usr/bin/env ruby

require 'cgi'
require_relative '../lib/docs_stat_formatter'
require_relative '../lib/docs_stat_controller'

def invalid_html
  return <<-EOS
Cotent-Type: text/plain; charset=UTF-8

無効なリクエストです
  EOS
end

params = CGI.new

year = params['year']
format = params['format']

case format
when "single_year_csv" then
  docs_stat = DocsStatController::read(year)
  docs_stat_csv = DocsStatFormatter::csv(docs_stat)
  file_name = "document_stat_#{year}.csv"
  print <<-EOS
Content-Type: text/csv; charset=UTF-8
Content-Disposition: attachment; filename=#{file_name}

#{docs_stat_csv}
  EOS

when "single_year_html" then
  docs_stat = DocsStatController::read(year)
  docs_stat_html = DocsStatFormatter::html(docs_stat)
  print <<-EOS
Content-Type: text/csv; charset=UTF-8

#{docs_stat_html}
<form action="display.cgi" mathod="post">
  <input type="hidden" name="year" value="#{year}">
  <input type="hidden" name="format" value="single_year_csv">
  <button type="submit">CSVで保存</button>
</form>
<br>
  EOS

when "compare_html" then
  if (years = year.split(',')) == []
    print invalid_html
  else
    docs_stats = []
    for year in years
      docs_stats << DocsStatController::read(year)
    end
    docs_stat_figure = DocsStatFormatter::figure(docs_stats)
    print <<-EOS
Content-Type: text/plain; charset=UTF-8

#{docs_stat_figure}
<form action="display.cgi" mathod="post">
  <input type="hidden" name="year" value="#{years.join(',')}">
  <input type="hidden" name="format" value="compare_csv">
  <button type="submit">CSVで保存</button>
</form>
<br>
    EOS
  end

when "compare_csv" then
  puts <<-EOS
Cotent-Type: text/html; charset=UTF-8

<html>
  <body>
    <div class="index">資料提出回数平均に対して，csvフォーマットは対応していません</div>
  </body>
</html>
  EOS

else
  puts invalid_html
end
