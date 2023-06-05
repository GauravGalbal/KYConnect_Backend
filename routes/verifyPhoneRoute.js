const express= require("express")
const router = express.Router()
const twilio = require('twilio')
const dotenv = require('dotenv')
dotenv.config()

const client = twilio(process.env.TWILIO_SID, process.env.TWILIO_TOKEN);

router.post("/sendPhoneOtp", (req,res)=>{
    client.verify.v2
        .services(process.env.TWILIO_VERIFY_SID)
        .verifications.create({ body: 'Hello', to:`+91${req.body.Phone}`, channel: "whatsapp" })
        .then(res.status(201).json("OTP sent..pls check your whatsapp"))
})

router.post("/verifyPhoneOtp", (req,res) => {
    client.verify.v2
    .services(process.env.TWILIO_VERIFY_SID)
    .verificationChecks.create({ to:`+91${req.body.Phone}` , code: req.body.otp })
    .then((verification_check) => {
        if(verification_check.status === "approved")
            res.status(201).json("Approved")
        else
            res.status(201).json('Rejected')
    })
})


module.exports=router