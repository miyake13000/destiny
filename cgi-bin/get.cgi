#!/usr/bin/env ruby

require 'cgi'
require 'uri'
require 'net/http'
require_relative '../lib/raw_data'
require_relative '../lib/docs_stat_parser'
require_relative '../lib/docs_stat_controller'

def auth_page_html(url)
  return <<-EOS
Content-Type: text/html; charset=UTF-8

<html>
<head>
  <title>Destiny</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
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
    <div class="div-index">該当ページへのアクセスには認証情報が必要です</div>
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
      <button type="submit" onclick="loading();">送信</button>
    </form>
    <div id=loading></div>
    <a href=index.cgi>トップページに戻る</a>
  </center>
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
  <title>Destiny</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&display=swap" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="/css/style.css">
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
        query.append("format", "html");
        query.append("year", year);
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
                callback(year, "情報の取得に失敗しました．時間をあけて再度実行してください．");
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
  <header>文書管理統計システム</header><br>
  EOS

  if years == [] then
    content << <<-EOS
  <center>
    <div class="error">該当ページは文書管理情報が存在しないか，対応しないフォーマットを用いています</div>
    <a href="/cgi-bin/index.cgi">トップページに戻る</a>
    EOS
  else
    content << <<-EOS
    <ul class="sidenav">
    EOS
    for year in years do
      content << <<-EOS
      <li>
     <input type="checkbox" id="chkbox#{year}" onchange="on_change(this.id, #{year})">
     <label for="chkbox#{year}">#{year}</label>
      </li>
      EOS
    end
    content << <<-EOS
      <li><br><a href=index.cgi>トップページに戻る</a></li>
    </ul>
    <cneter>
    <div class="sidenav">
      EOS
    for year in years do
      content << <<-EOS
    <div id="#{year}"></div>
      EOS
    end
  end

  content << <<-EOS
  </div>
  </center>
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
  <title>Destiny</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&display=swap" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="/css/style.css">
</head>
<body>
  <header>文書管理統計システム</header><br>
  <center>
    <div class="error">該当ページが見つかりませんでした</div><br>
    <a href=index.cgi>トップページに戻る</a>
  </center>
</body>
</html>
  EOS
end

params = CGI.new

url = params['url']
username = params['username']
password = params['password']

begin
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
  status_code = res.code
rescue SocketError  => e
  status_code = "0"
end


if status_code == "401" then
  print auth_page_html(url)
elsif status_code == "200" then

  raw_data = RawData.new(res.body)
  puts Time.now.iso8601(3)
  parsed_data = DocsStatParser::parse(raw_data)
  puts Time.now.iso8601(3)

  years = parsed_data[0]
  docs_stats = parsed_data[1]

  DocsStatController::delete
  puts Time.now.iso8601(3)
  for docs_stat in docs_stats
    DocsStatController::write(docs_stat)
    puts Time.now.iso8601(3)
  end

  print stat_page_html(years)
else
  print notfound_page_html
end

