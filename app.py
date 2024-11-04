from flask import Flask,url_for,request,render_template,session,flash,redirect, render_template, request, session, jsonify
import sqlite3
from flask_mail import Mail, Message 
from random import randint,randrange
from RSA import *

from datetime import datetime

app=Flask(__name__)
app.secret_key="Rudy"

mail=Mail(app)

print("working")
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bpt19503908@gmail.com'
app.config['MAIL_PASSWORD'] = 'ymvh jowy obrq mfap'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def random_with_N_digits(n):
            range_start = 10**(n-1)
            range_end = (10**n)-1
            return randint(range_start, range_end)

a=random_with_N_digits(4)
RecepientEmail=None
RecepientEmail="mohammedaadil1534@gmail.com"
@app.route('/',methods=["GET","POST"])
def login():
    username=None
    password=None
    err="Invalid username and password"
    if request.method=='POST':
        session['username']=request.form['uname']
        session['vid']=request.form['pwd']
        username=request.form['uname']
        password=request.form['pwd']
        conn = sqlite3.connect("reg.db")
        r=conn.cursor()
        r.execute("select name,pwd from regval2 where name=? and pwd=?",(username,password))
        rows=r.fetchall()
        if len(rows)!=0:
            for i in rows:
                if i[0]=="Admin" and i[1]=="Admin":
                    return redirect(url_for('Admin'))

                elif i[0]==username and i[1]==password:
                   
                
                    return redirect(url_for('userpage'))
                    #return render_template('user.html',username=username)
                else:
                    return render_template('login.html',err=err)
        else:
            return render_template('login.html',err=err)
    return render_template('login.html')

@app.route('/reg',methods=["GET","POST"])
def reg():
    uname=None
    pwd=None
    cpwd=None
    phn=None
    ema=None
    dob=None
    msg="Register successfully"
    if request.method=='POST':
        uname=request.form['txt']
        pwd=request.form['passw']
        cpwd=request.form['cpassw']
        phn=request.form['phn']
        ema=request.form['ema']
        RecepientEmail=ema
        print("working inside form: ", RecepientEmail)
        dob=request.form['dob']
        try:
            import sqlite3
            table_name = 'regval2'
            conn = sqlite3.connect("reg.db")
            c = conn.cursor()
            c.execute('create table if not exists ' + table_name + ' (name varchar(50),pwd varchar(50) primary key,cpwd varchar(50),phn varchar(50),ema varchar(50),dob varchar(50))')
            c.execute('insert into '+table_name+'  values (?,?,?,?,?,?)',(uname,pwd,cpwd,phn,ema,dob))
            conn.commit()
            conn.close()
            flash("Register successfully")
        except:
            return "Please enter uniq Voter ID"
        return render_template('registraion.html',msg=msg)
    else:
        return render_template('registraion.html')
    return render_template("registraion.html")

@app.route('/userpage',methods=["GET","POST"])
def userpage():
    voteid=session["vid"]
    dat=datetime.now().date()
    dat=dat.strftime("%d %b %Y")

    part=None
    vname=None
    li=[]
    che=None
    final_li=[]
    text=None
    rsalist=[]
    tupe=None
    username=None
    password=None
    # session['username']=request.form['uname']
    # session['vid']=request.form['pwd']
    # username=request.form['uname']
    # password=request.form['pwd']
    
    from block_chain import Block,BlockChain
    if request.method=='POST':
        vname=session["username"]
        li.append(vname)
        li.append(voteid)
        li.append(dat)
        part=request.form["groupOfMaterialRadios"]
        li.append(part)
        ###RSA part#################
        text=part
        p  =  generate_prime () # generates random P
        q  =  generate_prime () # generates random Q
        n  =  p * q  # compute N
        y  =  totient ( p ) # compute the totient of P
        x  =  totient ( q ) # compute the totient of Q
        totient_de_N  =  x * y  # compute the totient of N
        e  =  generate_E ( totient_de_N ) # generate E
        public_key  = ( n , e )

        print ( 'Your public key:' , public_key )
        tupe=list(public_key)
        print(tupe)
        rsalist.append(tupe)
        text_cipher  =  cipher ( text , e , n )
        print ( 'Your encrypted message:' , text_cipher )
        print(text_cipher)
        rsalist.append(text_cipher)
        d  =  calculate_private_key ( totient_de_N , e )
        print ( 'Your private key is:' , d )
        print(d)
        rsalist.append(d)
        original_text  =  decrypts ( text_cipher , n , d )
        print ( 'your original message:' , original_text )
        print(original_text)
        rsalist.append(original_text)
        table_name = 'RSA_table'
        conn = sqlite3.connect("reg.db")
        c = conn.cursor()
        c.execute('create table if not exists ' + table_name + ' (public_key varchar(50),text_cipher varchar(50),private_key varchar(50))')
        c.execute('insert into '+table_name+'  values (?,?,?)',(str(rsalist[0]),str(rsalist[1]),str(rsalist[2])))
        conn.commit()
        conn.close()
        conn=sqlite3.connect("reg.db")
        d=conn.cursor()
        d.execute("create table if not exists Rsa_table1 (public_key varchar(50),text_cipher varchar(50),private_key varchar(50),orignal_text varchar(50))")
        d.execute('insert into Rsa_table1 values(?,?,?,?)',(str(rsalist[0]),str(rsalist[1]),str(rsalist[2]),str(rsalist[3])))
        conn.commit()
        conn.close()
        # return redirect(url_for('login'))
