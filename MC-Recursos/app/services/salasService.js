import {PrismaClient} from "@prisma/client"

const prisma = new PrismaClient()

const salasService = {

    createSala: async(salaData) => {
        return prisma.salas.create({
            data: salaData
        })
    },

    removeSala: async(id)=> {
        return prisma.salas.delete({
            where: { id: parseInt(id) }
        })
    },

    hasExam: async(id) => {
        const reservasComSala = await prisma.reservas.findMany({
            where: { id_sala: id }
        })
        return reservasComSala.length > 0;
    }
}

export default salasService