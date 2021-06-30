#!/usr/bin/ruby

require 'cgi'
require 'uri'
require 'net/http'
require_relative '../lib/raw_data'
require_relative '../lib/docs_stat_parser'

def auth_page_html(url)
  return <<-EOS
Content-Type: text/html; charset=UTF-8

<html>
<head>
  <title>Destiny</title>
  <meta http-equiv="content-type" charset="UTF-8">
</head>
<body>
該当ページへのアクセスには認証情報が必要です
  <form action=get.cgi method=post>
    <input type="hidden" name="url" value="#{url}">
    <table border="0">
      <tr>
        <td>ユーザ名</td>
        <td><input type="text" name="username"></td>
      </tr>
      <tr>
        <td>パスワード</td>
        <td><input type="password" name="password"></td>
      </tr>
    </table>
    <button type="submit">送信</button>
  </form>
  <a href=index.cgi>トップページに戻る</a>
</body>
<html>
  EOS
end

def stat_page_html(years)
  content = []
  content << <<-EOS
Content-Type: text/html; charset=UTF-8

<html>
<head>
  <title>destiny</title>
  <script>
    function on_change(id, year){
        if (document.getElementById(id).checked){
            checked(year);
        }else{
            unchecked(year);
        }
    }
    function checked(year){
        var query = new FormData();
        query.append("operation", "add");
        query.append("url", "abcdef");
        httpGet(query, year, dom);
    }
    function unchecked(year){
        dom(year, "");
    }
    function httpGet(query, year, callback){
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.onreadystatechange = function(){
        if(xmlHttp.readyState == 4 && xmlHttp.status == 200){
            callback(year, xmlHttp.responseText);
        }else{
            if(xmlHttp.readyState == 4){
                callback(year, "miss");
            }
        }
      }
      xmlHttp.open("POST", "display.cgi");
      xmlHttp.send(query);
    }
    function dom(year, content){
        document.getElementById(year).innerHTML = content;
    }
  </script>
</head>
<body>
  EOS

  if years == [] then
    content << <<-EOS
該当ページは文書管理情報が存在しないか，対応しないフォーマットを用いています
    EOS
  else
    for year in years do
      content << <<-EOS
  <input type="checkbox" id="chkbox#{year}" onchange="on_change(this.id, #{year})">#{year}<br>
      EOS
    end
    for year in years do
      content << <<-EOS
  <div id="#{year}"></div><br>
      EOS
    end
  end

  content << <<-EOS
  <a href=index.cgi>トップページに戻る</a>
</body>
</html>
  EOS

  return content.join
end

def notfound_page_html
  return <<-EOS
Content-Type: text/html; charset=UTF-8

<html>
<head>
  <title>destiny</title>
</head>
<body>
  該当ページが見つかりませんでした
  <a href=index.cgi>トップページに戻る</a>
</body>
</html>
  EOS
end

params = CGI.new

url = params['url']
username = params['username']
password = params['password']

uri = URI::parse(url)
if uri.path == "" then
  uri.path = "/"
end
if uri.query != nil then
  uri.path = "#{uri.path}?#{uri.query}"
end
req = Net::HTTP::Get.new(uri.path)
req.basic_auth username, password
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = (uri.scheme == 'https')
res = http.request(req)

if res.code == "401" then
  print auth_page_html(url)
elsif res.code == "200" then
  raw_data = RawData.new(res.body)
  years = DocsStatParser::parse(raw_data)
  print stat_page_html(years)
else
  print notfound_page_html
end

