
USE RAS_MC_Notificacoes;

CREATE TABLE IF NOT EXISTS `Notificacoes` (
  `idNotificacao` INT NOT NULL,
  `idUser` VARCHAR(45) NOT NULL,
  `titulo` VARCHAR(50) NULL,
  `descricao` VARCHAR(200) NULL,
  `read` TINYINT NOT NULL,
  PRIMARY KEY (`idNotificacao`, `idUser`))
ENGINE = InnoDB;

INSERT INTO `Notificacoes` (`idNotificacao`, `idUser`, `titulo`, `descricao`, `read`) VALUES
(1, 'PG123', 'Notificação 1', 'Descrição da Notificação 1', 0),
(2, 'PG123', 'Notificação 2', 'Descrição da Notificação 2', 1),
(3, 'PG123', 'Notificação 3', 'Descrição da Notificação 3', 0);
