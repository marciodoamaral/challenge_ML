CREATE DATABASE challenge_ml;
ALTER DATABASE challenge_ml CHARACTER SET utf8 COLLATE utf8_general_ci;
use challenge_ml;

CREATE TABLE tb_base_set (
  id_base_set int NOT NULL AUTO_INCREMENT,
  url VARCHAR(300) NOT NULL,
  PRIMARY KEY(id_base_set)
);

CREATE TABLE tb_link_references_raw (
  id_link_references int NOT NULL AUTO_INCREMENT,
  id_base_set int NOT NULL,
  level VARCHAR(3) NOT NULL,
  top_url VARCHAR(300) NOT NULL,
  url VARCHAR(300) NOT NULL,
  PRIMARY KEY(id_link_references)
);

CREATE TABLE tb_link_references_summary (
  id_link_references_summary int NOT NULL AUTO_INCREMENT,
  id_base_set int NOT NULL,
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
  qty_references int,
  PRIMARY KEY(id_link_references_summary)
);

CREATE TABLE tb_log (
  id_log int,
  msg_log VARCHAR(300) NOT NULL
);

