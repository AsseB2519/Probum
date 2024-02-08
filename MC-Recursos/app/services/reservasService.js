import {PrismaClient} from "@prisma/client"
import salasService from "../services/salasService.js";

const prisma = new PrismaClient()

const reservasService = {

    createReserva: async(reservaData) => {
        return prisma.reservas.create({
            data: reservaData
        })
    },

    removeReserva: async(id)=> {
        return prisma.reservas.delete({
            where: { id: parseInt(id) }
        })
    },

    getProva: async(id) => {
        return prisma.reservas.findMany({
            where: { id_prova: parseInt(id) }
        })
    },

    updateReserva: async(id, reservaData) => {
        return prisma.reservas.update({
            where: { id: parseInt(id) },
            data: reservaData
        })
    },

    isValidReserva: async(reservaData) => {
        const reservasComSala = await prisma.reservas.findMany({
            where: { id_sala: reservaData.id_sala }
        })

        const salaTemReserva = await salasService.hasExam(reservaData.id_sala)
        if(!salaTemReserva) return true

        for (const reservaComp of reservasComSala) {
            if( reservaData.data === reservaComp.data ){
                const [hI, mI] = reservaData.hora_inicial.split('h').map(Number);
                const start = hI * 60 + mI;

                const [hF, mF] = reservaData.hora_final.split('h').map(Number);
                const end = hF * 60 + mF;

                const [hCI, mCI] = reservaComp.hora_inicial.split('h').map(Number);
                const startC = hCI * 60 + mCI;

                const [hCF, mCF] = reservaComp.hora_final.split('h').map(Number);
                const endC = hCF * 60 + mCF;

                if(start < endC && end > startC) return false
            }
        }
        return true;
    }
}

export default reservasService