## Views
* top_views:
  * CREATE VIEW top_views AS SELECT articles.title, articles.id,articles.author,
                      (SELECT count(log.path) FROM log WHERE log.path::text LIKE '%'||articles.slug::text ) AS views
                    FROM articles ORDER BY views DESC;
