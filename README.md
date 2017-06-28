# Logs Analysis
![Part of the Udacity Front-End Web Development Nanodegree](https://img.shields.io/badge/Udacity-Full--Stack%20Web%20Developer%20Nanodegree-02b3e4.svg)
---------------------
Reporting tool to output plain text reports on the data in the `newsdata.sql` database.

## Requirements
* Python3
* PostgreSQL
* Vagrant
* Virtual Box

## Usage
1. Ensure [Vagrant](https://www.vagrantup.com/), [Virtual Box](https://www.virtualbox.org/) and [Python](https://www.python.org/) are installed on your machine.
2. Clone the Udacity [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
3. Delete the `/tournament` directory in the clone.
4. [Clone](https://github.com/SteadBytes/logs-analysis.git) (or [download](https://github.com/SteadBytes/logs-analysis/archive/master.zip)) this repo into the `/vagrant` directory.
5. [Download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) the `newsdata.sql` data file.
6. Extract zip contents into cloned `/vagrant/udacity-fsnd-logs-analysis` directory
7. Launch the VM:
  * `vagrant$ vagrant up`
8. SSH into the VM:
  * On Mac/Linux `vagrant$ vagrant ssh`
    * Gives SSH connection details on windows
  * Windows use Putty or similar SSH client
9. In the VM navigate to the `/vagrant/udacity-fsnd-logs-analysis` directory:
  * `$ cd /vagrant/tournament`
10. Load the data into the `news` database already in the VM:
  * `$psql -d news -f newsdata.sql`
11. Run the two `CREATE VIEW` statements in the [Database Views](#database-views) section.
12. Run python report script:
  * `$ python3 logs_analysis.py`

## Database Views
* **top_views**:
  ```
  CREATE VIEW top_views AS SELECT
  articles.title, articles.id, articles.author,
  (SELECT count(log.path)
    FROM log
    WHERE log.path::text LIKE '%'||articles.slug::text) AS views
  FROM articles
  ORDER BY views DESC;
  ```
* **request_stats**
```
CREATE VIEW request_stats AS SELECT
requests.day, requests.requests, errors.errors,
ROUND(errors * 100.0 / requests, 1) AS error_percent
FROM(
  (SELECT log.time::date AS day,
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
```
