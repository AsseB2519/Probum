USE RAS_MC_Users;

CREATE TABLE IF NOT EXISTS `RAS_MC_Users`.`Utilizadores` (
  `numero` VARCHAR(45) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `numero_UNIQUE` (`numero` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  PRIMARY KEY (`numero`))
ENGINE = InnoDB;

INSERT INTO `RAS_MC_Users`.`Utilizadores` (`numero`, `nome`, `email`, `password`) VALUES 
('PG123', 'NomeUsuario', 'nomeusuario1@email.com', 'senha123'),
('D123', 'NomeUsuario', 'nomeusuario2@email.com', 'senha123');