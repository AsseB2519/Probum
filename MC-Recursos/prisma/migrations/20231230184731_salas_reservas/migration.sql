-- CreateTable
CREATE TABLE `Reservas` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `data` VARCHAR(45) NOT NULL,
    `hora_inicial` VARCHAR(45) NOT NULL,
    `hora_final` VARCHAR(45) NOT NULL,
    `id_prova` INTEGER NOT NULL,
    `id_sala` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Salas` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `piso` VARCHAR(45) NOT NULL,
    `numero` VARCHAR(45) NOT NULL,
    `capacidade` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `Reservas` ADD CONSTRAINT `Reservas_id_sala_fkey` FOREIGN KEY (`id_sala`) REFERENCES `Salas`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
