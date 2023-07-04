const express = require('express')
const multer = require('multer')
const { spawn } = require('child_process')
const path = require('path');
const fs = require('fs');
const nodemailer = require("nodemailer");
const dotenv = require('dotenv')
dotenv.config()



const Dummy = require('../models/Dummy')
const Customer=require('../models/Customer')
const CryptoJS = require('crypto-js');
const PDFDocument = require('pdfkit');

const router = express.Router()

let transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: process.env.MAIL_USER,
      pass: process.env.MAIL_PASS,
      // ⚠ Use environment variables set on the server for these values when deploying
    },
  });


const secretKey = 'mySecretKey';
const URL = "https://kyconnectfinalbackend.onrender.com/"
// const URL = "http://localhost:8000"

let dataCompare

// Updating the filename & selecting destination 
const storage = multer.diskStorage({
    destination: './uploads/images',
    filename: (req,file,cb)=> {
        return cb(null,`${file.originalname}`);
    }
})

// Storage destination is selected 
const upload = multer({
    storage: storage
})

router.get('/saveCustomer', async(req,res) => {
    try{
        res.status(201).send("Saves Customer data");
    }catch(err){
        res.status(500).send(err);
        console.log(err);
    }
});


// Save Details of Customer
router.post("/saveCustomer", upload.fields([{name:'selfieImage'},{name:'signature'},{name:'aadhaarFrontImage'},{name:'aadhaarBackImage'},{name:'panImage'}]), async(req, res) => {
    try{  
        const newCustomer= new Customer({
            firstName:req.body.firstName,
            middleName:req.body.middleName,
            lastName:req.body.lastName,
            email:req.body.email,
            gender:req.body.gender,
            maritalStatus:req.body.maritalStatus,
            phone:req.body.phone,
            address:req.body.address,
            city:req.body.city,
            state:req.body.state,
            country:req.body.country,
            postalCode:req.body.postalCode,
            panid:req.body.panid,
            aadhaarid:req.body.aadhaarid,
            selfieImage: `${URL}/profile/${req.files['selfieImage'][0].filename}`,
            panImage:`${URL}/profile/${req.files['panImage'][0].filename}`,
            aadhaarFrontImage:`${URL}/profile/${req.files['aadhaarFrontImage'][0].filename}`,
            aadhaarBackImage:`${URL}/profile/${req.files['aadhaarBackImage'][0].filename}`,
            signature:`${URL}/profile/${req.files['signature'][0].filename}`,
            account:req.body.account,
        })

        // Load the CryptoJS library (make sure you've included the library in your HTML file)
        // Define a secret key for encryption and decryption
        // const ciphertext = CryptoJS.AES.encrypt(newCustomer.firstName, secretKey).toString();
        // // Print the encrypted data to the console
        // console.log('Encrypted data:', ciphertext);
        // // Decrypt the data using the same secret key
        // const bytes = CryptoJS.AES.decrypt(ciphertext, secretKey);
        // const decryptedPlaintext = bytes.toString(CryptoJS.enc.Utf8);
        // // Print the decrypted data to the console
        // console.log('Decrypted data:', decryptedPlaintext);
        // console.log(originalpass)
    
        // res.send(newCustomer.panImage);
    
    // Sending photo link to python file and receiving the json data (OCR CHECK)
    const childPython = spawn('python',['./verify_kyc.py',newCustomer.panImage,newCustomer.aadhaarBackImage,newCustomer.aadhaarFrontImage,newCustomer.selfieImage])

    childPython.stdout.on('data',(bufferData)=>{
        console.log(bufferData);
        // const bufferString = Buffer.from(bufferData).toString();
        // dataCompare = JSON.parse(bufferString)
        // console.log(dataCompare);
    })
    childPython.stderr.on('data',(data)=>{
        console.log(`stderr:${data}`);
        console.log(data);
        res.send(data)
    })
    childPython.on('close',async(code)=>{
        console.log(`Python done ${code}`)
        // console.log(dataCompare);
        // console.log(dataCompare)
        // res.status(201).send(dataCompare)

    // // Comparing OCR data with newCustomer 

    // if(dataCompare['name'] === "False")
    //     res.send("nadhar")
    // else if(dataCompare['pan_number'] === "False")
    //     res.send("npan")
    // else if(dataCompare['face_verfication_result'] === "False")
    //     res.send("nface")
    // else{
    //     const Name = newCustomer.firstName+' '+newCustomer.middleName+' '+newCustomer.lastName;
    //     if(Name.trim().toLowerCase() != dataCompare['name'].trim().toLowerCase() || newCustomer.aadhaarid.trim().slice(-4) != dataCompare['aadhaar_no'].trim()){
    //         res.send("nadhar")
    //     }
        
    //     else{
    //         console.log("Aadhaar Data match")

    //         if(dataCompare['pan_number']!=newCustomer.panid){
    //             res.send("npan")
    //         }
    //         else {   
    //             console.log("PAN Data match")

    // //         // Risk Assessment
    //         const user = await Dummy.find({panid: newCustomer.panid})
    //         console.log(user)
    //         if(user[0])
    //             //console.log('Suspicious Customer');
    //             res.send('sus')
    //         else{
    // //             // Loan Account -> CIBIL Score Check
    //             if(newCustomer.account.trim().toLowerCase() === "loan"){
    //                 console.log("Checking CIBIL Score")
    //                 let cibil /*Request to API for obtaining CIBIL Score*/
    //             if(newCustomer.firstName === "Gaurav" || newCustomer.firstName === "Kaustubh" || newCustomer.firstName === "Harshita")
    //                     cibil=750
    //             else
    //                 cibil=650

    //             if(cibil<700)
    //                 // console.log('ncibil')
    //                 res.send("ncibil")
    //             else{
    //                 console.log(`Correct CIBIL ${cibil}`)
    //             }
    //         }

                const newCustomer2= new Customer({
                    firstName:CryptoJS.AES.encrypt(req.body.firstName, secretKey).toString(),
                    middleName:CryptoJS.AES.encrypt(req.body.middleName, secretKey).toString(),
                    lastName:CryptoJS.AES.encrypt(req.body.lastName, secretKey).toString(),
                    email:CryptoJS.AES.encrypt(req.body.email, secretKey).toString(),
                    gender:CryptoJS.AES.encrypt(req.body.gender, secretKey).toString(),
                    maritalStatus:CryptoJS.AES.encrypt(req.body.maritalStatus, secretKey).toString(),
                    phone:CryptoJS.AES.encrypt(req.body.phone, secretKey).toString(),
                    address:CryptoJS.AES.encrypt(req.body.address, secretKey).toString(),
                    city:CryptoJS.AES.encrypt(req.body.city, secretKey).toString(),
                    state:CryptoJS.AES.encrypt(req.body.state, secretKey).toString(),
                    country:CryptoJS.AES.encrypt(req.body.country, secretKey).toString(),
                    postalCode:CryptoJS.AES.encrypt(req.body.postalCode, secretKey).toString(),
                    panid:CryptoJS.AES.encrypt(req.body.panid, secretKey).toString(),
                    aadhaarid:CryptoJS.AES.encrypt(req.body.aadhaarid, secretKey).toString(),
                    selfieImage: CryptoJS.AES.encrypt(`${URL}/profile/${req.files['selfieImage'][0].filename}`, secretKey).toString(),
                    panImage:CryptoJS.AES.encrypt(`${URL}/profile/${req.files['panImage'][0].filename}`, secretKey).toString(),
                    aadhaarFrontImage:CryptoJS.AES.encrypt(`${URL}/profile/${req.files['aadhaarFrontImage'][0].filename}`, secretKey).toString(),
                    aadhaarBackImage:CryptoJS.AES.encrypt(`${URL}/profile/${req.files['aadhaarBackImage'][0].filename}`, secretKey).toString(),
                    signature:CryptoJS.AES.encrypt(`${URL}/profile/${req.files['signature'][0].filename}`, secretKey).toString(),
                    account:CryptoJS.AES.encrypt(req.body.account, secretKey).toString(),
                })
                
                const bytes = CryptoJS.AES.decrypt(newCustomer2.selfieImage, secretKey);
                const decryptedPlaintext = bytes.toString(CryptoJS.enc.Utf8);
                console.log(decryptedPlaintext);

                await newCustomer2.save()

                const doc = new PDFDocument();


                const document = `KYC - SELF DECLARATION – INDIVIDUAL CUSTOMER\nTo\nBank PLC\nAndheri Branch\nDear Sir/Madam,\nI ${newCustomer.firstName}_${newCustomer.middleName}_${newCustomer.lastName} solemnly declare that the information provided in this form with respect to my above mentioned customer id no. is correct and latest to the best of my knowledge. I authorize the bank to update its records as per the information given in this form and replace all such details given by me earlier.\nCurrent Residential Address\n${newCustomer.address}\nDeclaration: I confirm having attached and signed across my recent photograph above.\nFull name of the customer:${newCustomer.firstName} ${newCustomer.middleName} ${newCustomer.lastName}\nPAN Number :- ${newCustomer.panid}\n`

                doc.text(document);

                const filename = 'output.pdf';
                const filepath = path.join(__dirname, 'pdfs', filename);
              
                // Pipe the PDF into a file stream
                const fileStream = fs.createWriteStream(filepath);
                doc.pipe(fileStream);
              
                // Finalize the PDF and close the file stream
                doc.end();

                fileStream.on('finish', () => {
                    console.log(`PDF file saved to ${filepath}`);
                    //res.send('PDF file saved successfully');
                });

                try{               
                    let info = await transporter.sendMail({
                      from: process.env.MAIL_USER,
                      to: newCustomer.email,
                      subject: "Declaration Form",
                      body: "You have successfully completed the process... Here is your declaration form",
                       // Embedded image links to content ID
                      attachments: [{
                        filename: `${newCustomer.firstName}_Declaration.pdf`,
                        path: './routes/pdfs/output.pdf',
                      //   cid: 'unique@gmail.com' // Sets content ID
                      }]
                    });
                    console.log(info.messageId);
                  }catch(err){
                    console.log(err)
                }
        res.send("goboi")
            // }
            // }
        // }
    // }
    })

    }catch(err){
        res.status(500).send(err);
        console.log(err);
    }
});

module.exports = router
