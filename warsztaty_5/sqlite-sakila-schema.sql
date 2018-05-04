/*

Sakila for SQLite is a port of the Sakila example database available for MySQL, which was originally developed by Mike Hillyer of the MySQL AB documentation team. 
This project is designed to help database administrators to decide which database to use for development of new products
The user can run the same SQL against different kind of databases and compare the performance

License: BSD
Copyright DB Software Laboratory
http://www.etl-tools.com

*/

--
-- Table structure for table actor
--
--DROP TABLE actor;

 --
-- Table structure for table country
--

CREATE TABLE country (
  country_id SMALLINT NOT NULL,
  country VARCHAR(50) NOT NULL,
  last_update TIMESTAMP,
  PRIMARY KEY  (country_id)
)
;

CREATE TRIGGER country_trigger_ai AFTER INSERT ON country
 BEGIN
  UPDATE country SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END
;
 
CREATE TRIGGER country_trigger_au AFTER UPDATE ON country
 BEGIN
  UPDATE country SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END
;

--
-- Table structure for table city
--

CREATE TABLE city (
  city_id int NOT NULL,
  city VARCHAR(50) NOT NULL,
  country_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY  (city_id),
  CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;
CREATE  INDEX idx_fk_country_id ON city(country_id)
;

CREATE TRIGGER city_trigger_ai AFTER INSERT ON city
 BEGIN
  UPDATE city SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END
;
 
CREATE TRIGGER city_trigger_au AFTER UPDATE ON city
 BEGIN
  UPDATE city SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END
;


;

--
-- View structure for view actor_info
--

/*
CREATE VIEW actor_info
AS
SELECT
a.actor_id,
a.first_name,
a.last_name,
GROUP_CONCAT(DISTINCT CONCAT(c.name, ': ',
        (SELECT GROUP_CONCAT(f.title ORDER BY f.title SEPARATOR ', ')
                    FROM sakila.film f
                    INNER JOIN sakila.film_category fc
                      ON f.film_id = fc.film_id
                    INNER JOIN sakila.film_actor fa
                      ON f.film_id = fa.film_id
                    WHERE fc.category_id = c.category_id
                    AND fa.actor_id = a.actor_id
                 )
             )
             ORDER BY c.name SEPARATOR '; ')
AS film_info
FROM sakila.actor a
LEFT JOIN sakila.film_actor fa
  ON a.actor_id = fa.actor_id
LEFT JOIN sakila.film_category fc
  ON fa.film_id = fc.film_id
LEFT JOIN sakila.category c
  ON fc.category_id = c.category_id
GROUP BY a.actor_id, a.first_name, a.last_name;
*/

-- TO DO PROCEDURES
-- TO DO TRIGGERS

