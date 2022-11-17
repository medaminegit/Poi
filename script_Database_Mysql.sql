CREATE TABLE poi (
    id                MEDIUMINT NOT NULL AUTO_INCREMENT,
    libele            VARCHAR(100),
    lien              VARCHAR(150) NOT NULL,
    classement        INTEGER,
    contact           VARCHAR(300),
    description       VARCHAR(500),
    date_modification DATE,
    localisation_id   INTEGER NOT NULL,
    PRIMARY KEY (id)
)ENGINE=INNODB;
CREATE TABLE region (
    id        MEDIUMINT NOT NULL AUTO_INCREMENT,
    code_inse VARCHAR(10) ,
    libele    VARCHAR(50),
    PRIMARY KEY (id)
)ENGINE=INNODB;
CREATE TABLE departement (
    id         MEDIUMINT NOT NULL AUTO_INCREMENT,
    libele     VARCHAR(50),
    code_insee VARCHAR(10),
    region_id  MEDIUMINT NOT NULL,
    PRIMARY KEY (id)
)ENGINE=INNODB;

ALTER TABLE departement ADD CONSTRAINT fk_region_id FOREIGN KEY (region_id) REFERENCES region(id);