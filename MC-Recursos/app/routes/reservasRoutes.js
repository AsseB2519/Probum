import express from "express"
import {insertReserva,deleteReserva, getProvaInfo, changeReserva, validateReserva} from "../controllers/reservasController.js";

const router = express.Router()

router.post("/", insertReserva)
router.delete("/:id", deleteReserva)
router.get("/:id_prova", getProvaInfo)
router.put("/:id", changeReserva)
router.get("/", validateReserva)

export default router;