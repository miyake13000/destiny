#!/usr/bin/env ruby

require 'cgi'
require 'uri'
require_relative '../lib/source_url'
require_relative '../lib/source_url_controller'

def main(params)

  if valid_request?(params) == false
    print invalid_html
    return
  end

  url = params['url']
  operation = params['operation']

  content = []
  content << header

  msg = []
  emsg = []

  case operation
  when "add"
    source_url =  SourceUrl.new(url)
    begin
      res = SourceUrlController::add(source_url)
    rescue => e
      emsg << "#{e.message}<br>\n"
    end
      msg << "    #{res}<br>\n"
  when "delete"
    source_url =  SourceUrl.new(url)
    res = SourceUrlController::delete(source_url)
    msg << "    #{res}<br>\n"
  end

  source_urls = SourceUrlController::read()

  if source_urls == []
    msg << "URLを登録してください<br>\n"
  elsif
    content << url_table(source_urls)
  end

  content << url_form

  if msg != []
    content << msg(msg.join)
  end
  if emsg != []
    content << emsg(emsg.join)
  end

  content << footer

  print content.join
  return
end

def valid_request?(params)
  if params['operation'] != ''
    if params['operation'] != "add" && params['operation'] != "delete"
      return false
    end
    if params.request_method != "POST" || params['url'] == ""
      return false
    end
  end
  return true
end

def invalid_html
  return <<-EOS
Content-Type: text/plain; charset=UTF-8

Invalid Request
  EOS
end

def header
  return <<-EOS
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
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
  <table border="1" class="url">
    <tr>
      <th class="url">文書管理システムURL</th>
      <th colspan="2" class="button"></th>
    </tr>
  EOS
  for url in urls do
    url_escaped = CGI::escapeHTML(url)
    content << <<-EOS
    <tr>
      <td class="url">
        <a href=#{url_escaped}>#{url_escaped}</a>
      </td>
      <td class="button">
        <form action=get.cgi method=post>
          <input type="hidden" name="url" value="#{url_escaped}">
          <button type="submit" class="button" onclick="loading();">開く</button>
        </form>
      </td>
      <td class="button">
        <form action=index.cgi method=post>
          <input type="hidden" name="operation" value="delete">
          <input type="hidden" name="url" value="#{url_escaped}">
          <button type="submit" class="button">削除</button>
        </form>
      </td>
    </tr>
    EOS
  end
  content << "</table>\n"
  return content.join
end

def url_form
  return <<-EOS
  <form action=index.cgi method=post>
    <input type="hidden" name="operation" value="add">
    <input type=text name="url" class="url" placeholder="URL">
    <button type="submit" class="button">追加</button>
  </form>
  EOS
end

def msg(message)
  return <<-EOS
    <div class="div">#{message}</div>
  EOS
end

def emsg(message)
  return <<-EOS
    <div class="error">#{message}</div>
  EOS
end

def footer
  return <<-EOS
  <div id=loading></div>
  </center>
</body>
</html>
  EOS
end

main(CGI.new)
