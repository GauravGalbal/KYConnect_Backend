const dotenv = require('dotenv')
dotenv.config()
const mongoose = require('mongoose')

const Connection = async() => {
    try{
        // mongoose.connect(process.env.MONGO_URL).then(
        //     console.log('DataBase Connection Successful')
        // )
        mongoose.connect(process.env.MONGO_URL).then(
            console.log('Database Connection Successful')
        )
    }catch(err){
        console.log(err);
    }
}

module.exports = Connection