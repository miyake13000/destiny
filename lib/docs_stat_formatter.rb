class DocsStatFormatter
  def self.csv(docs_stat)
    return <<-EOS
,team_A,team_B,team_C,teamD
submission_A,1,1,1,1
submission_B,2,1,2,1
submission_C,1,2,1,2
submission_D,1,2,3,4
    EOS
  end

  def self.html(docs_stat)
    return <<-EOS
<table border="1">
  <tr>
    <th></th>
    <th>team_A</th>
    <th>team_B</th>
    <th>team_C</th>
    <th>team_D</th>
  </tr>
  <tr>
    <th>submission_A</th>
    <th>1</th>
    <th>1</th>
    <th>1</th>
    <th>1</th>
  </tr>
  <tr>
    <th>submission_B</th>
    <th>2</th>
    <th>1</th>
    <th>2</th>
    <th>1</th>
  </tr>
  <tr>
    <th>submission_C</th>
    <th>1</th>
    <th>2</th>
    <th>1</th>
    <th>2</th>
  </tr>
  <tr>
    <th>submission_D</th>
    <th>1</th>
    <th>2</th>
    <th>3</th>
    <th>4</th>
  </tr>
</table>
    EOS
  end
end
