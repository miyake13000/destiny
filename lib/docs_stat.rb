class DocsStat
  def initialize(year, submission_names, team_names, submission_numbers)
    @year = year
    @submission_name = SubmissionName.new(submission_names)
    @team_name = TeamName.new(team_names)
    @submission_number = SubmissionNumber.new(submission_numbers)
  end
end
