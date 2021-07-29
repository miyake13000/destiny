require 'cgi'

class SourceUrl
  def initialize(url)
    @url = url
  end

  def is_valid?
    uri = URI.parse(@url)
    uri.is_a?(URI::HTTP) && !uri.host.nil?
  rescue URI::InvalidURIError
    false
  end

  def to_s
    return @url
  end
end
