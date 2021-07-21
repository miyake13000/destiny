#!/usr/bin/env ruby

require 'cgi'
require 'uri'
require_relative '../lib/source_url'
require_relative '../lib/source_url_controller'

def html_head
  return <<-EOS
Content-Type: text/html; charset=UTF-8

<html>
<head>
  <title>Destiny</title>
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&display=swap" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="/css/style.css">
  <script>
    function loading(){
      document.getElementById("loading").innerHTML = "情報を取得中です．これには数十秒程度かかる場合があります．";
    }
  </script>
</head>
<body>
  <header>文書管理統計システム</header><br>
  <center>
    <h2>取得元URL一覧</h2>
  EOS
end

def url_table(urls)
  content = []

  content << <<-EOS
  <table border="1">
    <tr>
      <th class="url">文書管理システムURL</th>
      <th colspan="2"></th>
    </tr>
  EOS
  for url in urls do
    content << <<-EOS
    <tr>
      <td class="url">
        <a href=#{url}>#{url}</a>
      </td>
      <td>
        <form action=get.cgi method=post>
          <input type="hidden" name="url" value="#{url}">
          <button type="submit" class="button" onclick="loading();">開く</button>
        </form>
      </td>
      <td>
        <form action=index.cgi method=post>
          <input type="hidden" name="operation" value="delete">
          <input type="hidden" name="url" value="#{url}">
          <button type="submit" class="button">削除</button>
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
    <input type=text name="url" class="url" placeholder="URL">
    <button type="submit" class="button">追加</button>
  </form>
  EOS
end

def add_msg(message)
  return <<-EOS
    <div class="div">#{message}</div>
  EOS
end

def add_emsg(message)
  return <<-EOS
    <div class="error">#{message}</div>
  EOS
end

def html_footer
  return <<-EOS
  <div id=loading></div>
  </center>
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

# get url and operation from query
params = CGI.new
url = params['url']
operation = params['operation']

content = []
content << html_head

msg = []
emsg = []

case operation
when "add"
  if valid_url?(url) then
    source_url =  SourceUrl.new(url)
    SourceUrlController::add(source_url)
    msg << "URLを追加しました<br>"
  else
    emsg << "URLが正しくありません<br>"
  end
when "delete"
    source_url =  SourceUrl.new(url)
    SourceUrlController::delete(source_url)
    msg << "URLを削除しました<br>"
end

source_urls = SourceUrlController::read
if source_urls == [] then
  msg << "URLを登録してください<br>"
elsif
  content << url_table(source_urls)
end

content << add_url_form
if msg != []
  content << add_msg(msg.join)
end
if emsg != []
  content << add_emsg(emsg.join)
end
content << html_footer

print content.join
