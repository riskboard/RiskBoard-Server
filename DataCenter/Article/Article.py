import logging
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from pycountry import languages
from langdetect import detect
from rake_nltk import Rake

from DataCenter.Utils.parse import extractText

class Article():
  '''
  Defines the Article class. An article refers to
  a specific article, for example a Twitter article,
  a news article
  '''
  _collectionKey = 'article'
  _SENTENCE_COUNT = 4

  def __init__(self, url, date, actorIDs=[], peopleIDs=[],
               orgIDs=[], locationIDs=[], language=None,
               keywords=None, summary=None, id=None, db=None, **kwds):
    '''
    Initializes an Article class from a url.
    '''
    self.date = date
    self.url = url
    self.actorIDs = actorIDs
    self.peopleIDs = peopleIDs
    self.orgIDs = orgIDs
    self.locationIDs = locationIDs
    if not (language and keywords and summary):
      parse = self._parse_url(url)
      if parse: (self.language, self.keywords, self.summary) = parse
    else:
      self.language = language
      self.keywords = keywords
      self.summary = summary

    if db:
      self._db = db
      self._collection = db[Article._collectionKey]
      if not id:
        self.storeDB(db)
      else:
        self._mongoID = id
        self._id = str(id)

  def _parse_url(self, url):
    '''
    Takes in a url, and returns its language, keywords, and summary
    '''
    try:
      text = extractText(url)
      language = languages.get(alpha_2=detect(text)).name
      parser = HtmlParser.from_url(url, Tokenizer(language))
      stemmer = Stemmer(language)
      summarizer = Summarizer(stemmer)
      summarizer.stop_words = get_stop_words(language)
      summary = ''
      for sentence in summarizer(parser.document, Article._SENTENCE_COUNT):
        summary += str(sentence)

      r = Rake(language, max_length=3)
      r.extract_keywords_from_text(text)
      keywords = r.get_ranked_phrases()[:10]

      return language, keywords, summary

    except Exception as e:
      logging.error(e)
      return False

  def storeDB(self, db):
    '''
    Stores in database
    '''
    if not db:
      logging.error('No DB provided')
      return False
    self._mongoID = self._collection.insert_one(self._serialize()).inserted_id
    self._id = str(self._mongoID)
    return self._mongoID

  def _serialize(self):
    '''
    Serializes the Article class
    '''
    return {
      'url': self.url,
      'date': self.date,
      'actorIDs': self.actorIDs,
      'peopleIDs': self.peopleIDs,
      'orgIDs': self.orgIDs,
      'locationIDs': self.locationIDs,
      'language': self.language,
      'keywords': self.keywords,
      'summary': self.summary,
    }

  @classmethod
  def fromDB(cls, obj):
    '''
    Creates an Actor class from MongoDB object
    '''
    return cls(
      obj['url'], obj['date'], obj['actorIDs'], obj['peopleIDs'],
      obj['orgIDs'], obj['locationIDs'], obj['language'],
      obj['keywords'], obj['summary'], obj['_id'], obj['_db'])