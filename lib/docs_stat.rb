class DocsStat
  def initialize(year, teams, submissions, submission_numbers)
    @year = year
    @teams = teams
    @submissions = submissions
    @submission_numbers = submission_numbers
  end

  def year
    return @year
  end

  def teams
    return @teams
  end

  def submissions
    return @submissions
  end

  def submission_numbers
    return @submission_numbers
  end

  def include_team_id?(team_id)
    include_flag = false
    for team in @teams
      if team[0] == team_id
        include_flag = true
        break
      end
    end
    return include_flag
  end

  def new_team(id, name)
    @teams << [id, name]
    for submission in @submissions
      @submission_numbers << [id, submission[0], 0]
    end
  end

  def include_submission_id?(submission_id)
    include_flag = false
    for submission in @submissions
      if submission[0] == submission_id
        include_flag = true
        break
      end
    end
    return include_flag
  end

  def new_submission(id, name)
    @submissions << [id, name]
    for team in @teams
      @submission_numbers << [team[0], id, 0]
    end
  end

  def add_submission_number(team_id, submission_id)
    for submission_number in @submission_numbers
      if (submission_number[0] == team_id) && (submission_number[1] == submission_id)
        submission_number[2] += 1
      end
    end
  end

  def number_of(team_id, submission_id)
    number = -1

    for submission_number in @submission_numbers
      if (submission_number[0] == team_id) && (submission_number[1] == submission_id)
        number = submission_number[2]
        break
      end
    end

    return number
  end

  def sum_of(team_id)
    sum = 0

    for submission_number in @submission_numbers
      if submission_number[0] == team_id
        sum += submission_number[2]
      end
    end
    return sum
  end

  def average_of(team_id)
    sum = 0
    count = 0
    for submission_number in @submission_numbers
      if submission_number[0] == team_id
        sum += submission_number[2]
        count += 1
      end
    end

    if count != 0
      average = sum/count.to_f
    else
      average = 0
    end
    return average.round(4)
  end
end
