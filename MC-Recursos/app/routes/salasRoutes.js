import express from "express"
import {insertSala,deleteSala,checkForExam} from "../controllers/salasController.js";

const router = express.Router()

router.post("/", insertSala)
router.delete("/:id", deleteSala)
router.get("/:id", checkForExam)

export default router;