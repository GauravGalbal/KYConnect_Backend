const mongoose = require("mongoose");

const customerSchema = new mongoose.Schema({
  firstName: {
    type: String,
    required: true
  },
  middleName: {
    type: String,
    required: true
  },
  lastName: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true,
  },
  gender: {
    type: String,
    required:true
  },
  maritalStatus: {
    type: String,
    required:true
  },
  phone: {
    type: String,
    required: true
  },
  address: {
    type: String,
    required: true
  },
  city: {
    type: String,
    required: true
  },
  state: {
    type: String,
    required: true
  },
  country: {
    type: String,
    required: true
  },
  postalCode: {
    type: String,
    required: true
  },
  panid: {
    type: String,
    required: true
  },
  aadhaarid: {
    type: String
  },
  selfieImage: {
    type: String,
    required: true
  },
  panImage: {
    type: String,
    required: true
  },
  aadhaarFrontImage: {
    type: String
  },
  aadhaarBackImage: {
    type: String
  },
  signature: {
    type: String,
    required: true
  },
  account: {
    type: String,
    required: true
  },
},{timestamps: true});

const Customer = mongoose.model('Customer', customerSchema);

module.exports = Customer;