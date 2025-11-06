from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


accounts = {}

@app.route("/")
def Home():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_account():
    accno = request.form['accno']
    name = request.form['name']
    balance = int(request.form['balance'])
    accounts[accno] = {"name": name, "balance": balance}
    return redirect(url_for("Dashboard", accno=accno))

@app.route('/dashboard/<accno>')
def Dashboard(accno):
    data = accounts[accno]
    return render_template('dashboard.html', accno=accno, data=data)

@app.route('/deposit/<accno>', methods=['POST'])
def Deposit(accno):
    amount = int(request.form['amount'])
    accounts[accno]['balance'] += amount
    return redirect(url_for('Dashboard', accno=accno))

@app.route('/withdrawn/<accno>', methods=['POST'])
def Withdrawn(accno):
    amount = int(request.form['amount'])
    if accounts[accno]['balance'] >= amount:
        accounts[accno]['balance'] -= amount
        return redirect(url_for("Dashboard", accno=accno))
    else:
        return (
            f"Requested amount is greater than current balance <br>"
            f'<a href="/dashboard/{accno}">Go Back to Dashboard</a>'
        )

@app.route('/delete/<accno>')
def Delete(accno):
    accounts.pop(accno)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
