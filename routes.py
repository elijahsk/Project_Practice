import sqlite3
from flask import Flask, render_template, request, session, \
flash, redirect, url_for
from functools import wraps
from threading import Thread
from flask.ext.mail import Message
from flask.ext.mail import Mail

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = '***@***.***'
MAIL_PASSWORD = '******'

# administrator list
ADMINS = ['song.kai@dhs.sg']

connection=sqlite3.connect("dstore.db")
cu=connection.cursor()
cu.execute("""DROP TABLE IF EXISTS merchandise""")
cu.execute("""CREATE TABLE merchandise(name VARCHAR[20],description VARCHAR[100],category VARCHAR[20],price REAL,ordering INT,pid INT)""")
cu.execute("""INSERT INTO merchandise VALUES('A4 Lecture Pad','NICE LECTURE PAD','stationery',2.60,0,0)""")
cu.execute("""INSERT INTO merchandise VALUES('7-Colour Sticky Note with Pen','NICE STICKY NOTE WITH PEN','stationery',4.20,0,1)""")
cu.execute("""INSERT INTO merchandise VALUES('A5 Exercise Book','NICE EXERCISE BOOK','stationery',2.90,0,2)""")
cu.execute("""INSERT INTO merchandise VALUES('A5 Note Book with Zip Bag','NICE NOTE BOOK WITH ZIP BAG','stationery',4.60,0,3)""")
cu.execute("""INSERT INTO merchandise VALUES('2B Pencil','NICE PENCIL','stationery',0.90,0,4)""")
cu.execute("""INSERT INTO merchandise VALUES('Stainless Steel Tumbler','NICE TUMBLER','stationery',12.90,0,5)""")
cu.execute("""INSERT INTO merchandise VALUES('A4 Clear Holder','NICE HOLDER','stationery',4.40,0,6)""")
cu.execute("""INSERT INTO merchandise VALUES('A4 Vanguard File','NICE FILE','stationery',1.00,0,7)""")
cu.execute("""INSERT INTO merchandise VALUES('Name Card Holder','NICE HOLDER','others',10.90,0,8)""")
cu.execute("""INSERT INTO merchandise VALUES('Umbrella','NICE UMBRELLA','others',9.00,0,9)""")
cu.execute("""INSERT INTO merchandise VALUES('School Badge (Junior High)','NICE BADGE','badges',1.30,0,10)""")
cu.execute("""INSERT INTO merchandise VALUES('School Badge (Senior High)','NICE BADGE','badges',1.80,0,11)""")
cu.execute("""INSERT INTO merchandise VALUES('Dunman Dolls (Pair)','NICE DOLLS','special',45.00,0,12)""")

cu.execute("""DROP TABLE IF EXISTS user""")
cu.execute("""CREATE TABLE user(username VCHAR[20],password VCHAR[20],uid INT,authority INT,email VCHAR[100])""")
cu.execute("""INSERT INTO user VALUES('******','******',0,0,'***@***.***')""")

cu.execute("""DROP TABLE IF EXISTS orders""")
cu.execute("""CREATE TABLE orders(uid INT,oid INT,time DATETIME,status INT,item0 INT,item1 INT,item2 INT,item3 INT,item4 INT,item5 INT,item6 INT,item7 INT,item8 INT,item9 INT,item10 INT,item11 INT,item12 INT,paid INT)""")

connection.commit()
connection.close()



from flask import *
import datetime
import hashlib

DATABASE='dstore.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'my precious'

user=-1

def hashstr(string):
	temp=hashlib.sha256()
	temp.update(string)
	return temp.digest()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


#Using new thred to send email asynchronously
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper



@app.route('/')
def main():
    title='MainPage'
    if 'username' in session:
        user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
        return render_template('main.html',title=title,username=session['username'],user=user)
    else:
        return render_template('main.html',title=title,username='')

@app.route('/login',methods=['GET','POST'])
def login():
    title='Login'
    error=None
    if request.method=='POST':
        cur=connect_db().execute('SELECT password FROM user WHERE username=:1',(request.form['username'],))
        temp=cur.fetchone()
        if not temp:
            error='No such user'
        elif hashstring(request.form['password'])!=temp[0]:
            error='Wrong Password'
        else:
            session['logged_in']=True
            session['username']=request.form['username']
            session['user']=int(connect_db().execute('SELECT uid FROM user WHERE username=:1',(request.form['username'],)).fetchone()[0])
            return redirect(url_for('success'))
    if 'username' in session:
        return render_template('login.html',title=title,username=session['username'],error=error,user=user)
    else:
        return render_template('login.html',title=title,username='',error=error)