#############################################################################################
        # #read block_chain part
        conn = sqlite3.connect("reg.db")
        g = conn.cursor()
        g.execute("select name,voterid,tstamp,party from final_block_chain")
        rows=g.fetchall()
        lii=[]
        for i in rows:
            lii.append(i)
            # print(i)
        lii.append(li)
        print(lii)

        table_name="final_block_chain"
        conn = sqlite3.connect("reg.db")
        c = conn.cursor()
        c.execute('create table if not exists ' + table_name + ' (name varchar(50),voterid varchar(50),tstamp varchar(50),party varchar(50),prevhash varchar(50),hash varchar(50))')
        for i in range(len(lii)):
            if lii[i] not in final_li:
                final_li.append(lii[i])
        # print(final_li)

        c.execute("delete from final_block_chain")
        osa=BlockChain()
        
        for i in range(len(final_li)):
            osa.addBlock(Block(final_li[i][2],final_li[i][0],final_li[i][1],final_li[i][3]))
        if request.form["otp"]==str(a):
            for b in osa.chain:
                print(b.name)
                print(b.voter_id)
                print(b.tstamp)
                print(b.party)
                print(b.prevhash)
                print(b.hash)
                c.execute('insert into '+table_name+'  values (?,?,?,?,?,?)',(b.name,b.voter_id,b.tstamp,b.party,b.prevhash,b.hash))
                import smtplib
                s = smtplib.SMTP('smtp.gmail.com: 587')
                s.starttls()
                frm='testcasep@gmail.com'
                
                # s.login("testcasep@gmail.com","project2021")
                message=str(b.party)
                # s.sendmail(frm,ema,message)
                s.quit()
            conn.commit()
            conn.close()

            return redirect(url_for('login'))
        else:       
            print("otp didn't match")
        return redirect(url_for('login'))


    elif request.method=='GET':
       
        # conn = sqlite3.connect("reg.db")
        # r=conn.cursor()
        # r.execute("select name,pwd from regval2 where name=? and pwd=?",(username,password))
        # rows=r.fetchall()
        # if len(rows)!=0:
        #     for i in rows:

        #         if i[0]==username and i[1]==password:
        #             RecepientEmail=i[4]
        #             print("Updated email" ,RecepientEmail)


        conn = sqlite3.connect("reg.db")
        che=conn.cursor()
        che.execute("select name, voterid from final_block_chain where name=? and voterid=?",(session['username'],session['vid']))
        rows=che.fetchall()
        if len(rows)!=0:
            return jsonify({'message': 'You have already voted!!!not'})
        else:
            print("woking after login: ", RecepientEmail)
            msg = Message('Hello', sender = 'bpt19503908@gmail.com', recipients = [RecepientEmail])
            msg.body = str(a)
            mail.send(msg)
            return render_template('user.html')
        return render_template('user.html')
    else:
        return render_template('user.html')
    return render_template('user.html')

@app.route('/admin',methods=["GET","POST"])
def Admin():
    admk=[]
    dmk=[]
    mnm=[]
    namt=[]
    if request.method=='GET':
        conn = sqlite3.connect("reg.db")
        g = conn.cursor()
        g.execute("select * from RSA_table")
        rows=g.fetchall()
        return render_template("admin.html",rows=rows)
    else:
        conn=sqlite3.connect("reg.db")
        h=conn.cursor()
        h.execute("select * from Rsa_table1")
        dd=h.fetchall()
        for i in dd:
            if i[3]==("['A', 'D', 'M', 'K']"):
                admk.append(i[3])
            elif i[3]==("['D', 'M', 'K']"):
                dmk.append(i[3])
            elif i[3]==("['N', 'A', 'M','T']"):
                namt.append(i[3])
            else:
                mnm.append(i[3])
        print(len(admk))
        print(len(dmk))
        print(len(namt))
        print(len(mnm))
        return render_template("admin.html",dd=dd,admkc=len(admk),dmkc=len(dmk),namtc=len(namt),mnmc=len(mnm))
    return render_template("admin.html")

if __name__=='__main__':
    app.run(debug=True)
