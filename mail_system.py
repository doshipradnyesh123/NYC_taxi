import smtplib
import ssl
from email.message import EmailMessage
import streamlit as st
class Mail_alert:

    def __init__(self):
        # Define email sender and receiver
            self.email_sender = 'doshipradnyesh123@gmail.com'
            self.email_password = 'enter_encrpt_passwd'
            self.cc_email=['pradnyeshdoshi01@gmail.com','amanpaliwal777@gmail.com']
        
    def send_mail(self,fare_price,email,pickup_point,dropoff_point):
        try:        
            self.email_receiver = ['pradnyeshdoshi01@gmail.com']            
            # Set the subject and body of the email
            subject = 'Taxi Booking Conformation '

            body_1 = """
            Your Pickup Point is  :  """+pickup_point
            body_2 = """
            Your Dropoff Point is  :  """+dropoff_point
            body_3 = """
            Your Fare amount is  :  """+fare_price

            body=body_1+body_2+body_3
            em = EmailMessage()
            em['From'] = self.email_sender
            em['To'] = self.email_receiver
            em['Subject'] = subject
            em['Cc'] = self.cc_email
            em.set_content(body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.sendmail(self.email_sender, self.email_receiver, em.as_string())

        except Exception as e:
            print("Mail not send !!")

        else:
            print("Mail sended !!")


# m=Mail_alert()
# m.send_mail()

class email_verfication(Mail_alert):

    # def otp_compare(self,otp,otp_check):
    #     if otp!=otp_check:
    #         return False
    #     return True

    def otp_verification(self,customer_mail_id,otp):
        try:        
            print(customer_mail_id,otp)
            self.email_receiver = [customer_mail_id]            
            # Set the subject and body of the email
            subject = 'Mail Verification by New York Taxi '
            body = """
            Your 6 digit OTP  :  """+str(otp)

            em = EmailMessage()
            em['From'] = self.email_sender
            em['To'] = self.email_receiver
            em['Subject'] = subject
            em['Cc'] = self.cc_email
            em.set_content(body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.sendmail(self.email_sender, self.email_receiver, em.as_string())
            # st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102);te } </style>""", unsafe_allow_html=True)
            
            # otp_check=st.text_input(label="OTP Verification",value="",placeholder="Please enter correct OTP")
            # verifyClicked=st.button(" Verify ",key="verify",on_click=self.otp_compare,args=(otp,otp_check))
            # st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102);te } </style>""", unsafe_allow_html=True)
            # if verifyClicked:
                
            #     if len(str(otp_check))==0:
            #         pass
            #     elif str(otp_check)==otp:
            #         st.write("Coreect otp !!")
                    
            #     elif str(otp_check)!=otp :
            #             print("Wrong OTP")
        except Exception as e:
            print("Mail not send !!",e)

        else:
            print("Mail sended !!")

