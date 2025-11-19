source "https://rubygems.org"

gem "jekyll", "~> 3.10.0"
gem "webrick", "~> 1.8"
gem "kramdown-parser-gfm"

# Ruby 3.4+ compatibility
gem "base64"
gem "logger"
gem "bigdecimal"
gem "csv"

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-sitemap", "~> 1.4"
  gem "jekyll-seo-tag", "~> 2.8"
end

# Windows and JRuby does not include zoneinfo files
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end
