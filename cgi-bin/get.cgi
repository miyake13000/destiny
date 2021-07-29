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
    function on_change(src_id, dest_id){
      if (document.getElementById(src_id).checked){
        var query = new FormData();
        query.append("format", "single_year_html");
        query.append("year", dest_id);
        httpGet(query, dest_id, dom);
      }else{
        dom(dest_id, "");
      }
    }
    function compare(src_id, dest_id){
      if (document.getElementById(src_id).checked){
        el = document.getElementsByName("year");
        var years = "";
        for(let i = 0; i < el.length; i++){
          if(el[i].checked == true){
            years += el[i].value;
            years += ",";
          }
        }
        if(years == ""){
          dom(dest_id, "年度を選択してください");
        }else{
          years = years.slice(0, -1);
          var query = new FormData();
          query.append("format", "compare_html");
          query.append("year", years);
          httpGet(query, dest_id, dom);
        }
      }else{
        dom(dest_id, "");
      }
    }
    function httpGet(query, id, callback){
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.onreadystatechange = function(){
        if(xmlHttp.readyState == 4 && xmlHttp.status == 200){
          callback(id, xmlHttp.responseText);
        }else{
          if(xmlHttp.readyState == 4){
            callback(id, "情報の取得に失敗しました．時間をあけて再度実行してください．");
          }
        }
      }
      xmlHttp.open("POST", "display.cgi");
      xmlHttp.send(query);
    }
    function dom(id, content){
      document.getElementById(id).innerHTML = content;
    }
  </script>
</head>
<body>
  <header>文書管理統計システム</header><br>
  EOS

  content << <<-EOS
    <ul class="sidenav">
  EOS
  content << <<-EOS
      <li>
        <input type="checkbox" id="chkbox_compare" value="compare" onclick="compare(this.id, this.value);">
        <label for="chkbox_compare">選択年度を比較</label>
      </li>
      <br>
  EOS
  for year in years do
    content << <<-EOS
      <li>
        <input type="checkbox" id="chkbox#{year}" name="year" value="#{year}" onchange="on_change(this.id, this.value);">
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
  content << "    <div id=\"compare\"></div>\n"
  for year in years do
    content << <<-EOS
    <div id="#{year}"></div>
    EOS
  end

  content << <<-EOS
  </div>
  </center>
</body>
</html>
  EOS

  return content.join
end

def no_year_html
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
    <div class="error">該当ページは文書管理情報が存在しないか，対応しないフォーマットを用いています</div><br>
    <a href=index.cgi>トップページに戻る</a>
  </center>
</body>
</html>
  EOS
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
  parsed_data = DocsStatParser::parse(raw_data)

  years = parsed_data[0]
  docs_stats = parsed_data[1]

  DocsStatController::delete

  for docs_stat in docs_stats
    DocsStatController::write(docs_stat)
  end

  if years == []
    print no_year_html
  else
    print stat_page_html(years)
  end

else
  print notfound_page_html
end

