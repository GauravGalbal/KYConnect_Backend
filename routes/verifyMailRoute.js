const express= require("express")
const client = require('@sendgrid/mail')
const router = express.Router()
const dotenv = require('dotenv')
dotenv.config()
const nodemailer = require("nodemailer");

client.setApiKey(process.env.MAIL_API_KEY)

let checkOTP

let transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: process.env.MAIL_USER,
    pass: process.env.MAIL_PASS,
    // ⚠ Use environment variables set on the server for these values when deploying
  },
});

function generateOTP() {
    const OTP_LENGTH = 6;
    
    const OTP_CHARS = '0123456789';
    
    let otp = '';
    for(let i = 0; i < OTP_LENGTH; i++) {
      otp += OTP_CHARS.charAt(Math.floor(Math.random() * OTP_CHARS.length));
    }
    return otp;
  }
  

router.post("/sendMailOtp", async(req,res)=>{
  try{
    checkOTP=generateOTP();

    let info = await transporter.sendMail({
      from: process.env.MAIL_USER,
      to: req.body.mail,
      subject: "Verify MAIL",
      html: `<h1>${checkOTP}</h1>`
    });
    // console.log(info.messageId);
    res.send("Mail Sent")
  }catch(err){
    console.log(err)
  }

//     const msg = {
//         to: 'gauravgalbal@gmail.com', // Change to your recipient
//         from: 'gaurav.galbal@spit.ac.in', // Change to your verified sender
//         subject: 'Sending with SendGrid is Fun',
//         text: 'and easy to do anywhere, even with Node.js',
//         html: '<strong>and easy to do anywhere, even with Node.js</strong>',
//       }

//     await client.send(msg).then((d) => {res.send(d)})
//     .catch((err) => {
//         res.send(err);
//     })
})

router.post("/verifyMailOtp", (req,res)=>{
    if(req.body.otp === checkOTP){
        checkOTP=-1;
        res.send("verified")
    }
    else if(checkOTP==-1){   
        res.send("Not Valid")
    }
    else    
        res.send("not Verified")
})

module.exports=router