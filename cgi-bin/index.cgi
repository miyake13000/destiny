#!/usr/bin/ruby

require 'cgi'
require_relative '../lib/source_url_controller'

params = CGI.new

def html_head
  return <<-EOS
Content-Type: text/html

<html>
<head>
  <title>Destiny</title>
  <meta http-equiv="content-type" charset="UTF-8">
</head>
<body>
EOS
end

def url_table(urls)
  content = []

  content << <<-EOS
  <table border="1">
    <tr>
      <td>文書管理システムURL</td>
      <td>操作</td>
    </tr>
  EOS
  for url in urls do
    content << <<-EOS
    <tr>
      <td>
        <a href=#{url}>#{url}</a>
      </td>
      <td>
        <form action=get.cgi method=post>
          <input type="hidden" name="url" value="#{url}">
          <button type="submit">情報を取得</button>
        </form>
      </td>
      <td>
        <form action=index.cgi method=post>
          <input type="hidden" name="operation" value="delete">
          <input type="hidden" name="url" value="#{url}">
          <button type="submit">削除</button>
        </form>
      </td>
    </tr>
    EOS
  end
  content << "</table>\n"

  return content.join
end

def add_url_form
  return <<-EOS
  <form action=index.cgi method=post>
    <input type="hidden" name="operation" value="add">
    <input type=url name="url">
    <button type="submit">追加</button>
  </form>
  EOS
end

def html_footer
  return <<-EOS
</body>
</html>
  EOS
end

content = []

content << html_head

if params['operation'].to_s == "add" then
  if SourceUrlController::add(params['url']) == true then
    content << "Success to add URL\n"
  elsif
    content << "Failed to add URL\n"
  end
elsif params['operation'].to_s == "delete" then
  if SourceUrlController::delete(params['url']) == true then
    content << "Success to delete URL\n"
  elsif
    content << "Failed to delete URL\n"
  end
end

source_urls = SourceUrlController::read
if source_urls == [] then
  content << "URL not found\n"
elsif
  content << url_table(source_urls)
end

content << add_url_form
content << html_footer

print content.join
