def format(self, record):
  """Apply little arrow and colors to the record.

  Arrow and colors are only applied to sphinxcontrib.versioning log statements.

  :param logging.LogRecord record: The log record object to log.
  """
  formatted = super(ColorFormatter, self).format(record)
  if self.verbose or not record.name.startswith(self.SPECIAL_SCOPE):
      return formatted

  # Arrow.
  formatted = '=> ' + formatted

  # Colors.
  if not self.colors:
      return formatted
  if record.levelno >= logging.ERROR:
      formatted = str(colorclass.Color.red(formatted))
  elif record.levelno >= logging.WARNING:
      formatted = str(colorclass.Color.yellow(formatted))
  else:
      formatted = str(colorclass.Color.cyan(formatted))
  return formatted 