require 'bundler/setup'
require 'sqlite3'

sql_create_table = []
sql_create_table << 'CREATE TABLE SourceURL(url TEXT)'
sql_create_table << 'CREATE TABLE Year(year INTEGER)'
sql_create_table << 'CREATE TABLE TeamName(year INTEGER, team_id INTEGER, team_name TEXT)'
sql_create_table << 'CREATE TABLE SubmissionName(year INTEGER, submission_id INTEGER, submission_name TEXT)'
sql_create_table << 'CREATE TABLE SubmissionNumber(year INTEGER, team_id INTEGER, submission_id INTEGER, submission_number INTEGER)'

db = SQLite3::Database.new(File.expand_path('../db.sqlite3', __FILE__))
for sql in sql_create_table
  db.execute(sql)
end

db.close
