from flask import Flask, render_template,request
import pyodbc
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  #POST for submiting data ,GET for www.localhost.com
def handleDuesForm():
    if request.method == 'POST':
        m_ID = request.form['num']
        m_ID =int(m_ID)  # Data intergrity
        F_n = request.form['nm']
        F_n  =F_n.upper().strip()  # Data intergrity
        S_n = request.form['snm']
        S_n = S_n.upper().strip() # Data intergrity
        Mon = request.form['pay']
        Mon = int(Mon)
        mnth = request.form['mn']
        yer = request.form['yr']


        connection_str = ("Driver={ODBC Driver 11 for SQL Server};"
                              "Server=DESKTOP-CQQ2V0L\SQLEXPRESS;"
                              "Database=YCP;"
                              "Trusted_Connection=yes;")
        connection = pyodbc.connect(connection_str)

        ################  check duplicates  surname and month
        query1 = 'SELECT * FROM DUES'
        df = pd.read_sql(query1,connection)
        check_id = df['Memberid'].values.tolist()
        check_month = df['month'].values.tolist()
        if (m_ID in check_id and mnth in check_month):
            err_msg = 'This name has paid dues for this month.'
            return render_template("YCP_DuesForm.html", err_dup=err_msg)
        ################################
        else: # no duplicate
            cursor = connection.cursor()
            query = 'Insert into Dues Values (?,?,?,?,?,?)'
            cursor.execute(query,m_ID,F_n,S_n,Mon,mnth,yer)
            connection.commit()
            connection.close()
            return render_template('YCP_feedback.html', Fnm=F_n, Fsnm=S_n, fmnth = mnth)
    if request.method == 'GET': #display this page for user - GET HTTP,  if form has not been  filled and submitted
        return render_template("YCP_DuesForm.html")


########   check membership dues
@app.route('/check')  # Get method
def handleCheckDues():

        connection_str = ("Driver={ODBC Driver 11 for SQL Server};"
                          "Server=DESKTOP-CQQ2V0L\SQLEXPRESS;"
                          "Database=YCP;"
                          "Trusted_Connection=yes;")
        connection = pyodbc.connect(connection_str)

        query2 = "SELECT * FROM DUES"
        readfile = pd.read_sql(query2, connection)

        file_html = readfile.to_html()  #dataframe to HTML
        # connection.close()
        return render_template("YCPshowDues.html", record=file_html)


#delete records in registered users
@app.route('/check',  methods=['GET', 'POST'])
def handleDelete():
    if request.method == 'POST':
        id = request.form['num']
        id = int(id) # Data intergrity
        mnth = request.form['mn']
        password = request.form['pass']

        if password == 'SECRET':
            connection_str = ("Driver={ODBC Driver 11 for SQL Server};"
                              "Server=DESKTOP-CQQ2V0L\SQLEXPRESS;"
                              "Database=YCP;"
                              "Trusted_Connection=yes;")
            connection = pyodbc.connect(connection_str)
            cursor = connection.cursor()   # create a writer or eraser
            # query3 = 'DROP INDEX (?) ON DUES'
            query3 = 'DELETE from DUES where Memberid = (?) and month = (?) '
            cursor.execute(query3, id, mnth)   # carry out data manipulation
            connection.commit()    # save changes

            query4 = 'SELECT * FROM DUES'
            df_fetch2  = pd.read_sql(query4, connection)
            filehtml2 = df_fetch2.to_html()
            return render_template("YCPshowDues.html", usersfile2=filehtml2)

        else:
            err_pass = 'invalid password'
            return render_template("YCPshowDues.html", errors_pass2=err_pass)
    # If the method is GET,render the HTML page to the user who hasn't submit any data
    if request.method == 'GET':
        return render_template("YCPshowDues.html")
#

if __name__ == '__main__':
    app.run(debug=True)

