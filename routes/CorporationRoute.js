const express=require('express')

const Corporation=require('../models/Corporation')

const router = express.Router()


router.get('/saveCorporation', async(req,res) => {
    try{
        res.status(201).send("Corporation Data");
    }catch(err){
        res.status(500).send(err);
        console.log(err);
    }
});


// Save Details of Customer
router.post("/saveCorporation", async(req, res) => {
    try{
        const newCorporation= new Corporation({
            companyName: req.body.companyName, 
            registrationNumber: req.body.registrationNumber,
            companyEmail: req.body.companyEmail,
            country: req.body.country,
            startDate: req.body.startDate,
            businessType: req.body.businessType,
        
            managerPanid: req.body.managerPanid,
            managerName: req.body.managerName,
            managerPhone: req.body.managerPhone,
            managerEmail: req.body.managerEmail,
            managerPanFront: req.body.managerPanFront,
            managerPanBack: req.body.managerPanBack,
        
            financeManagerPanid: req.body.financeManagerPanid,
            financeManagerName: req.body.financeManagerName,
            financeManagerPhone: req.body.financeManagerPhone,
            financeManagerEmail: req.body.financeManagerEmail,
            financeManagerPanFront: req.body.financeManagerPanFront,
            financeManagerPanBack: req.body.financeManagerPanBack,
        
            directorPanid: req.body.directorPanid,
            directorName: req.body.directorName,
            directorEmail: req.body.directorEmail,
            directorPhone: req.body.directorPhone,
            directorPanFront: req.body.directorPanFront,
            directorPanBack: req.body.directorPanBack,
        
            managerSelfieImage: req.body.managerSelfieImage,
            financeManagerSelfieImage: req.body.financeManagerSelfieImage,
            directorSelfieImage: req.body.directorSelfieImage,
        
            businessDescription: req.body.businessDescription,
            incorporationCertificate: req.body.incorporationCertificate,
            businessLicense: req.body.businessLicense
        })

    await newCorporation.save().then(() => {
        console.log("Saved Data Corporation");
    });

    }catch(err){
        res.status(500).send(err);
        console.log(err);
    }
});



module.exports = router