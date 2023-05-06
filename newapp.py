from flask import Flask,render_template,request,redirect
import ibm_db

conn =  ibm_db.connect("database = bludb; hostname = 125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; port = 30426; uid = ksy13207; password = Z5tm8KPtdC4hpoaL; security = SSL; sslcertificate = DigiCertGlobalRootCA.crt", " ", " ")
print("connection done")

app=Flask(__name__)

@app.route('/' , methods=["GET","POST"])
def home():
    return render_template('homepage.html')

@app.route('/register' , methods=["GET","POST"])
def register():
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
            print("username already exists")
        else :
            query= "select * from registeration where emailid= ?"         
            stmt = ibm_db.prepare(conn,query)
            ibm_db.bind_param(stmt,1,emailid)
            ibm_db.execute(stmt) 
            details=ibm_db.fetch_assoc(stmt)               
            if details:
                print("emailid have already been used")
            else :
                query="insert into registeration values(?,?,?)"
                stmt = ibm_db.prepare(conn,query)                                
                ibm_db.bind_param(stmt,1,user)
                ibm_db.bind_param(stmt,2,emailid)
                ibm_db.bind_param(stmt,3,password)
                ibm_db.execute(stmt)
                return redirect('/login')   
    return render_template('register.html')



@app.route('/login' , methods=["GET","POST"])
def login():
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
            return redirect('/')
        else:
            print("username doesn't exist,please login")
            return redirect('/login')
    return render_template("login.html")



@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__" :
    app.run(debug = True)
