require 'bundler/setup'
require 'sqlite3'
require_relative './docs_stat'

class DocsStatController
  def self.read(year)
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))

    sql_read_teams = 'SELECT team_id, team_name FROM TeamName WHERE year=?'
    teams = db.execute(sql_read_teams, year)

    sql_read_submissions = 'SELECT submission_id, submission_name FROM SubmissionName WHERE year=?'
    submissions = db.execute(sql_read_submissions, year)

    sql_read_submission_numbers = 'SELECT team_id, submission_id, submission_number FROM SubmissionNumber WHERE year=?'
    submission_numbers = db.execute(sql_read_submission_numbers, year)
    submission_numbers.sort!{|a, b| [a[1], a[0]] <=> [b[1], b[0]] }

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

    db.close
  end

  def self.delete
    db = SQLite3::Database.new(File.expand_path('../../db/db.sqlite3', __FILE__))

    db.execute('DELETE FROM Year')
    db.execute('DELETE FROM TeamName')
    db.execute('DELETE FROM SubmissionName')
    db.execute('DELETE FROM SubmissionNumber')

    db.close
  end
end