@app.route('/signup',methods=['GET','POST'])
def signup():
    title='Sign Up!'
    error1=None
    error2=None
    error3=None
    if request.method=='POST':
        cur=connect_db().execute('SELECT username FROM user WHERE username=:1',(request.form['username'],))
        if cur.fetchone():
            error1='Username already exists!'
            error2=None
            error3=None
        elif len(request.form['username'])<2:
            error1='Keep your username at least 2 characters!'
            error2=None
            error3=None
        elif len(request.form['username'])>20:
            error1='Keep your username shorter than 20 characters!'
            error2=None
            error3=None
        elif len(request.form['password'])<6:
            error2='Password at least 6 characters!'
            error1=None
            error3=None
        elif not request.form['password']==request.form['cpassword']:
            error1=None
            error2='Two password not the same!'
            error3=None
        elif not ('@' in request.form['email']):
            error1=None
            error2=None
            error3='Invalid email!'
        elif not ('.' in request.form['email']):
            error1=None
            error2=None
            error3='Invalid email!'
        else:
            g=connect_db()
            cu=g.cursor()
            num=len(connect_db().execute("""SELECT * FROM user""").fetchall())
            cur=cu.execute('INSERT INTO user VALUES(?,?,?,1,?)',
                           (request.form['username'],
                            hashstring(request.form['password']),
                            num,
                            request.form['email'],)
                           )

            g.commit()
            return redirect(url_for('successs'))
    if 'username' in session:
        return render_template('signup.html',title=title,username=session['username'],error1=error1,error2=error2,error3=error3,user=user)
    else:
        return render_template('signup.html',title=title,username='',error1=error1,error2=error2,error3=error3)

@app.route('/successs')
def successs():
    title='Sign up Successfully'
    return render_template('successs.html',title=title,username='')


@app.route('/success')
@login_required
def success():
    user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
    title='Log in Successfully'
    return render_template('success.html',title=title,username=session['username'],user=user)


@app.route('/allitems')
def allitems():

    title='allitems'
    cur=[]
    cur=connect_db().execute('SELECT * FROM merchandise').fetchall()
    for item in cur:
        item=str(item)
    l=len(cur)
    if 'username' in session:
        user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
        return render_template('viewall.html',title=title,username=session['username'],l=l,cur=cur,user=user)
    else:
        return render_template('viewall.html',title=title,username='',l=l,cur=cur)

@app.route('/stationery')
def stationery():
    title='Stationery'
    cur=connect_db().execute("""SELECT * FROM merchandise WHERE category='stationery'""").fetchall()
    for item in cur:
        item=str(item)
    l=len(cur)
    if 'username' in session:
        user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
        return render_template('stationery.html',title=title,username=session['username'],l=l,cur=cur,user=user)
    else:
        return render_template('stationery.html',title=title,username='',l=l,cur=cur)

@app.route('/badges')
def badges():
    title='Badges'
    cur=connect_db().execute("""SELECT * FROM merchandise WHERE category='badges'""").fetchall()
    for item in cur:
        item=str(item)
    l=len(cur)
    if 'username' in session:
        user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
        return render_template('badges.html',title=title,username=session['username'],l=l,cur=cur,user=user)
    else:
        return render_template('badges.html',title=title,username='',l=l,cur=cur)

@app.route('/others')
def others():
    title='others'
    cur=connect_db().execute("""SELECT * FROM merchandise WHERE category='others'""").fetchall()
    for item in cur:
        item=str(item)
    l=len(cur)
    if 'username' in session:
        user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
        return render_template('others.html',title=title,username=session['username'],l=l,cur=cur,user=user)
    else:
        return render_template('others.html',title=title,username='',l=l,cur=cur)


@app.route('/special')
def special():

    title='special'
    cur=connect_db().execute("""SELECT * FROM merchandise WHERE category='special' """).fetchall()
    for item in cur:
        item=str(item)
    l=len(cur)
    if 'username' in session:
        user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
        return render_template('special.html',title=title,username=session['username'],l=l,cur=cur,user=user)
    else:
        return render_template('special.html',title=title,username='',l=l,cur=cur)


