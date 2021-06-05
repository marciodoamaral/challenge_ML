CREATE DATABASE challenge_ml;
ALTER DATABASE challenge_ml CHARACTER SET utf8 COLLATE utf8_general_ci;
use challenge_ml;

CREATE TABLE tb_base_set (
  id_base_set int NOT NULL AUTO_INCREMENT,
  url VARCHAR(300) NOT NULL,
  CONSTRAINT UC_Url UNIQUE (url),
  PRIMARY KEY(id_base_set)
);

INSERT INTO tb_base_set
  (url)
VALUES
  ('https://crawler-test.com/'),
  ('https://webscraper.io/test-sites');

CREATE TABLE tb_link_references (
  id_link_references int NOT NULL AUTO_INCREMENT,
  level VARCHAR(3) NOT NULL,
  top_url VARCHAR(300) NOT NULL,
  url VARCHAR(300) NOT NULL,
  PRIMARY KEY(id_link_references)
);

CREATE TABLE tb_log (
  id_log int,
  msg_log VARCHAR(300) NOT NULL
);

