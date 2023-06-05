const mongoose = require('mongoose');

const corporationSchema = new mongoose.Schema({

// Company Details
  companyName: {
    type: String,
    required: true
  },
  registrationNumber: {
    type: String,
    required: true,
    unique: true
  },
  companyEmail: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  country: {
    type:String,
    required:true
  },
  startDate: {
    type: Date,
    required:true
  },
  businessType: {
    type: String,
    required: true
  },

// Manager Details
  managerPanid: {
    type: String,
    required: true
  },
  managerName: {
    type: String,
    required: true
  },
  managerPhone: {
    type: String,
    required: true
  },
  managerEmail: {
    type: String,
    required: true
  },
  managerPanFront: {
    type: String,
    required: true
  },
  managerPanBack: {
    type: String,
    required: true
  },

// Finance Manager Details
  financeManagerPanid: {
    type: String,
    required: true
  },
  financeManagerName: {
    type: String,
    required: true
  },
  financeManagerPhone: {
    type: String,
    required: true
  },
  financeManagerEmail: {
    type: String,
    required: true
  },
  financeManagerPanFront: {
    type: String,
    required: true
  },
  financeManagerPanBack: {
    type: String,
    required: true
  },

// Director Details
  directorPanid: {
    type: String,
    required: true
  },
  directorName: {
    type: String,
    required: true
  },
  directorEmail: {
    type: String,
    required: true
  },
  directorPhone: {
    type: String,
    required: true
  },
  directorPanFront: {
    type: String,
    required: true
  },
  directorPanBack: {
    type: String,
    required: true
  },

// Images
  managerSelfieImage: {
    type: String,
    required: true
  },
  financeManagerSelfieImage: {
    type: String,
    required: true
  },
  directorSelfieImage: {
    type: String,
    required: true
  },

// Documents
  businessDescription: {
    type: String,
    required: true
  },
  incorporationCertificate: {
    type: String,
    required: true
  },
  businessLicense: {
    type: String,
    required: true
  },
},{timestamps: true});

const Corporation = mongoose.model('Corporation', corporationSchema);

module.exports = Corporation;