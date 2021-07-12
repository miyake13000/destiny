require 'bundler/setup'
require 'nokogiri'
require_relative './raw_data'
require_relative './docs_stat'

class DocsStatParser
  def self.parse(raw_data)
    html = raw_data.to_s

    html = Nokogiri::HTML.parse(html)
    year_queue = []
    docs_stats = []

    for docs in html.xpath("html/body/table[2]/tr")
      remark = docs.xpath("td[8]").text
      if (docs_info = remark.match(/(\d+)-(\d+)-(.+-.+)-.+/)) != nil

        match = docs.xpath("td[6]").text.match(/(\d+).+/)
        year = match[1].to_i
        team_name = match[0]
        team_id = docs_info[1].to_i
        submission_id = docs_info[2].to_i
        submission_name = docs_info[3]

        if !year_queue.include?(year)
          year_queue << year
          docs_stats << DocsStat.new(year, [], [], [])
        end

        index = year_queue.index(year)

        if !docs_stats[index].include_team_id?(team_id)
          docs_stats[index].new_team(team_id, team_name)
        end

        if !docs_stats[index].include_submission_id?(submission_id)
          docs_stats[index].new_submission(submission_id, submission_name)
        end

        docs_stats[index].add_submission_number(team_id, submission_id)
      end
    end
    return [year_queue, docs_stats]
  end
end
