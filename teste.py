import SQL.sql_fiodameada as sql
import feedparser


sql.connect_db()


site = feedparser.parse("https://www.aosfatos.org/noticias/feed/")
site2 = feedparser.parse("https://www.e-farsas.com/feed")
site4 = feedparser.parse("https://reddit.com/r/Reddit.rss")
site3 = feedparser.parse(
    "https://feedparser.readthedocs.io/en/latest/examples/rss20.xml"
)


tags = sql.Parceiros().confirm_tags(site4)

print(tags)


sql.disconnect_db()
