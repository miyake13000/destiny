require_relative './docs_stat'

class DocsStatFormatter
  def self.csv(docs_stat)
    return <<-EOS
    EOS
  end

  def self.html(docs_stat)
    content = []
    content << <<-EOS
<h2>#{docs_stat.year}年度統計情報</h>
<table border="1">
  <tr>
    <td></td>
    <td></td>
    EOS

    for team in docs_stat.teams
      content << "    <td>#{team[1]}</td>\n"
    end

    content << "  </tr>\n"

    for submission in docs_stat.submissions
      content << "  <tr>\n"
      content << "    <td>#{submission[0]}</td>\n"
      content << "    <td>#{submission[1]}</td>\n"
      for team in docs_stat.teams
        content << "    <td>#{docs_stat.number_of(team[0], submission[0])}</td>\n"
      end
      content << "  </tr>\n"
    end

    content << "  <tr>\n"
    content << "    <td></td>\n"
    content << "    <td>平均</td>\n"
    for team in docs_stat.teams
      content << "    <td>#{docs_stat.average_of(team[0])}</td>\n"
    end
    content << "  </tr>\n"

    content << "</table>\n"
    return content.join
  end
end
