{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "c5373553",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'flask_mysqldb'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[1], line 2\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mflask\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m Flask, render_template, request, redirect, url_for, session\n\u001b[1;32m----> 2\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mflask_mysqldb\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m MySQL\n\u001b[0;32m      3\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mMySQLdb\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mcursors\u001b[39;00m\n\u001b[0;32m      4\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mre\u001b[39;00m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'flask_mysqldb'"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, request, redirect, url_for, session\n",
    "from flask_mysqldb import MySQL\n",
    "import MySQLdb.cursors\n",
    "import re\n",
    " \n",
    " \n",
    "app = Flask(__name__)\n",
    " \n",
    " \n",
    "app.secret_key = 'secret_key'\n",
    " \n",
    "app.config['MYSQL_HOST'] = 'localhost'\n",
    "app.config['MYSQL_USER'] = 'root'\n",
    "app.config['MYSQL_PASSWORD'] = 'your password'\n",
    "app.config['MYSQL_DB'] = 'ryanlogin'\n",
    " \n",
    "mysql = MySQL(app)\n",
    " \n",
    "@app.route('/')\n",
    "@app.route('/login', methods =['GET', 'POST'])\n",
    "def login():\n",
    "    msg = ''\n",
    "    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:\n",
    "        username = request.form['username']\n",
    "        password = request.form['password']\n",
    "        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)\n",
    "        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))\n",
    "        account = cursor.fetchone()\n",
    "        if account:\n",
    "            session['loggedin'] = True\n",
    "            session['id'] = account['id']\n",
    "            session['username'] = account['username']\n",
    "            msg = 'Logged in successfully !'\n",
    "            return render_template('index.html', msg = msg)\n",
    "        else:\n",
    "            msg = 'Incorrect username / password !'\n",
    "    return render_template('login.html', msg = msg)\n",
    " \n",
    "@app.route('/logout')\n",
    "def logout():\n",
    "    session.pop('loggedin', None)\n",
    "    session.pop('id', None)\n",
    "    session.pop('username', None)\n",
    "    return redirect(url_for('login'))\n",
    " \n",
    "@app.route('/register', methods =['GET', 'POST'])\n",
    "def register():\n",
    "    msg = ''\n",
    "    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :\n",
    "        username = request.form['username']\n",
    "        password = request.form['password']\n",
    "        email = request.form['email']\n",
    "        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)\n",
    "        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))\n",
    "        account = cursor.fetchone()\n",
    "        if account:\n",
    "            msg = 'Account already exists !'\n",
    "        elif not re.match(r'[^@]+@[^@]+\\.[^@]+', email):\n",
    "            msg = 'Invalid email address !'\n",
    "        elif not re.match(r'[A-Za-z0-9]+', username):\n",
    "            msg = 'Username must contain only characters and numbers !'\n",
    "        elif not username or not password or not email:\n",
    "            msg = 'Please fill out the form !'\n",
    "        else:\n",
    "            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))\n",
    "            mysql.connection.commit()\n",
    "            msg = 'You have successfully registered !'\n",
    "    elif request.method == 'POST':\n",
    "        msg = 'Please fill out the form !'\n",
    "    return render_template('register.html', msg = msg)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f2893e67",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
