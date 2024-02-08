
USE RAS_MC_Correcao;

CREATE TABLE IF NOT EXISTS `ClassificacaoQuestoes` (
  `idProva` INT NOT NULL,
  `idQuestao` INT NOT NULL,
  `idAluno` VARCHAR(50) NOT NULL,
  `classificacao` FLOAT NOT NULL,
  PRIMARY KEY (`idProva`, `idAluno`, `idQuestao`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `ClassificacaoProvas` (
  `idProva` INT NOT NULL,
  `idAluno` VARCHAR(50) NOT NULL,
  `classificacao` FLOAT NOT NULL,
  `publica` TINYINT NOT NULL,
  PRIMARY KEY (`idProva`, `idAluno`))
ENGINE = InnoDB;

INSERT INTO `ClassificacaoQuestoes` (`idProva`, `idQuestao`, `idAluno`, `classificacao`) 
VALUES (1, 101, 'PG1', 8.5);

INSERT INTO `ClassificacaoQuestoes` (`idProva`, `idQuestao`, `idAluno`, `classificacao`) 
VALUES (1, 102, 'PG1', 7.0);

INSERT INTO `ClassificacaoQuestoes` (`idProva`, `idQuestao`, `idAluno`, `classificacao`) 
VALUES (1, 103, 'PG2', 6.5);

INSERT INTO `ClassificacaoQuestoes` (`idProva`, `idQuestao`, `idAluno`, `classificacao`) 
VALUES (2, 1, 'PG3', 9.0);


DELIMITER //

CREATE TRIGGER prova_questao_classificacao 
AFTER UPDATE ON ClassificacaoQuestoes 
FOR EACH ROW
BEGIN
    UPDATE ClassificacaoProvas 
    SET classificacao = classificacao + NEW.classificacao - OLD.classificacao
    WHERE idProva = NEW.idProva AND idAluno = NEW.idAluno;
END;

//
DELIMITER ;
