-- DROP database RAS_Prova;

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema RAS_Prova
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema RAS_Prova
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `RAS_Prova` ;
USE `RAS_Prova` ;

-- -----------------------------------------------------
-- Table `RAS_Prova`.`prova`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`prova` (
  `id` INT NOT NULL,
  `versao` INT NOT NULL,
  `nome` VARCHAR(1000) NOT NULL,
  `criador` VARCHAR(1000) NOT NULL,
  `data` DATETIME NOT NULL,
  `duracao` INT NOT NULL,
  `tempo_admissao` INT NOT NULL,
  `aleatorio` TINYINT NOT NULL,
  `retrocesso` TINYINT NOT NULL,
  PRIMARY KEY (`id`, `versao`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `RAS_Prova`.`questao_desenvolvimento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`questao_desenvolvimento` (
  `id` INT NOT NULL,
  `descricao` VARCHAR(1000) NOT NULL,
  `imagem` VARCHAR(1000) NULL,
  `min_palavras` INT NULL,
  `max_palavras` INT NULL,
  `criterio_avaliacao` VARCHAR(1000) NOT NULL,
  `prova_id` INT NOT NULL,
  `prova_versao` INT NOT NULL,
  `prova_pos` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_questao_desenvolvimento_prova_idx` (`prova_id` ASC, `prova_versao` ASC) VISIBLE,
  CONSTRAINT `fk_questao_desenvolvimento_prova`
    FOREIGN KEY (`prova_id` , `prova_versao`)
    REFERENCES `RAS_Prova`.`prova` (`id` , `versao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RAS_Prova`.`aluno_prova`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`aluno_prova` (
  `id_aluno` VARCHAR(32) NOT NULL,
  `id_prova` INT NOT NULL,
  `prova_versao` INT NOT NULL,
  PRIMARY KEY (`id_aluno`, `id_prova`, `prova_versao`),
  INDEX `fk_aluno_prova_prova_idx` (`id_prova` ASC, `prova_versao` ASC) VISIBLE,
  CONSTRAINT `fk_aluno_prova_prova`
    FOREIGN KEY (`id_prova` , `prova_versao`)
    REFERENCES `RAS_Prova`.`prova` (`id` , `versao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RAS_Prova`.`prof_prova`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`prof_prova` (
  `id_prof` VARCHAR(32) NOT NULL,
  `id_prova` INT NOT NULL,
  PRIMARY KEY (`id_prof`, `id_prova`),
  INDEX `fk_prof_prova_prova_idx` (`id_prova` ASC) VISIBLE,
  CONSTRAINT `fk_prof_prova_prova`
    FOREIGN KEY (`id_prova`)
    REFERENCES `RAS_Prova`.`prova` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RAS_Prova`.`questao_vf`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`questao_vf` (
  `id` INT NOT NULL,
  `descricao` VARCHAR(1000) NOT NULL,
  `imagem` VARCHAR(1000) NULL,
  `prova_id` INT NOT NULL,
  `prova_versao` INT NOT NULL,
  `prova_pos` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_questao_vf_prova_idx` (`prova_id` ASC, `prova_versao` ASC) VISIBLE,
  CONSTRAINT `fk_questao_vf_prova`
    FOREIGN KEY (`prova_id` , `prova_versao`)
    REFERENCES `RAS_Prova`.`prova` (`id` , `versao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RAS_Prova`.`questao_escolha_multipla`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`questao_escolha_multipla` (
  `id` INT NOT NULL,
  `descricao` VARCHAR(1000) NOT NULL,
  `imagem` VARCHAR(1000) NULL,
  `prova_id` INT NOT NULL,
  `prova_versao` INT NOT NULL,
  `prova_pos` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_questao_escolha_multipla_prova_idx` (`prova_id` ASC, `prova_versao` ASC) VISIBLE,
  CONSTRAINT `fk_questao_escolha_multipla_prova`
    FOREIGN KEY (`prova_id` , `prova_versao`)
    REFERENCES `RAS_Prova`.`prova` (`id` , `versao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RAS_Prova`.`questao_espacos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`questao_espacos` (
  `id` INT NOT NULL,
  `descricao` VARCHAR(1000) NOT NULL,
  `imagem` VARCHAR(1000) NULL,
  `prova_id` INT NOT NULL,
  `prova_versao` INT NOT NULL,
  `prova_pos` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_questao_espacos_prova_idx` (`prova_id` ASC, `prova_versao` ASC) VISIBLE,
  CONSTRAINT `fk_questao_espacos_prova`
    FOREIGN KEY (`prova_id` , `prova_versao`)
    REFERENCES `RAS_Prova`.`prova` (`id` , `versao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RAS_Prova`.`alinea`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`alinea` (
  `id` INT NOT NULL,
  `questao` VARCHAR(1000) NOT NULL,
  `correto` TINYINT NOT NULL,
  `pontos_acerto` FLOAT NOT NULL,
  `pontos_erro` FLOAT NOT NULL,
  `questao_id` INT NOT NULL,
  `questao_pos` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RAS_Prova`.`espacos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RAS_Prova`.`espacos` (
  `id` INT NOT NULL,
  `n_espaco` INT NOT NULL,
  `correto` VARCHAR(1000) NOT NULL,
  `texto` VARCHAR(1000) NOT NULL,
  `questao_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_texto_questao_espaco_questao_espacos_idx` (`questao_id` ASC) VISIBLE,
  CONSTRAINT `fk_espacos_questao_espacos`
    FOREIGN KEY (`questao_id`)
    REFERENCES `RAS_Prova`.`questao_espacos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


-- Inserir dados na tabela 'prova'
INSERT INTO `RAS_Prova`.`prova` (`id`, `versao`, `nome`, `criador`, `data`, `duracao`, `tempo_admissao`, `aleatorio`, `retrocesso`)
VALUES
(1, 1, 'Prova de Matemática', 'D123', '2024-01-03 12:00:00', 120, 30, 1, 0),
(2, 1, 'Prova de História', 'D123', '2024-01-04 14:00:00', 90, 20, 0, 1),
(3, 1, 'Prova de Ciências', 'D123', '2024-01-05 10:30:00', 180, 45, 1, 1);

-- Inserir dados na tabela 'questao_desenvolvimento'
INSERT INTO `RAS_Prova`.`questao_desenvolvimento` (`id`, `descricao`, `imagem`, `min_palavras`, `max_palavras`, `criterio_avaliacao`, `prova_id`, `prova_versao`, `prova_pos`)
VALUES
(1, 'Qual é a importância da revolução industrial?', NULL, NULL, NULL, 'Clareza e abordagem do tema.', 1, 1, 1),
(2, 'Elabore um ensaio sobre o impacto da globalização na sociedade atual.', NULL, 200, 500, 'Coerência e análise crítica.', 2, 1, 1);

-- Inserir dados na tabela 'aluno_prova'
INSERT INTO `RAS_Prova`.`aluno_prova` (`id_aluno`, `id_prova`, `prova_versao`)
VALUES
('PG123', 1, 1),
('PG123', 2, 1),
('PG123', 3, 1);

-- Inserir dados na tabela 'prof_prova'
INSERT INTO `RAS_Prova`.`prof_prova` (`id_prof`, `id_prova`)
VALUES
('D123', 1),
('D123', 2),
('D123', 3);

-- Inserir dados na tabela 'questao_vf'
INSERT INTO `RAS_Prova`.`questao_vf` (`id`, `descricao`, `imagem`, `prova_id`, `prova_versao`, `prova_pos`)
VALUES
(3, 'A Terra é plana?', NULL, 1, 1, 2),
(4, 'O sol gira em torno da Terra?', NULL, 2, 1, 2);

-- Inserir dados na tabela 'questao_escolha_multipla'
INSERT INTO `RAS_Prova`.`questao_escolha_multipla` (`id`, `descricao`, `imagem`, `prova_id`, `prova_versao`, `prova_pos`)
VALUES
(5, 'Qual é a capital do Brasil?', NULL, 1, 1, 3),
(6, 'Quem foi o primeiro presidente dos Estados Unidos?', NULL, 2, 1, 3);

-- Inserir dados na tabela 'questao_espacos'
INSERT INTO `RAS_Prova`.`questao_espacos` (`id`, `descricao`, `imagem`, `prova_id`, `prova_versao`, `prova_pos`)
VALUES
(7, 'Complete a frase: O __ é o maior planeta do sistema solar.', NULL, 1, 1, 4),
(8, 'Preencha os espaços em branco na seguinte frase: A __ foi um evento histórico que ocorreu em __.', NULL, 2, 1, 4);

-- Inserir dados na tabela 'alinea'
INSERT INTO `RAS_Prova`.`alinea` (`id`, `questao`, `correto`, `pontos_acerto`, `pontos_erro`, `questao_id`, `questao_pos`)
VALUES
(1, 'A', 1, 1.0, 0.0, 5, 1),
(2, 'B', 0, 0.5, 0.0, 5, 1),
(3, 'C', 0, 0.5, 0.0, 6, 1),
(4, 'D', 0, 0.5, 0.0, 6, 1),
(5, 'E', 0, 0.5, 0.0, 5, 1),
(6, 'V', 0, 0.5, 0.0, 3, 1),
(7, 'F', 0, 0.5, 0.0, 3, 1),
(8, 'V', 0, 0.5, 0.0, 4, 1),
(9, 'F', 0, 0.5, 0.0, 4, 1);

-- Inserir dados na tabela 'espacos'
INSERT INTO `RAS_Prova`.`espacos` (`id`, `n_espaco`, `correto`, `texto`, `questao_id`)
VALUES
(1, 1, 'Júpiter', 'Júpiter é o maior planeta do sistema solar.', 1),
(2, 1, 'Revolução Francesa', 'A Revolução __ foi um evento histórico que ocorreu em 1789.', 2);