@app.route('/view/<int:pid>',methods=['GET','POST'])
def view(pid):

    title='Single Items'
    message=None
    cur=connect_db().execute("""SELECT * FROM merchandise WHERE pid=:1""",(str(pid),)).fetchone()
    if request.method=='POST':
        if 'username' in session:
            user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
            t=[0,0,0,0,0,0,0,0,0,0,0,0,0]
            if not request.form['amount'+str(pid)].isdigit():
                flash('You must enter a positive integer!')
                return redirect(url_for('view',pid=pid))
            if (request.form['amount'+str(pid)].isdigit()) and (int(request.form['amount'+str(pid)])==0):
                flash('You must enter a positive integer!')
                return redirect(url_for('view',pid=pid))

            t[pid]=request.form['amount'+str(pid)]
            num=connect_db().execute("""SELECT * FROM orders ORDER BY time DESC""").fetchall()
            if num:
                num=num[0][1]+1
                if len(connect_db().execute("""SELECT * FROM orders WHERE uid=:1 ORDER BY time DESC""",(str(user),)).fetchall())!=0:
                    if connect_db().execute("""SELECT * FROM orders WHERE uid=:1 ORDER BY time DESC""",(str(user),)).fetchall()[0][3]==1:
                        num=connect_db().execute("""SELECT * FROM orders WHERE uid=:1 ORDER BY time DESC""",(str(user),)).fetchall()[0][1]
            else:
                num=0
            g=connect_db()
            cu=g.cursor()
            cur=cu.execute("""INSERT INTO orders VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                     (user,
                                      num,
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),1,
                                      t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10],t[11],t[12],0))
            g.commit()
            return redirect(url_for('allitems'))
        else:
            return redirect(url_for('login'))
    if 'username' in session:
        user=int(connect_db().cursor().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
        return render_template('viewsingle.html',title=title,username=session['username'],cur=cur,user=user)
    else:
        return render_template('viewsingle.html',title=title,username='',cur=cur)


@app.route('/viewallorder/<int:uid>')
@login_required
def viewallorder(uid):
    user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
    if user==0 or user==uid:
        title='All Orders'
        ausername=connect_db().execute('SELECT username FROM user WHERE uid=:1',(str(uid),)).fetchone()[0]
        cur=connect_db().execute("""SELECT * FROM orders WHERE uid=:1""",(str(uid),)).fetchall()
        cur2=connect_db().execute("""SELECT * FROM merchandise ORDER BY pid ASC""").fetchall()
        return render_template('allorders.html',title=title,cur=cur,cur2=cur2,username=session['username'],ausername=ausername,user=user)
    else:
        return redirect(url_for('login'))

@app.route('/dele/<int:oid>')
@login_required
def dele(oid):
    user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
    if (user==0) or (user==int(connect_db().execute("""SELECT uid FROM orders WHERE oid=:1""",(str(oid),)).fetchone()[0])):
        uid=int(connect_db().execute("""SELECT uid FROM orders WHERE oid=:1""",(str(oid),)).fetchone()[0])
        g=connect_db()
        cur=g.cursor().execute("""DELETE FROM orders WHERE oid=:1""",(str(oid),))
        g.commit()
        return redirect(url_for('viewallorder',uid=uid))
    else:
        flash('You are not authorized to view other order from others')
        return redirect(url_for('login'))


@app.route('/finishorder')
@login_required
def finishorder():
    user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
    cur=connect_db().execute("""SELECT * FROM orders WHERE uid==:1 ORDER BY time DESC""",(str(user),)).fetchall()
    if len(cur)!=0:
        cur=cur[0][1]
        g=connect_db()
        cur2=g.cursor().execute("""UPDATE orders SET status=0 WHERE oid=:1""",(str(cur,)))
        g.commit()
    return redirect(url_for('viewallorder',uid=user))

@app.route('/pay/<int:oid>')
@login_required
def pay(oid):
    title='Pay for It'
    cur=connect_db().execute("""SELECT * FROM orders WHERE oid=:1""",(str(oid),)).fetchall()
    cur2=connect_db().execute("""SELECT * FROM merchandise""").fetchall()
    paid=cur[0][-1]
    t=[0,0,0,0,0,0,0,0,0,0,0,0,0]
    for order in cur:
        for i in range(4,17):
            t[i-4]+=int(order[i])
    price=0
    for i in range(0,13):
        price+=t[i]*cur2[i][3]
    user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
    return render_template('pay.html',title=title,cur2=cur2,t=t,price=price,oid=oid,username=session['username'],paid=paid,user=user)

@app.route('/paid/<int:oid>')
@login_required
def paid(oid):
    user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
    uid=int(connect_db().execute("""SELECT uid FROM orders WHERE oid=:1""",(str(oid),)).fetchone()[0])
    if (user!=uid):
        flash('You have no authority to make that change')
        return redirct(url_for('viewallorders'),uid=user)
    g=connect_db()
    cur=g.cursor().execute("""SELECT * FROM orders WHERE oid=:1""",(str(oid,))).fetchall()
    cur2=g.cursor().execute("""SELECT * FROM merchandise""").fetchall()
    t=[]
    for item in cur2:
        t.append(item[4])
    for item in cur:
        for i in range(4,17):
            t[i-4]+=item[i]
    for i in range(0,13):
        g=connect_db()
        cur=g.cursor().execute("""UPDATE merchandise SET ordering=:1 WHERE pid=:2""",(t[i],i,))
        g.commit()
    g=connect_db()
    cur=g.cursor().execute("""UPDATE orders SET paid=1 WHERE oid=:1""",(str(oid,)))
    g.commit()
    g=connect_db()
    cur2=g.cursor().execute("""UPDATE orders SET status=0 WHERE oid=:1""",(str(oid,)))
    g.commit()

    return redirect(url_for('mail'))

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in',None)
    session.pop('username', None)
    return redirect(url_for('logoutsuccess'))

@app.route('/contact')
def contact():
    title='Contact Us!'
    if 'username' in session:
        user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
        return render_template('contact.html',title=title,username=session['username'],user=user)
    else:
        return render_template('contact.html',title=title,username='')


@app.route('/credit/<int:oid>',methods=['GET','POST'])
@login_required
def credit(oid):
    title='Credit Card Info'
    user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
    if request.method=='POST':
        return redirect(url_for('paid',oid=oid))
    return render_template('credit.html',title=title,username=session['username'],user=user,oid=oid)


@app.route('/logoutsuccess')
def logoutsuccess():
    title='Log Out Successfully'
    return render_template('successss.html', title=title,username='')

@app.route('/search',methods=['GET','POST'])
@login_required
def search():
    title='Search'
    user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
    if not user==0:
        flash('You are not authorized of using this function hahahahaha!')
        return redirect(url_for('login'))
    cur=[]
    if request.method=='POST':
        key=request.form['search'].lower()
        cu=connect_db().execute("""SELECT * FROM user ORDER BY uid ASC""").fetchall()
        for users in cu:
            if key in users[0].lower():
                cur.append(users)
    return render_template('search.html',title=title,username=session['username'],cur=cur,user=user)

@app.route('/delete/<int:uid>')
@login_required
def delete(uid):
    if not session['username']=='adminsk':
        flash('You are not authorized of using this function hahahahahaha!')
        return redirect(url_for('login'))
    g=connect_db()
    cur=g.cursor().execute('DELETE FROM user WHERE uid =:1',(str(uid),))
    g.commit()
    g=connect_db()
    cur=g.cursor().execute('DELETE FROM orders WHERE uid =:1',(str(uid),))
    g.commit()
    return redirect(url_for('search'))

@async
def send_async_email(msg):
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)

@app.route('/mail',methods=['GET', 'POST'])
@login_required
def mail():
        title='Send Emails'
        user=int(connect_db().execute("""SELECT uid FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
	email1=str(connect_db().execute("""SELECT email FROM user WHERE username=:1""",(session['username'],)).fetchone()[0])
	email2=str(connect_db().execute("""SELECT email FROM user WHERE uid=0""").fetchone()[0])
	mailtext1 ="""Dear """+session['username']+""":
            Thank you for doing purchase at DHS Souvenirs!
            Check for more detailed information at http://elijahsk.pythonanywhere.com

        Warmest Regards,
        DHS Souvenirs"""
	mailtext2="""Dear shop owner:
            We are pleased to inform you that a customer has made a purchase at DHS Souvenirs!
            Check for more detailed information at http://elijahsk.pythonanywhere.com
        Warmest Regardsm
        DHS Souvenirs"""
	send_email('DHSouvenir Order', ADMINS[0], email1, mailtext1, mailtext1)
	send_email('DHSouvenir Order', ADMINS[0], email2, mailtext2, mailtext2)
	return render_template('mail.html',title=title,username=session['username'],user=user)


if __name__ == '__main__':
    app.run(debug=True)
