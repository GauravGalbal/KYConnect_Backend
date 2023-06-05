const CustomerRoute = require('./routes/CustomerRoute')
const CorporationRoute = require('./routes/CorporationRoute')
const verifyPhoneRoute = require('./routes/verifyPhoneRoute')
const verifyMailRoute = require('./routes/verifyMailRoute')
const Connection = require('./DataBase/db')
// const createDummy = require('./DataBase/defaults/default')

const dotenv = require('dotenv')
dotenv.config()

const express = require('express')
const cors = require('cors')

const app = express()

const PORT = 8000

Connection();
// createDummy();

app.get("/", (req, res) => {
    res.status(201).json("Hello");
})

app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cors());

// sending local folder online
app.use('/profile', express.static('uploads/images'))


app.use('/customer', CustomerRoute);
app.use('/corporation', CorporationRoute);
app.use('/sendandverify', verifyPhoneRoute);
app.use('/sendandverifyMail', verifyMailRoute);

app.listen(PORT, () => {
    console.log("listening on port 8000")
})