import express, { Express, Request, Response } from "express";
import axios from "axios";
import dotenv from "dotenv";
import cors from "cors";

dotenv.config();

const app: Express = express();
app.use(cors());
const port = process.env.PORT;

app.get("/patients", (req: Request, res: Response) => {
  let config = {
    method: "get",
    url: "https://us-central1-cc-lab-3-382417.cloudfunctions.net/patients",
  };

  axios
    .request(config)
    .then((response) => {
      console.log(response);

      res.send(response.data);
    })
    .catch((error) => {
      res.send(error);
    });
});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
