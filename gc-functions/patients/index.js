const Firestore = require('@google-cloud/firestore');

const PROJECTID = 'cc-lab-3-382417';
const COLLECTION_NAME = 'patients';

const firestore = new Firestore({
  projectId: PROJECTID,
  timestampsInSnapshots: true
});

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');


const app = express();

app.use(bodyParser.json());
app.use(cors());

const isEmpty = (obj) => {
  return Object.keys(obj).length === 0;
};

app.get('', async (req, res) => {
  return await firestore
    .collection(COLLECTION_NAME)
    .get()
    .then((snapshot) => {
      const result = []
      snapshot.docs.forEach(doc => {
        let p = doc.data();
        if(!isEmpty(p)){
          p.id = doc.id;
          result.push(p)
        }
      })

      res.status(200).send(result);
    })
    .catch((err) => {
      console.log(err);
      res.status(500).send('Internval server error');
    });
});


exports.app = app;
