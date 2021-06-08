CREATE DATABASE challenge_ml;
ALTER DATABASE challenge_ml CHARACTER SET utf8 COLLATE utf8_general_ci;
use challenge_ml;

CREATE TABLE tb_base_set (
  id_base_set int NOT NULL AUTO_INCREMENT,
  url VARCHAR(300) NOT NULL,
  PRIMARY KEY(id_base_set)
);

INSERT INTO tb_base_set
  (url)
VALUES
  ('https://www.google.com'),
  ('https://about.google/?utm_source=google-BR&utm_medium=referral&utm_campaign=hp-footer&fg=1');

CREATE TABLE tb_link_reference_raw (
  level VARCHAR(3) NOT NULL,
  top_url VARCHAR(300) NOT NULL,
  url VARCHAR(300) NOT NULL
);

CREATE TABLE tb_link_reference_summary (
  id_link_reference_summary int NOT NULL AUTO_INCREMENT,
  url VARCHAR(300) NOT NULL,
  qty_reference int,
  PRIMARY KEY(id_link_reference_summary)
);

CREATE TABLE tb_link_reference_feature_summary (
  id_link_reference_summary int NOT NULL AUTO_INCREMENT,
  url VARCHAR(300) NOT NULL,
  feature_01 int,
  feature_02 int,
  feature_03 int,
  feature_04 int,
  feature_05 int,
  feature_06 int,
  feature_07 int,
  feature_08 int,
  feature_09 int,
  feature_10 int,
  qty_reference int,
  PRIMARY KEY(id_link_reference_summary)
);

CREATE TABLE tb_log (
  id_log int,
  msg_log VARCHAR(300) NOT NULL
);

