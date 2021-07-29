require 'bundler'
require_relative './source_url'
Bundler.require

class SourceUrlController
  def self.add(source_url)
    if !source_url.is_valid?
      return "URLが正しくありません"
    end
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))
    sql_add_url = 'INSERT INTO SourceURL(url) VALUES(?)'
    begin
      db.execute(sql_add_url, source_url.to_s)
    rescue SQLite3::ConstraintException
      db.close
      return "URLが重複しています"
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end
    db.close
    return "URLを追加しました"
  end

  def self.delete(source_url)
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))
    sql_delete_url = 'DELETE FROM SourceURL WHERE url=?'
    begin
      db.execute(sql_delete_url, source_url.to_s)
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end
    db.close
    return "URLを削除しました"
  end

  def self.read()
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))
    sql_get_url = 'SELECT url FROM SourceURL'
    begin
      urls = db.execute(sql_get_url)
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end
    db.close
    return urls.flatten
  end
end
