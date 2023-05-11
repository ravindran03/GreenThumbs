from flask import Flask,render_template,request,redirect,session,url_for
import ibm_db

conn =  ibm_db.connect("database = bludb; hostname = 125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; port = 30426; uid = ksy13207; password = Z5tm8KPtdC4hpoaL; security = SSL; sslcertificate = DigiCertGlobalRootCA.crt", " ", " ")
print("connection done")

app=Flask(__name__)
app.secret_key = "forreal"

@app.route('/')
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
            session['user']=details['USERNAME']
            return redirect('/')
        else:
            query="select * from registeration where username= ? "
            stmt=ibm_db.prepare(conn,query)
            ibm_db.bind_param(stmt,1,user)           
            ibm_db.execute(stmt)
            details=ibm_db.fetch_assoc(stmt)
            if details:
                msg="username and password didn't match"
            else:
               msg="username doesn't exist,please register first"            
    return render_template("login.html",msg=msg)


@app.route('/profile')
def profile():
    if session['user']:
        msg="welcome"+session['user']
        return render_template('profile.html',user=session['user'],msg=msg,visibility='hidden')
    else:
        return render_template('profile.html',msg="login to view your profile")
    
@app.route('/guides',methods=['GET','POST'])
def guides():
    if request.method=='POST':
        pname=request.form['pname']
        return redirect(url_for('aboutplant',pname=pname))
    
    plist=[]
    query="select pname from plant"     #guide table
    stmt=ibm_db.prepare(conn,query)
    ibm_db.execute(stmt)
    pnames=ibm_db.fetch_tuple(stmt)
    while pnames:
        plist.append(pnames[0])
        pnames=ibm_db.fetch_tuple(stmt)
        
    print(plist)

    
    return render_template("guides.html",plist=plist)

@app.route('/plants',methods=['GET','POST'])
def plants():
    if request.method=='POST':
        pname=request.form['pname']
        pid=request.form['pid']
        price=request.form['price']
        query="insert into plant values(?,?,?)"
        stmt=ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,pname)
        ibm_db.bind_param(stmt,2,pid)
        ibm_db.bind_param(stmt,3,price)
        ibm_db.execute(stmt)
        msg="new plant added succesfully"
        return msg
        






    return render_template("plants.html")

@app.route('/logout')
def logout():
    session.pop('user',None)
    # flash="logged out successfully"
    return redirect('/')

@app.route('/guides/<pname>')
def aboutplant(pname):
    query="select * from guide where pname=?"
    stmt=ibm_db.prepare(conn,query)
    ibm_db.bind_param(stmt,1,pname)
    ibm_db.execute(stmt)
    details=ibm_db.fetch_assoc(stmt)
    print(type(details))
    return str(details)


#we still have to work on shop to display the plants for buying p.s=tablename =plant


if __name__ == "__main__" :
    app.run(debug = True)
