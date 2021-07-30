require 'cgi'

class SourceUrl
  def initialize(url)
    @url = url
  end

  def is_valid?
    if @url.length >= 2048
      return false
    end
    if @url.include?(" ")
      return false
    end
    uri = URI.parse(@url)
    return uri.is_a?(URI::HTTP) && !uri.host.nil?
  rescue URI::InvalidURIError
    return false
  end

  def to_s
    return @url
  end
end
