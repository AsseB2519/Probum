import salasService from "../services/salasService.js";

export const insertSala = async (req, res) => {
    try {
        const {piso, numero, capacidade} = req.body
        const checkFields = ["piso", "numero", "capacidade"]

        // verificar se os campos estão válidos
        for (const field of checkFields) {
          if (req.body[field] === undefined || req.body[field] == null) {
              throw new TypeError(`${field} is null or undefined`)
          }
        }

        const salaData = {
            piso: piso,
            numero: numero,
            capacidade: capacidade
        }

        // Criar a Sala
        const sala = await salasService.createSala(salaData)
        res.status(201).json({data: sala})

    } catch (error) {
        if(error instanceof TypeError){
            console.error("Erro ao criar a sala: ", error.message)
            res.status(400).json({error: `Erro ao criar a sala: ${error.message}`})
        }
        else{
            console.error("Erro ao criar a sala: ", error.message)
            res.status(500).json({error: `Erro ao criar a sala: ${error.message}`})
        }
    }
}

export const deleteSala = async (req, res) => {
    try {
        const id = req.params.id;

        if(!id){
            throw new TypeError(`id is null or undefined`);
        }

        const sala = await salasService.removeSala(id);
        res.status(201).json(sala);

    } catch (error) {
        if(error instanceof TypeError){
            console.error("Erro ao remover a sala: ", error.message)
            res.status(400).json({error: `Erro ao remover a sala: ${error.message}`})
        }
        else{
            console.error("Erro ao remover a sala: ", error.message)
            res.status(500).json({error: `Erro ao remover a sala: ${error.message}`})
        }
    }
}

export const checkForExam = async(req, res) => {
    try{
        const id = req.params.id;

        if(!id){
            throw new TypeError(`id is null or undefined`);
        }

        const hasExamBool = await salasService.hasExam(parseInt(id));
        res.status(201).json(hasExamBool);
    }
    catch (error) {
        if(error instanceof TypeError){
            console.error("Erro ao verificar a sala: ", error.message)
            res.status(400).json({error: `Erro ao verificar a sala: ${error.message}`})
        }
        else{
            console.error("Erro ao verificar a sala: ", error.message)
            res.status(500).json({error: `Erro ao verificar a sala: ${error.message}`})
        }
    }
}
