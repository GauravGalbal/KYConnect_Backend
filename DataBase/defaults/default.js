const Dummy = require('../../models/Dummy')
const customers = require('./data')

const createDummy = async() => {
    try{
        Dummy.insertMany(customers)
    }catch(err){
        console.log(err)
    }
        // const newDummy = new Dummy({
        //     panid: "123456"
        // })
        // await newDummy.save()
        // .then((res) => {
        //     console.log("created dummy")
        // })
        // .catch((err) => {
        // console.log(err)
        // })
}

module.exports = createDummy