import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import dotenv from "dotenv";

import salasRoutes from "./routes/salasRoutes.js"
import reservasRoutes from "./routes/reservasRoutes.js"

import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const app = express();
dotenv.config();
app.use(bodyParser.json({ limit: "30mb", extended: true }));
app.use(bodyParser.urlencoded({ limit: "30mb", extended: true }));
app.use(cors());

app.use("/recursos/salas", salasRoutes)
app.use("/recursos/reservas", reservasRoutes)

const APP_PORT = process.env.APP_PORT;

try {
    await prisma.$connect();
    app.listen(APP_PORT, () =>
        console.log(`Server running on port: ${APP_PORT}`),
    );
} catch (error) {
    console.error("Unable to connect to the database:", error);
} finally {
    await prisma.$disconnect();
}