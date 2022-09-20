
from ast import arguments
from select import select
from ssl import Options
from typing import final
import streamlit as st
from streamlit_option_menu import option_menu
import time
import mysql.connector
import datetime
from NYC_web import *
from NewYork_Location import *
from PIL import Image
dollors="Free"
# from datetime import datetime
# cust_mail_id=""

import random
from mail_system import Mail_alert,email_verfication

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
aboutSection=st.container()
signUpSection=st.container()
otpSection=st.container()
#Database connection parameter
host_name="localhost"
database_name="NYC_TAXI"
user_name="root"
database_password="root"   
cust_mail_id=''
#icon Link : https://icons.getbootstrap.com/

#1 database connection         
# try:
#     mydb = mysql.connector.connect(
#     host=host_name,
#     database=database_name,
#     user=user_name,
#     password=database_password
# )
# except:
#     print("\tAlert: Database server connection failed !!")
#     raise SystemExit

# cursor = mydb.cursor()


def login(userName: str, password: str) -> bool:
    global cust_mail_id
#     if (userName is None):
#         return False
#     args = [userName, password]
#     sql="select email from user_detail where username=%s and u_password=%s"
#     result_args = cursor.execute(sql, args)
#     verification=cursor.fetchall()
#     print(verification)
#     if len(verification)==0:
#         return False
    
#     cust_mail_id=verification[0][0]
#     # set_cust_mail_id(cust_mail_id)
#     print("cust_mail_id ",cust_mail_id)
    return True

def objective_function():
    st.title("Objective")
    st.subheader("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")  
    st.markdown(objective_part1)
    st.subheader("Predicting pickup density and Fare Price using 50 million taxi trips")
    st.markdown(objective_part2)
    st.subheader("Making transportation more efficient")
    st.markdown(objective_part3)
    st.markdown(objective_part4)
    st.markdown(objective_part5)
    st.markdown(objective_part6)
    st.subheader("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")    

def pradnyesh():
    st.markdown(pradnyesh_1)
    st.markdown(pradnyesh_2)
    st.markdown(pradnyesh_3)
    st.markdown(pradnyesh_4)

def aman():
    st.markdown(aman_1)
    st.markdown(aman_2)
    st.markdown(aman_3)
    st.markdown(aman_4)

def about_us():
    #PRadnyesh Profile
    p1,p2,p3,p4=st.columns(4)
    with p1:
        image = Image.open("profile2.png")
        st.image(image, caption='Co-Founder')   
    
    info1,info2=st.columns(2)
    with info1:
        st.subheader("Pradnyesh Doshi")   

    pradnyesh()
    st.subheader("━━━━━━━━━━━━━━━━━━━━━━━━━")

    #Aman Profile
    p5,p6,p7,p8=st.columns(4)
    with p5:
        image = Image.open("profile4.png")
        st.image(image, caption='CEO')   
    
    info3,info4=st.columns(2)
    with info3:
        st.subheader("Aman Paliwal")

    aman()



#process input and make predition
def prediction_clicked(clock_hours,clock_min,book_date,pickup_point,dropoff_point,passenger_count):
    
    input_data=clock_hours,clock_min,book_date,pickup_point,dropoff_point,passenger_count
    df=input_processing(input_data)    
    output=model.predict(df)
    global dollors
    dollors=f"${output[0]:.2f}"
    print(dollors)
    return dollors
    #st.metric(label="Fare Amount", value=dollors)


