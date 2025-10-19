from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "jothika"

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="loan_project"
)

@app.route('/')
def register():
    return render_template("register.html")

@app.route('/submit', methods=['POST'])
def register_details():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phone_no = request.form['phone_no']
    role=request.form['role']
    
    cursor = db.cursor()
    insert_query = "INSERT INTO register(username, password, email, phone_no, status,role) VALUES (%s, %s, %s, %s, %s,%s)"
    values = (username, password, email, phone_no, "Active",role)
    cursor.execute(insert_query, values)
    db.commit()
    cursor.close()

    return redirect('/login')

@app.route('/login', methods=["GET", "POST"])  
def login_details():  
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        query = "SELECT * FROM register WHERE username=%s AND password=%s AND status=%s"
        values = (username, password, "Active")
        cursor.execute(query, values)
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[2]
            session['role']=user[1]
        
            if user[1]==1:
               return redirect('/user_dasbord')
            else:
                 return redirect('/dasbord')
        else:
            return "<h2>Login failed. <a href='/login'>Try again</a></h2>"
    
    return render_template("login.html")

@app.route('/dasbord')
def dasbord():
    if 'user_id' in session:
        cursor=db.cursor()
        query="SELECT*FROM loans"
        cursor.execute(query)
        data=cursor.fetchall()
        cursor.close()

        return render_template("dasbord.html",data=data)
    else:
        return redirect('/login')

@app.route('/user_dasbord')
def user_dasbord():

    id=session['user_id']
    cursor=db.cursor()
    query="SELECT*FROM loans where user_id=%s"
    value=(id,)
    cursor.execute(query,value)
    data=cursor.fetchall()
    cursor.close()
    return render_template("user_dasbord.html",data=data)
    


@app.route('/edit/<id>')   
def edit_loan(id):
    cursor=db.cursor()
    query="SELECT*FROM loans WHERE id=%s "
    value=(id,)
    cursor.execute(query,value)
    data=cursor.fetchone()
    cursor.close()

    return render_template('edit_loan.html',data=data)

@app.route('/user_edit/<id>')   
def user_edit_loan(id):
    cursor=db.cursor()
    query="SELECT*FROM loans WHERE id=%s "
    value=(id,)
    cursor.execute(query,value)
    data=cursor.fetchone()
    cursor.close()

    return render_template('edit_loan.html',data=data)

@app.route('/edit_loan/<id>' , methods=['POST'])
def edit_loan_details(id):
    loan_type = request.form['loan_type']
    amount = request.form['amount']
    duration = request.form['duration']
    employment_status = request.form['employment_status']
    income = request.form['income']
    print(id,loan_type ,amount,duration,employment_status,income)
    cursor=db.cursor()
    query="update loans set loan_type=%s,amount=%s,duration=%s,employment_status=%s,income=%s WHERE id=%s "
    values=(loan_type,amount,duration,employment_status,income,id)
    cursor.execute(query,values)
    db.commit()
    cursor.close()
    return redirect('/dasbord')





@app.route('/user_edit_loan/<id>' , methods=['POST'])
def user_edit_loan_details(id):
    loan_type = request.form['loan_type']
    amount = request.form['amount']
    duration = request.form['duration']
    employment_status = request.form['employment_status']
    income = request.form['income']
   
    cursor=db.cursor()
    query="update loans set loan_type=%s,amount=%s,duration=%s,employment_status=%s,income=%s WHERE id=%s "
    values=(loan_type,amount,duration,employment_status,income,id)
    cursor.execute(query,values)
    db.commit()
    cursor.close()
    return redirect('/user_dasbord')



@app.route('/delete/<id>')
def delete_loan(id):
    cursor=db.cursor()
    query="update loans set status='DEACTIVATE' WHERE id=%s"
    value=(id,)
    cursor.execute(query,value)  
    data=cursor.fetchone()  
    cursor.close()

    return redirect('/dasbord')

@app.route('/active/<id>')    
def active_loan(id):
    cursor=db.cursor()
    query="update loans set status='ACTIVE' WHERE id=%s"
    value=(id,)
    cursor.execute(query,value)  
    data=cursor.fetchone()  
    cursor.close()

    return redirect('/dasbord')

@app.route('/user_delete/<id>')
def user_delete_loan(id):
    cursor=db.cursor()
    query="update loans set status='DEACTIVATE' WHERE id=%s"
    value=(id,)
    cursor.execute(query,value)  
    data=cursor.fetchone()  
    cursor.close()

    return redirect('/user_dasbord')

@app.route('/user_active/<id>')    
def user_active_loan(id):
    cursor=db.cursor()
    query="update loans set status='ACTIVE' WHERE id=%s"
    value=(id,)
    cursor.execute(query,value)  
    data=cursor.fetchone()  
    cursor.close()

    return redirect('/user_dasbord')





@app.route('/pending/<id>')
def pending_loan(id):
    cursor=db.cursor()
    query="update loans set application_status='Approve' WHERE id=%s"
    value=(id,)
    cursor.execute(query,value)  
    db.commit()  
    cursor.close()
    return redirect('/dasbord')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_details'))


@app.route('/apply_loan')
def apply_loan():
    return render_template("apply_loan.html")

@app.route('/submit_loan',methods =['POST', 'GET'])
def apply_loan_details():

    if request.method == 'POST':
        user_id=session['user_id']
        loan_type=request.form['loan_type']
        amount=request.form['amount']
        duration=request.form['duration']
        employment_status=request.form['employment_status']
        income=request.form['income']

        cursor=db.cursor()
        apply_query = "INSERT INTO loans(loan_type,amount,duration,employment_status,income,status,user_id,application_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(loan_type,amount,duration,employment_status,income,"ACTIVE",user_id,"Pending")
        cursor.execute(apply_query, values)
        db.commit()
        cursor.close()
        return redirect('/user_dasbord')



if __name__ == "__main__":
    app.run(debug=True)