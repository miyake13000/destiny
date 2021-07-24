require_relative './docs_stat'

class DocsStatFormatter
  def self.single_year_csv(docs_stat)
    content = []
    content << docs_stat.year.to_s
    content << ","

    for team in docs_stat.teams
      content << ","
      content << team[1]
    end

    for submission in docs_stat.submissions
      content << "\n"
      content << submission[0].to_s
      content << ","
      content << submission[1]

      for team in docs_stat.teams
        content << ","
        content << docs_stat.number_of(team[0], submission[0])
      end
    end

    content << "\n"
    content << ","
    content << "平均"
    averages = docs_stat.averages
    for average in averages
      content << ","
      content << average.to_s
    end
    return content.join
  end

  def self.single_year_html(docs_stat)
    content = []
    content << <<-EOS
<h2>#{docs_stat.year}年度統計情報</h>
<table border="1">
  <tr>
    <td rowspan="2" align="center">成果物番号</td>
    <td rowspan="2" align="center">成果物名</td>
    <td colspan="#{docs_stat.teams.length}" align="center">提出回数</td>
  </tr>
  <tr>
    EOS

    for team in docs_stat.teams
      content << "    <td align=\"center\">#{team[1]}</td>\n"
    end

    content << "  </tr>\n"

    for submission in docs_stat.submissions
      content << "  <tr>\n"
      content << "    <td align=\"right\">#{submission[0]}</td>\n"
      content << "    <td align=\"left\">#{submission[1]}</td>\n"
      for team in docs_stat.teams
        content << "    <td align=\"right\">#{docs_stat.number_of(team[0], submission[0])}</td>\n"
      end
      content << "  </tr>\n"
    end

    content << "  <tr>\n"
    content << "    <td colspan=\"2\" align=\"center\">合計</td>\n"
    for team in docs_stat.teams
      content << "    <td align=\"right\">#{docs_stat.sum_of(team[0])}</td>\n"
    end
    content << "  </tr>\n"

    content << "  <tr>\n"
    content << "    <td colspan=\"2\" align=\"center\">平均</td>\n"
    averages = docs_stat.averages
    for average in averages
      content << "    <td align=\"right\">#{average}</td>\n"
    end
    content << "  </tr>\n"

    content << "</table>\n"

    return content.join
  end

  def self.compare_html(docs_stats)
    content = []
    max_teams_number = 0
    for docs_stat in docs_stats
      if docs_stat.teams.length > max_teams_number
        max_teams_number = docs_stat.teams.length
      end
    end

    content << <<-EOS
    <h2>資料提出回数平均</h2>
    <table>
      <tr>
        <td align="center">年度</td>
    EOS
    for i in 1..max_teams_number
      content << "        <td align=\"center\">#{i}班</td>\n"
    end
    content << "      </tr>\n"

    content << "      <tr>\n"
    for docs_stat in docs_stats
      content << "        <td align=\"left\">#{docs_stat.year}年度</td>\n"
      averages = docs_stat.averages
      for i in 0..(max_teams_number-1)
        if averages[i] == nil
          content << "        <td align=\"right\">-</td>\n"
        else
          content << "        <td align=\"right\">#{averages[i]}</td>\n"
        end
      end
      content << "      </tr>\n"
    end
    content << "  </table>\n"

    return content.join
  end

  def self.compare_csv(docs_stats)
    content = []
    max_teams_number = 0
    for docs_stat in docs_stats
      if docs_stat.teams.length > max_teams_number
        max_teams_number = docs_stat.teams.length
      end
    end
    content << "年度"
    for i in 1..max_teams_number
      content << ",#{i}班"
    end
    for docs_stat in docs_stats
      content << "\n"
      content << "#{docs_stat.year}年度"
      averages = docs_stat.averages
      for i in 0..(max_teams_number-1)
        if averages[i] == nil
          content << ",-"
        else
          content << ",#{averages[i]}"
        end
      end
    end
    return content.join
  end
end