def show_main_page(): 
     
    with st.sidebar:
        select=option_menu( menu_title=None,
            options=['Home','Objective','About us'],
            icons=['house-fill','chat-left-quote-fill','file-earmark-code-fill'],
        )
    #page 1
    if select=="Home":
        global cust_mail_id
        with mainSection: 
            st.title("Predict Fare Amount")     
            pickup_point = st.multiselect(
            'Enter Pickup Point',Location_list,key="pickpoint")
            dropoff_point = st.multiselect(
            'Enter Drop-off Point',Location_list,key="droppoint")

            col11,col22=st.columns(2)
            with col11:
                yyyy,mm,dd=[int(x) for x in str(datetime.datetime.date(datetime.datetime.now())).split("-")]
                book_date = st.date_input("Select Booking Date ", datetime.date(yyyy,mm,dd))

            with col22:
                passenger_count=st.number_input("Enter total Passenger",min_value=1,max_value=4)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                clock_hours=st.number_input("Enter Hours ",min_value=1,max_value=23)
            with col2:
                pass
            
            clock_min = st.slider('Enter Minute', 0, 59, 10)

            

            input_data=clock_hours,clock_min,book_date,pickup_point,dropoff_point,passenger_count
            # print(clock_hours,clock_min,book_date,pickup_point,dropoff_point,passenger_count,type(book_date))
            #df=input_processing(input_data) #NYC_web function 
            if(len(pickup_point)==0):
                pass
            elif(len(dropoff_point)==0):
                pass
            elif(len(pickup_point)>=2 or len(dropoff_point)>=2):
                st.error("PLease Select Only One Pickup and Drop-off Location !!")
            elif dropoff_point==pickup_point:
                st.error("PLease Enter Correct Pickup and Dropoff Location !!")
            else:
                col5,col6,col7=st.columns(3)
                with col6:
                    processingClicked = st.button("Predict", key="processing",on_click=prediction_clicked,args=input_data)
                    st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102);te } </style>""", unsafe_allow_html=True)
                    if processingClicked:
                        st.metric(label="Fare Amount", value=prediction_clicked(clock_hours,clock_min,book_date,pickup_point,dropoff_point,passenger_count))               
                        st.balloons()

                        #mail alert system
                        mail_arguments=globals()["dollors"],globals()["cust_mail_id"],pickup_point[0],dropoff_point[0]
                        # arg3=mail_arguments,arg2
                        # print(mail_arguments,arg2,arg3)
                        print(mail_arguments)
                        bookFareClicked=st.button("Conform Taxi",key="booking",on_click=Mail_alert().send_mail,args=mail_arguments)
                        st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102);te } </style>""", unsafe_allow_html=True)
                        


    #Page 2
    if select=='Objective':
        objective_function()
        
    #Page 3
    if select=='About us':
        about_us()

    
    st.sidebar.button("LOGOUT",on_click=LoggedOut_Clicked,key="logout3")
    st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102); } </style>""", unsafe_allow_html=True)



def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    
def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)

def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
        with st.spinner('Your NYC Taxi Prediction page is Loading .......'):
            time.sleep(2)
            #st.success('Done!')
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")

def show_login_page():

    with st.sidebar:
        select2=option_menu( menu_title=None,
            options=['Sign Up','Log in','Objective','About us'],
            icons=['person-plus-fill','box-arrow-in-right','chat-left-quote-fill','file-earmark-code-fill']
        )
    if select2=='Log in':

        with loginSection:
            st.title("NewYork Taxi Fare Application")
            if st.session_state['loggedIn'] == False:
                global userName
                userName = st.text_input (label="UserName", value="", placeholder="Enter your user name")
                password = st.text_input (label="Password", value="",placeholder="Enter password", type="password")
                st.button ("Login", on_click=LoggedIn_Clicked, args= (userName, password))

    if select2=='Objective':
        objective_function()

    if select2=="About us":
        about_us() 

    if select2=='Sign Up':
        show_sign_up_page()

def otp_geneartion():
    otp=random.randint(600000,999999)
    return otp

def otp_compare(otp,otp_check):
    if otp!=otp_check:
        return False
    return True

def otp_verification(otp):
    with otpSection:
                    otp_check=st.text_input(label="OTP Verification",value="",placeholder="Please enter correct OTP")
                    verifyClicked=st.button(" Verify ",key="verify",on_click=otp_compare,args=(otp,otp_check))
                    st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102);te } </style>""", unsafe_allow_html=True)
                    print("check :",otp,otp_check)
                    if verifyClicked:
                        
                        if len(str(otp_check))==0:
                            pass
                        elif str(otp_check)==otp:
                            st.write("Coreect otp !!")
                            
                        elif str(otp_check)!=otp :
                            print("Wrong OTP")


