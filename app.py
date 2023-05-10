from flask import Flask,render_template,request,redirect
import ibm_db

conn =  ibm_db.connect("database = bludb; hostname = 125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; port = 30426; uid = ksy13207; password = Z5tm8KPtdC4hpoaL; security = SSL; sslcertificate = DigiCertGlobalRootCA.crt", " ", " ")
print("connection done")

app=Flask(__name__)

@app.route('/' , methods=["GET","POST"])
def home():
    return render_template('homepage.html')

@app.route('/register' , methods=["GET","POST"])
def register(msg=""):
    if request.method == 'POST':        
        user=request.form['username']
        emailid=request.form['email']
        password=request.form['password']    
        list1=[user,emailid,password]    
        print(list1)

        query= "select * from registeration where username= ?"         
        stmt = ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,user)
        ibm_db.execute(stmt) 
        details=ibm_db.fetch_assoc(stmt)               
        if details:
            msg="username already exists,try another"
            
        else :
            query= "select * from registeration where emailid= ?"         
            stmt = ibm_db.prepare(conn,query)
            ibm_db.bind_param(stmt,1,emailid)
            ibm_db.execute(stmt) 
            details=ibm_db.fetch_assoc(stmt)               
            if details:
                msg="emailid have already been used,please log in"                
                
            else :
                query="insert into registeration values(?,?,?)"
                stmt = ibm_db.prepare(conn,query)                                
                ibm_db.bind_param(stmt,1,user)
                ibm_db.bind_param(stmt,2,emailid)
                ibm_db.bind_param(stmt,3,password)
                ibm_db.execute(stmt)
                msg="account registration succesfull,login to website"
                return redirect('/login')   
    return render_template('register.html',msg=msg)



@app.route('/login' , methods=["GET","POST"])
def login(msg=""):
    if request.method == 'POST':
        user = request.form['user_name']
        pw=request.form["pass_word"]
        list=[user,pw]
        print(list)
        
        query="select * from registeration where username= ? and password= ?"
        stmt=ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,user)
        ibm_db.bind_param(stmt,2,pw)
        ibm_db.execute(stmt)
        details=ibm_db.fetch_assoc(stmt)
        if details:
            msg="welcome  "+user
            return redirect('/')
        else:
            msg="username doesn't exist,please register first"
            
    return render_template("login.html",msg=msg)



@app.route('/profile')
def profile():
    
    return render_template('profile.html',msg="login to view profile")

if __name__ == "__main__" :
    app.run(debug = True)
