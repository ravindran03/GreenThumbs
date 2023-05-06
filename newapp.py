from flask import Flask,render_template,request,redirect



app=Flask(__name__)

@app.route('/' , methods=["GET","POST"])
def home():
    return render_template('homepage.html')

@app.route('/register' , methods=["GET","POST"])
def register():
    if request.method == 'POST':        
        user=request.form['username']
        id=request.form['email']
        pw=request.form['password']    
        list1=[user,id,pw]    
        print(list1)
        return redirect('/login')   
    return render_template('register.html')



@app.route('/login' , methods=["GET","POST"])
def login():
   if request.method == 'POST':
      user = request.form['user_name']
      pw=request.form["pass_word"]
      list=[user,pw]
      print(list)
      return redirect('/')
   return render_template("login.html")
@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__" :
    app.run(debug = True)
