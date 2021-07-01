#!/usr/bin/ruby

require 'cgi'
require 'uri'
require_relative '../lib/source_url'
require_relative '../lib/source_url_controller'

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

def valid_url?(url)
  uri = URI.parse(url)
  uri.is_a?(URI::HTTP) && !uri.host.nil?
rescue URI::InvalidURIError
  false
end

params = CGI.new
url = params['url']
operation = params['operation']

content = []
content << html_head

case operation
when "add"
  if valid_url?(url) then
    source_url =  SourceUrl.new(url)
    SourceUrlController::add(source_url)
    content << "URLを追加しました\n"
  else
    content << "URLが正しくありません\n"
  end
when "delete"
  if valid_url?(url) then
    source_url =  SourceUrl.new(url)
    SourceUrlController::delete(source_url)
    content << "URLを削除しました\n"
  else
    content << "URLが正しくありません\n"
  end
end

source_urls = SourceUrlController::read
if source_urls == [] then
  content << "URLを登録してください\n"
elsif
  content << url_table(source_urls)
end

content << add_url_form
content << html_footer

print content.join
