const mongoose = require("mongoose");

const dummySchema = new mongoose.Schema({
    panid : {
        type: String
    }
})

const Dummy = mongoose.model('Dummy', dummySchema);

module.exports = Dummy;