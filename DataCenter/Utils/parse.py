import urllib
from bs4 import BeautifulSoup

def extractText(url):
  with urllib.request.urlopen(url) as url:
    html = url.read()
  soup = BeautifulSoup(html, "html.parser")

  # kill all script and style elements
  for script in soup(["script", "style"]):
      script.extract()    # rip it out

  # get text
  text = soup.body.get_text(separator=' ')

  # break into lines and remove leading and trailing space on each
  lines = (line.strip() for line in text.splitlines())
  # break multi-headlines into a line each
  chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
  # drop blank lines
  text = '\n'.join(chunk for chunk in chunks if chunk)
  return text