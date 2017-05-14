## Views
* top_views:
  * CREATE VIEW top_views AS SELECT articles.title, articles.id,articles.author,
                      (SELECT count(log.path) FROM log WHERE log.path::text LIKE '%'||articles.slug::text ) AS views
                    FROM articles ORDER BY views DESC;


* request_stats
    CREATE VIEW request_stats AS SELECT requests.day, requests.requests, errors.errors,ROUND(errors * 100.0 / requests, 1) AS error_percent FROM
    ((SELECT log.time::date AS day,
      count(*) AS requests
      FROM log
      GROUP BY 1
      ORDER BY requests DESC) requests
    JOIN
    (SELECT log.time::date AS day2,
      count(*) AS errors
      FROM log
      WHERE log.status::text != '200 OK'
      group by 1 order by errors DESC) errors
    ON day = day2);
