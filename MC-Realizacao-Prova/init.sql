USE RAS_MC_Realizar;

CREATE TABLE IF NOT EXISTS `respostas_alunos` (
  `idProva` INT NOT NULL,
  `idQuestao` INT NOT NULL,
  `idAluno` VARCHAR(50) NOT NULL, 
  `resposta` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`idProva`, `idQuestao`, `idAluno`))
ENGINE = InnoDB;

INSERT INTO `respostas_alunos` (`idProva`, `idQuestao`, `idAluno`, `resposta`) 
VALUES (1, 1, 'PG1', 'A');

INSERT INTO `respostas_alunos` (`idProva`, `idQuestao`, `idAluno`, `resposta`) 
VALUES (2, 2, 'PG2', 'B');
