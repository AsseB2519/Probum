import reservasService from "../services/reservasService.js";

export const insertReserva = async (req, res) => {
    try {
        const {data, hora_inicial, hora_final, id_prova, id_sala} = req.body
        const checkFields = ["data", "hora_inicial", "hora_final", "id_prova", "id_sala"]

        // verificar se os campos estão válidos
        for (const field of checkFields) {
            if (req.body[field] === undefined || req.body[field] == null) {
                throw new TypeError(`${field} is null or undefined`)
            }
        }

        const reservaData = {
            data: data,
            hora_inicial: hora_inicial,
            hora_final: hora_final,
            id_prova: id_prova,
            id_sala: id_sala
        }

        const reserva = await reservasService.createReserva(reservaData)
        res.status(201).json({data: reserva})

    } catch (error) {
        if(error instanceof TypeError){
            console.error("Erro ao criar a reserva: ", error.message)
            res.status(400).json({error: `Erro ao criar a reserva: ${error.message}`})
        }
        else{
            console.error("Erro ao criar a reserva: ", error.message)
            res.status(500).json({error: `Erro ao criar a reserva: ${error.message}`})
        }
    }
}

export const deleteReserva = async (req, res) => {
    try {
        const id = req.params.id;

        if(!id){
            throw new TypeError(`id is null or undefined`);
        }

        const sala = await reservasService.removeReserva(id);
        res.status(201).json(sala);

    } catch (error) {
        if(error instanceof TypeError){
            console.error("Erro ao remover a reserva: ", error.message)
            res.status(400).json({error: `Erro ao remover a reserva: ${error.message}`})
        }
        else{
            console.error("Erro ao remover a reserva: ", error.message)
            res.status(500).json({error: `Erro ao remover a reserva: ${error.message}`})
        }
    }
}

export const getProvaInfo = async (req, res) => {
    try {
        const id_prova = req.params.id_prova;

        if(!id_prova){
            throw new TypeError(`id_prova is null or undefined`);
        }

        const prova = await reservasService.getProva(id_prova);
        res.status(201).json(prova);

    } catch (error) {
        if(error instanceof TypeError){
            console.error("Erro ao buscar a reserva: ", error.message)
            res.status(400).json({error: `Erro ao buscar a reserva: ${error.message}`})
        }
        else{
            console.error("Erro ao buscar a reserva: ", error.message)
            res.status(500).json({error: `Erro ao buscar a reserva: ${error.message}`})
        }
    }
}

export const changeReserva = async (req, res) => {
    try {
        const id = req.params.id;

        if(!id){
            throw new TypeError(`id is null or undefined`);
        }

        const {data, hora_inicial, hora_final, id_prova, id_sala} = req.body
        const checkFields = ["data", "hora_inicial", "hora_final", "id_prova", "id_sala"]

        // verificar se os campos estão válidos
        for (const field of checkFields) {
            if (req.body[field] === undefined || req.body[field] == null) {
                throw new TypeError(`${field} is null or undefined`)
            }
        }

        const reservaData = {
            data: data,
            hora_inicial: hora_inicial,
            hora_final: hora_final,
            id_prova: id_prova,
            id_sala: id_sala
        }

        const reserva = await reservasService.updateReserva(id, reservaData)
        res.status(201).json({data: reserva})

    } catch (error) {
        if(error instanceof TypeError){
            console.error("Erro ao atualizar a reserva: ", error.message)
            res.status(400).json({error: `Erro ao atualizar a reserva: ${error.message}`})
        }
        else{
            console.error("Erro ao atualizar a reserva: ", error.message)
            res.status(500).json({error: `Erro ao atualizar a reserva: ${error.message}`})
        }
    }
}

export const validateReserva = async (req, res) => {
    try {

        const {data, hora_inicial, hora_final, id_sala} = req.body // object destructuring
        const checkFields = ["data", "hora_inicial", "hora_final", "id_sala"]

        // verificar se os campos estão válidos
        for (const field of checkFields) {
            if (req.body[field] === undefined || req.body[field] == null) {
                throw new TypeError(`${field} is null or undefined`)
            }
        }

        const reservaData = {
            data: data,
            hora_inicial: hora_inicial,
            hora_final: hora_final,
            id_sala: id_sala
        }

        const reservaValid = await reservasService.isValidReserva(reservaData)
        res.status(201).json(reservaValid)

    } catch (error) {
        if(error instanceof TypeError){
            console.error("Erro ao validar a reserva: ", error.message)
            res.status(400).json({error: `Erro ao validar a reserva: ${error.message}`})
        }
        else{
            console.error("Erro ao validar a reserva: ", error.message)
            res.status(500).json({error: `Erro ao validar a reserva: ${error.message}`})
        }
    }
}