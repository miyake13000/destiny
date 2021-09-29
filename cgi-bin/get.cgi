#!/usr/bin/env ruby

require 'cgi'
require 'uri'
require 'net/http'
require_relative '../lib/raw_data'
require_relative '../lib/docs_stat_parser'
require_relative '../lib/docs_stat_controller'

def main(params)

  if !valid_request?(params)
    print invalid_html
    return
  end

  url = params['url']
  username = params['username']
  password = params['password']

  begin
    uri = URI::parse(url)
    if uri.path == "" then
      uri.path = "/"
    end
    if uri.query != nil then
      path = "#{uri.path}?#{uri.query}"
    else
      path = uri.path
    end

    req = Net::HTTP::Get.new(path)
    req.basic_auth username, password
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = (uri.scheme == 'https')
    http.open_timeout = 5
    http.read_timeout = 10
    res = http.request(req)
    status_code = res.code
  rescue SocketError, ArgumentError, Errno::ECONNREFUSED, Net::ReadTimeout, Net::OpenTimeout  => e
    print error_html("該当ページが見つかりませんでした")
    return
  end

  if status_code == "401"
    print auth_page_html(url)
    return

  elsif status_code == "200"
    raw_data = RawData.new(res.body)
    parsed_data = DocsStatParser::parse(raw_data)

    years = parsed_data[0]
    docs_stats = parsed_data[1]

    if years == []
      print error_html("該当ページは文書管理情報が存在しないか，対応しないフォーマットを用いています")
      return
    end

    DocsStatController::delete
    for docs_stat in docs_stats
      DocsStatController::write(docs_stat)
    end

    print stat_page_html(years, url)
    return

  else
    print error_html("情報を取得できませんでした")
    return
  end
end

def valid_request?(params)
  if params.request_method == "POST"
    if params['url'] == ""
      return false
    else
      return true
    end
  else
    return false
  end
end

def invalid_html
  return <<-EOS
Content-Type: text/plain; charset=UTF-8

Invalid Request
  EOS
end


def auth_page_html(url)
  return <<-EOS
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
  <title>Destiny</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&display=swap" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="../css/style.css">
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

def stat_page_html(years, url)
  content = []
  content << <<-EOS
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
  <title>Destiny</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&display=swap" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="../css/style.css">
  <script>
    function change_year_chkbox(src_id, dest_id){
      change_zip_form_value();
      change_compare_chkbox()
      if (document.getElementById(src_id).checked){
        var query = new FormData();
        query.append("format", "single_year_html");
        query.append("year", dest_id);
        httpGet(query, dest_id, dom);
      }else{
        dom(dest_id, "");
      }
    }
    function change_compare_chkbox(){
      if (document.getElementById("chkbox_compare").checked){
        document.getElementById("ipt_zip_format").value = "compare_zip"
        years = get_checking_years();
        if(years == ""){
          dom("compare", "年度を選択してください");
        }else{
          var query = new FormData();
          query.append("format", "compare_html");
          query.append("year", years);
          httpGet(query, "compare", dom);
        }
      }else{
        document.getElementById("ipt_zip_format").value = "single_zip"
        dom("compare", "");
      }
    }
    function change_zip_form_value(){
      years = get_checking_years();
      if (years == ""){
        document.getElementById("ipt_zip_year").value = "#{years.join(',')}";
      }else{
        document.getElementById("ipt_zip_year").value = years;
      }
    }
    function get_checking_years(){
      el = document.getElementsByName("chkbox_single_year");
      var years = "";
      for(let i = 0; i < el.length; i++){
        if(el[i].checked == true){
          years += el[i].value;
          years += ",";
        }
      }
      return years.slice(0, -1)
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
  <center>
    取得元URL : <a href="#{url}">#{url}</a>
  </center>
  EOS

  content << <<-EOS
  <div class="container">
    <div class="sidebar">
      <ul class="side">
        <li>
          <input type="checkbox" id="chkbox_compare" value="compare" onclick="change_compare_chkbox(this.id, this.value);">
          <label for="chkbox_compare">選択年度を比較</label>
        </li>
        <br>
   EOS
   for year in years do
     content << <<-EOS
        <li>
          <input type="checkbox" id="chkbox#{year}" name="chkbox_single_year" value="#{year}" onchange="change_year_chkbox(this.id, this.value);">
          <label for="chkbox#{year}">#{year}</label>
        </li>
    EOS
  end
  content << <<-EOS
        <li>
          <br>
          <form action=display.cgi method="post">
            <input type="hidden" id="ipt_zip_year" name="year" value="#{years.join(',')}">
            <input type="hidden" id="ipt_zip_format" name="format" value="compare_zip">
            <button type="submit">まとめて保存</button>
          </form>
        </li>
        <li><br><a href=index.cgi>トップページに戻る</a></li>
      </ul>
    </div>

    <div class="main">
      <div id="compare"></div>
  EOS
  for year in years do
    content << <<-EOS
      <div id="#{year}"></div>
    EOS
  end
  content << <<-EOS
    </div>
  </div>
</body>
</html>
  EOS

  return content.join
end

def error_html(emsg)
  return <<-EOS
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
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
    <div class="error">#{emsg}</div><br>
    <a href=index.cgi>トップページに戻る</a>
  </center>
</body>
</html>
  EOS
end

main (CGI.new)
