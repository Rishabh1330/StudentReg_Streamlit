import streamlit as st
# st.title("welcome to my app")
# st.title("welcome to my app")
# st.write("I am Paragraph")
# st.header("Heading")
# st.subheader("Sub Heading")
# st.markdown("<h1>Rishabh</h1>",unsafe_allow_html=True)
# st.markdown("<marquee Style='color:red;'>Urgent: Last Date is 1st March</marquee>",unsafe_allow_html=True)
# st.image("Images\image1.jpeg",caption="Mountains")
# st.button("SignIn")
# # list=[st.checkbox("java"),st.checkbox("Python"),st.checkbox("JavaScript"),st.checkbox("C++")]
# # st.error(list)
# gender=st.radio("Gender",options=['Male','Female','Others'])
# st.error(gender)
# st.success(gender)
# st.text_input("Enter your UserName")
# st.text_input("Enter your Password",type='password')
import sqlite3
from streamlit_option_menu import option_menu

def connectdb():
    conn=sqlite3.connect("mydb.db")
    return conn
def createTable():
    with connectdb() as con:
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name text,password text,rollno int primary key,branch text)")
        con.commit()

def addRecord(data):
    with connectdb() as con:
        cur=con.cursor()
        try:
            cur.execute("INSERT INTO student(name,password,rollno,branch) VALUES(?,?,?,?)",data)
            con.commit()
        except sqlite3.IntegrityError:
            st.error("student already registered")

def display():
    with connectdb() as con:
        cur=con.cursor()
        cur.execute("SELECT * FROM student")
        result =cur.fetchall()
        return result

def checkrollno(rollno):
    with connectdb() as con:
        cur=con.cursor()
        cur.execute("SELECT * FROM student WHERE rollno=?",(rollno,))
        result =cur.fetchone()
        return result

def rePass(reset,rollno):
    with connectdb() as con:
        cur=con.cursor()
        cur.execute("UPDATE student SET password=? WHERE rollno=?",(reset,rollno))
        con.commit()
def signUp():    
    st.title("User Login")
    name=st.text_input("Enter Your Username")
    password=st.text_input("Enter Your Password",type="password")
    RePassword=st.text_input("Re-type pasword",type="password")
    rollno=st.number_input("Roll no",format="%0.0f")
    branch=st.selectbox("Enter Branch",options=["CSE","AIML","MECHANICAL"])
    data=[name,password,rollno,branch]
    if st.button('SignIn'):
        if(password !=RePassword):
            st.warning("Password mismatched")
        else: 
            addRecord(data)
            st.success("Student Registed")
def resetPas():
    st.title("Reset Password")
    roll=st.number_input("Enter your Roll No",format="%0.0f")
    if st.button('Verify Roll no'):
        verified=checkrollno(roll)
        if  not verified:
            st.warning("Wrong Roll No")
        else:
            st.session_state['verified_roll']=roll

    if 'verified_roll' in st.session_state:
        reset=st.text_input("Reset password",type="password")
        reType=st.text_input("Re-type the password",type="password")
        if st.button("Update password"):
            if (reset !=reType):
                st.warning("passwords did not match")
            else:
                rePass(reset,st.session_state['verified_roll'])
                st.success("Password reset")
                del st.session_state['verified_roll']

with st.sidebar:
    selected =option_menu("my App",['Signup','Display all records','Reset Password'],icons=["box-arrow-in-right",'table','gear'])
createTable()
if selected=="Signup":
        signUp()
elif selected=="Reset Password":
        resetPas()
else:
    data=display()  
    st.table(data)