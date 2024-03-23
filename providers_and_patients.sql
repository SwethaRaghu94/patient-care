
        
CREATE TABLE patients
(
  id                INT          NOT NULL AUTO_INCREMENT,
  first_name        VARCHAR(255) NULL    ,
  last_name         VARCHAR(255) NULL    ,
  email             VARCHAR(255) NULL    ,
  age               INT          NULL    ,
  language          VARCHAR(45)  NULL    ,
  gender            VARCHAR(45)  NULL    ,
  insurance         VARCHAR(255) NULL    ,
  date_enrolled     DATE         NOT NULL,
  medical_condition LONGTEXT     NULL    ,
  symptoms          LONGTEXT     NULL    ,
  goals             LONGTEXT     NULL    ,
  barriers          LONGTEXT     NULL    ,
  expected_results  LONGTEXT     NULL    ,
  created_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  provider_id       INT          NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE providers
(
  id         INT          NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(255) NULL    ,
  last_name  VARCHAR(255) NULL    ,
  email      VARCHAR(255) NULL    ,
  password   VARCHAR(255) NULL    ,
  created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

ALTER TABLE patients
  ADD CONSTRAINT FK_providers_TO_patients
    FOREIGN KEY (provider_id)
    REFERENCES providers (id);

        
      