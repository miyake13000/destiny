require 'bundler'
require_relative './docs_stat'
Bundler.require

class DocsStatController
  def self.read(year)
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))

    begin
      sql_read_teams = 'SELECT team_id, team_name FROM TeamName WHERE year=?'
      teams = db.execute(sql_read_teams, year)
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end

    begin
      sql_read_submissions = 'SELECT submission_id, submission_name FROM SubmissionName WHERE year=?'
      submissions = db.execute(sql_read_submissions, year)
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end

    begin
      sql_read_submission_numbers = 'SELECT team_id, submission_id, submission_number FROM SubmissionNumber WHERE year=?'
      submission_numbers = db.execute(sql_read_submission_numbers, year)
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end

    db.close

    teams.sort!{|a, b| a[0] <=> b[0]}
    submissions.sort!{|a, b| a[0] <=> b[0]}
    docs_stat = DocsStat.new(year, teams, submissions, submission_numbers)
    return docs_stat
  end

  def self.write(docs_stat)
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))

    year = docs_stat.year
    sql_add_year = 'INSERT INTO Year VALUES(?)'
    db.execute(sql_add_year, year)

    sql_add_team = 'INSERT INTO TeamName VALUES(?, ?, ?)'
    sql_add_submission = 'INSERT INTO SubmissionName VALUES(?, ?, ?)'
    sql_add_submission_number = 'INSERT INTO SubmissionNumber VALUES(?, ?, ?, ?)'

    begin
      db.transaction do
        for team in docs_stat.teams
          db.execute(sql_add_team, year, team[0], team[1])
        end
        for submission in docs_stat.submissions
          db.execute(sql_add_submission, year, submission[0], submission[1])
        end
        for submission_number in docs_stat.submission_numbers
          db.execute(sql_add_submission_number, year, submission_number[0], submission_number[1], submission_number[2])
        end
      end
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end
    db.close
  end

  def self.delete
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))
    begin
      db.transaction do
        db.execute('DELETE FROM Year')
        db.execute('DELETE FROM TeamName')
        db.execute('DELETE FROM SubmissionName')
        db.execute('DELETE FROM SubmissionNumber')
      end
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end
    db.close
  end
end