def user_registration(first_name,miiddle_name,last_name,birthdate,email_id,user_id,password): # user added in database
    arguments=first_name,miiddle_name,last_name,birthdate,email_id,user_id,password
    print("argument : ",arguments)
    try:
        sql = """INSERT INTO user_detail (first_name,middle_name,last_name,birth_date,email,username,u_password) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,arguments)
        mydb.commit()
    except Exception as e:
        st.error("Username already exit or Please enter correct information !!")
    else:
        st.success("Thank you for Registration ! Welcome in New York !!")




def show_sign_up_page():
    # with st.sidebar:
    #     select3=option_menu( menu_title=None,
    #         options=['Sign Up','Log in','Objective','About us'],
    #         icons=['person-plus-fill','box-arrow-in-right','chat-left-quote-fill','file-earmark-code-fill']
    #     )

    # if select3=='Sign Up':

    with signUpSection:
        # otp=''
        # email_flag=0
        
        st.title("Registration")
        first_name = st.text_input("First Name : ",placeholder="Enter your name")
        miiddle_name = st.text_input("Middle Name : ",placeholder="Enter your middle name")
        last_name = st.text_input("Last Name : ",placeholder="Enter your surname")

        birth_col,gender_col=st.columns(2)
        with birth_col:
            birthdate = st.date_input("Birth Date : ",datetime.date(1995, 1, 1))
        with gender_col:
            gender=st.selectbox("Gender : ",options=("","Male","Female","Other"))
        
        email_id = st.text_input (label="Email : ", value="", placeholder="Enter your valid mail id")
        user_id = st.text_input (label="Username : ", value="", placeholder="Enter your user name")
        password = st.text_input (label="Password : ", value="",placeholder="Enter password", type="password")
        conform_password = st.text_input (label="Confirm Password : ", value="",placeholder="Re-enter password", type="password")
        
        if len(password)==0 :
            pass
        elif len(conform_password)==0:
            pass
        elif password!=conform_password:
            st.error("PLease Enter correct password !!")
        
        aggrement = st.checkbox("Term and Condition apply !")
        if aggrement :            
           #first_name,middle_name,last_name,birth_date,email,username,u_password
            argument=first_name,miiddle_name,last_name,birthdate,email_id,user_id,password
            signInClicked=st.button(" Sign In ",key="registration",on_click=user_registration,args=argument)
            st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102);te } </style>""", unsafe_allow_html=True)
        
                

            #    otp_verification(otp)
            #     #otp_cheking()
            #     with otpSection:
            #         otp_check=st.text_input(label="OTP Verification",value="",placeholder="Please enter correct OTP")
            #         verifyClicked=st.button(" Verify ",key="verify",on_click=otp_compare,args=(otp,otp_check))
            #         st.markdown(""" <style> div.stButton > button:first-child { background-color: rgb(246, 51, 102);te } </style>""", unsafe_allow_html=True)
            #         if verifyClicked:
                        
            #             if len(str(otp_check))==0:
            #                 pass
            #             elif str(otp_check)==otp:
            #                 st.write("Coreect otp !!")
                            
            #             elif str(otp_check)!=otp :
            #                 print("Wrong OTP")

with headerSection:
    # st.title("NewYork Taxi Fare Application")    
    #first run will have nothing in session_state
    with st.sidebar:
        #st.markdown("PROJECT")
        st.title("NYC Taxi Fare Prediction and Analysis")  
        # image = Image.open("F:\\CDAC\\Project\\Front_end\\profile.png")
        # st.image(image, caption='Co-Founder')
        #st.subheader("MENU 🚕")        
        st.subheader("━━━━━━━━━━━━━━━━━")    
        st.markdown(information_1) 
        st.markdown(information_2)
        st.subheader("━━━━━━━━━━━━━━━━━")      
        

    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page() 
    else:
        if st.session_state['loggedIn']:
            #show_logout_page()    
            show_main_page()  
        else:
            show_login_page()
    
        

    
        

