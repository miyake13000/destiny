require 'bundler'
require 'sqlite3'
require_relative './source_url'
Bundler.require

class SourceUrlController
  def self.add(source_url)
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))
    sql_add_url = 'INSERT INTO SourceURL(url) VALUES(?)'
    db.execute(sql_add_url, source_url.to_s)
    db.close
  end

  def self.delete(source_url)
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))
    sql_delete_url = 'DELETE FROM SourceURL WHERE url=?'
    db.execute(sql_delete_url, source_url.to_s)
    db.close
  end

  def self.read()
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))
    sql_get_url = 'SELECT url FROM SourceURL'
    urls = db.execute(sql_get_url)
    db.close
    return urls.flatten
  end
end
