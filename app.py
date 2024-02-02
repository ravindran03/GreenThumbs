from flask import Flask,render_template,request,redirect,session,url_for,render_template_string
import ibm_db
import ibm_boto3
from ibm_botocore.client import ClientError,Config


conn =  ibm_db.connect("database = ; hostname = ; port = ; uid = ; password = ; security = ; sslcertificate = ", " ", " ")
print("connection done")

app=Flask(__name__)
app.secret_key = "forreal"

@app.route('/')
def home():
    user=session.get('user')
    if user:
        return render_template('homepage.html',detpro=user)
    else:
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
    user=session.get('user')
    if user:
        query= "select * from registeration where username= ?"         
        stmt = ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,user)
        ibm_db.execute(stmt) 
        details=ibm_db.fetch_assoc(stmt)
        print(details)
        msg="welcome"+session['user']

        list=[]
        query= "select * from enroll where username= ?"         
        stmt = ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,user)
        ibm_db.execute(stmt) 
        details1=ibm_db.fetch_assoc(stmt)
        print(details1)
        while details1:
            list.append(details1)
            details1=ibm_db.fetch_assoc(stmt)
            if not details:
                break
        msg="welcome"+session['user']
        return render_template('profile.html',msg=msg,detpro=user,details=details,details1=list)
    else:
        return render_template('profile.html',msg="login to view your profile")

   
@app.route('/guides',methods=['GET','POST'])
def guides():
    if request.method=='POST':
        pname=request.form['pname']
        print(pname)
        return redirect(url_for('aboutplant',pname=pname))
    
    plist=[]
    query="select pname from guide"     
    stmt=ibm_db.prepare(conn,query)
    ibm_db.execute(stmt)
    pnames=ibm_db.fetch_tuple(stmt)
    while pnames:
        plist.append(pnames[0])
        pnames=ibm_db.fetch_tuple(stmt)
    user=session.get('user')
    if user:
        return render_template('guides.html',plist=plist,detpro=user)
    else:    
        print(plist)    
        return render_template("guides.html",plist=plist)


@app.route('/guides/<pname>')
def aboutplant(pname):
    query="select * from guide where pname=?"
    stmt=ibm_db.prepare(conn,query)
    ibm_db.bind_param(stmt,1,pname)
    ibm_db.execute(stmt)
    details=ibm_db.fetch_assoc(stmt)

    variable="""<center><div class="plant-info">
        <h1>Information</h1>
        <img src="https://potplants.s3.us-south.cloud-object-storage.appdomain.cloud/{{details['PMAGE']}}" alt="{{details['PMAGE']}}">
        <h2>Scientific Name:</h2>
        <p>{{ details['SCIENTIFIC_NAME'] }}</p>
        <h2>Common Name:</h2>
        <p>{{ details['PNAME'] }}</p>
        <h2>Preferred Light:</h2>
        <p>{{ details['PREFERRED_LIGHT'] }}</p>
        <h2>Preferred Soil:</h2>
        <p>{{ details['PREFERRED_SOIL'] }}</p>
        <h2>Watering Needs:</h2>
        <p>{{ details['WATERING_NEEDS'] }}</p>
    </div></center>"""
    
    return render_template_string(variable,details=details)


@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if request.method == 'POST':
        user = request.form['user_name']
        pw=request.form["pass_word"]
        list=[user,pw]
        print(list)
        
        query="select * from admin where username= ? and password= ?"
        stmt=ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,user)
        ibm_db.bind_param(stmt,2,pw)
        ibm_db.execute(stmt)
        details=ibm_db.fetch_assoc(stmt)
        if details:
            session['user']=details['USERNAME']
            # session['user']=details['USERNAME']
            return redirect('/shop')
    return render_template('adminlogin.html')
    

@app.route('/shop',methods=['GET','POST'])
def shop():
    if request.method=='POST':
        pname=request.form['pname']
        pid=request.form['pid']
        price=request.form['price']
        pimage=request.files['pimage']
        filename=pimage.filename
        result=cosupload(pimage)
        # pimage.save(iname) #used to save the object locally
                
        if result:
            query="insert into plant values(?,?,?,?)"
            stmt=ibm_db.prepare(conn,query)
            ibm_db.bind_param(stmt,1,pname)
            ibm_db.bind_param(stmt,2,pid)
            ibm_db.bind_param(stmt,3,price)
            ibm_db.bind_param(stmt,4,filename)            
            # print(type(pname))
            ibm_db.execute(stmt)        
            msg='''<h2>new plant added succesfully<h2><p>to add another plant <a href="/shop" >go to shop</a></p><p>to view added plant <a href="/plants" >go to plants</a></p>'''
            return msg
    user=session.get('user')
    if user:
        return render_template("shop.html",detpro=user)
    else:
        return redirect('/adminlogin')


#cloud object storage
def cosupload(image):    
    COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
    COS_API_KEY_ID = "t6P4mXYo0f_17TLletzv35JHnKmziHnzL7NNo57ARTbi"
    COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/22999e2d442a4ba698829ce83834117e:79083486-d8ef-4dc5-bc2a-5c251b09e844:bucket:potplants" 
    cos = ibm_boto3.client("s3", ibm_api_key_id = COS_API_KEY_ID , ibm_service_instance_id = COS_INSTANCE_CRN , endpoint_url = COS_ENDPOINT, config = Config(signature_version='oauth'))
    cos.upload_fileobj(image, Bucket = "potplants", Key = image.filename )
    #upload_fileobj(file,bucket,objectname)
    print("file uploaded")
    return True



@app.route('/plants')
def plants():
    user=session.get('user')

    plants=[]
    query="select * from plant "
    stmt=ibm_db.prepare(conn,query)
    ibm_db.execute(stmt)
    details=ibm_db.fetch_assoc(stmt)    
    while details:
        plants.append(details)
        details=ibm_db.fetch_assoc(stmt)
    
    if user:
        return render_template('plants.html',detpro=user,list=plants)
    
    return render_template('plants.html',list=plants)


@app.route('/buy',methods=['POST','GET'])
def buy():
    user=session.get('user')
    if user and request.method == 'POST':
       
        pname = request.form['pname']
        pid = request.form['pid']
        list=[pname,pid]
        print(list)
        query = "insert into enroll values(?,?,?)"
        stmt=ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,user)   
        ibm_db.bind_param(stmt,2,pid)
        ibm_db.bind_param(stmt,3,pname)                   
        ibm_db.execute(stmt)        
        return '''<center><h2>you are enrolled<h2><p>go to your <a  href="/profile">profile</a>to view details of the enrolled plants</p>we will notify you when the enrolled guide is available<p>to further enroll go <a  href="/plants">back</a></p><center>'''
    else :
        return '''<center><h2>login to enroll <a href="/login" >login here</a><h2><center>'''
    
        
@app.route('/logout')
def logout():
    session.pop('user',None)
    # flash="logged out successfully"
    return redirect('/')


    

if __name__ == "__main__" :
    app.run(debug = True)
