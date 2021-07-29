require 'bundler/setup'
require_relative './docs_stat'
Bundler.require
require 'SVG/Graph/Bar'
require 'zip'

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
    content << "合計"
    sums = docs_stat.sums
    for sum in sums
      content << ","
      content << sum.to_s
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
<h2>#{docs_stat.year}年度統計情報</h2>
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
    sums = docs_stat.sums
    for sum in sums
      content << "    <td align=\"right\">#{sum}</td>\n"
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

  def self.compare_figure(docs_stats)
    max_teams_number = 0
    x_axis = []
    for docs_stat in docs_stats
      if docs_stat.teams.length > max_teams_number
        max_teams_number = docs_stat.teams.length
      end
      x_axis << docs_stat.year.to_s
    end

    data_per_year = []
    for docs_stat in docs_stats
      tmp = []
      averages = docs_stat.averages
      for i in 0..(max_teams_number-1)
        if averages[i] == nil
          tmp << 0.0
        else
          tmp << averages[i]
        end
      end
      data_per_year << tmp
    end

    data_collection = []
    for i in 0..(max_teams_number - 1)
      tmp = []
      for data in data_per_year
        tmp << data[i]
      end
      data_collection << tmp
    end

    options = {
      :width             => 1000,
      :height            => 500,
      :stack             => :side,
      :fields            => x_axis,
      :graph_title       => "成果物提出回数平均",
      :show_graph_title  => true,
      :show_x_title      => true,
      :x_title           => '年度',
      :show_y_title      => true,
      :y_title           => '平均',
      :y_title_text_direction => :bt,
      :scale_integers => true,
      :no_css            => true
    }
    g = SVG::Graph::Bar.new(options)

    count = 1
    for data in data_collection
      g.add_data( {
        :data => data,
        :title => "#{count}班  "
      })
      count += 1
    end

    return g.burn_svg_only
  end

  def self.single_zip(docs_stats)
    zip_data = Zip::OutputStream.write_buffer do |zip|
      for docs_stat in docs_stats
        zip.put_next_entry("docs_stat_#{docs_stat.year}.csv")
        zip.write self.single_year_csv(docs_stat)
      end
    end
    return zip_data.string
  end

  def self.compare_zip(docs_stats)
    zip_data = Zip::OutputStream.write_buffer do |zip|
      for docs_stat in docs_stats
        zip.put_next_entry("docs_stat_#{docs_stat.year}.csv")
        zip.write self.single_year_csv(docs_stat)
      end
      zip.put_next_entry("docs_stat_average.csv")
      zip.write self.compare_csv(docs_stats)
      zip.put_next_entry("docs_stat_graph.svg")
      zip.write self.compare_figure(docs_stats)
    end
    return zip_data.string
  end
end
