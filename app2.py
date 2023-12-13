# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from blockchain import Blockchain
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# Dummy user class. Replace this with your actual User model.
class User():
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

# Simulate a user with username 'admin' and password 'password'
users = {'admin': {'password': 'password'}}

# Replace this with your actual user loading logic.

@app.route('/index', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        private_key = request.form.get('Private Key')
        password = request.form.get('password')

        # Check if there is such a private key in the admin list
        if private_key in blockchain.Identity_admin and private_key in blockchain.Users:
            if Blockchain.check_password(password, blockchain.Users[private_key]):
                session["user"] = blockchain.Identity_admin[private_key][0]["nume"]
                return redirect(url_for('admindashboard'))
            else: 
                flash("Your password is wrong")
                return render_template('login.html')
        else:
            # Check if there is such a private key in the user list
            if private_key in blockchain.Users and private_key in blockchain.Identity_dict:
                print(blockchain.Identity_dict)
                if Blockchain.check_password(password, blockchain.Users[private_key]):
                    session["user"] = blockchain.Identity_dict[private_key][0]["name"]
                    return redirect(url_for('userPage'))
                else: 
                    flash("Your password is wrong")
                    return render_template('login.html')
            else:
                flash("There is no such Private Key in the user list")
                return render_template('login.html')
    else: 

        return render_template('login.html')



@app.route('/admindashbord')
def admindashboard():
    if "user" in session:
        user = session["user"]
        flash(f"{user}", "error")
    else:
        return redirect(url_for('login'))
    return render_template('admindashbord.html')

@app.route('/findCandidate', methods = ['GET', 'POST'])
def findCandidate():
    if "user" in session:
            user = session["user"]
            flash(f"{user}", "error")
            if request.method == 'POST':        
                # Start of the first function
                    form_values = []
                    list = {
                        'name': request.form.get('name'),  # Convert to string or handle accordingly
                        'date_of_b': request.form.get('date_of_birth'),
                        'CNP': request.form.get("CNP"),
                        'criminal_records': request.form.get("criminal_record"),
                        'nationality': request.form.get('nationality')
                    }
                    form_values.append(list)

                    # Caută în dicționar
                    for key in blockchain.Identity_dict:
                        if blockchain.Identity_dict[key] == form_values:
                            flash(key)
                        else:
                            flash("There is not a person with these description")

    else:
        return redirect(url_for('login'))
    return render_template('candidateManagement.html')

@app.route('/submitCandidate', methods = ['GET', 'POST'])
def submitCandidate():
    if "user" in session:
        user = session["user"]
        flash(f"{user}", "error")
        if request.method == 'POST':        
            name = request.form.get('submit_name')
            private_key = request.form.get('submit_private_key')
            party = request.form.get('political_party')
            picture = request.files['picture']  # Use square brackets, not parentheses

        if private_key not in blockchain.Identity_contestants:
            blockchain.Identity_contestants[private_key] = []

            # You can save the image to a specific folder or process it as needed
            # For example, save it to the 'uploads' folder
            picture_name = secure_filename(picture.filename)
            picture_path = os.path.join(os.path.join(app.root_path, 'static/uploads'), picture_name)
            picture.save(picture_path)

            blockchain.Identity_contestants[private_key].append({
                'public_key': Blockchain.generateAddress(Blockchain.generatePrivateKey()),
                'name': name,
                'party': party,
                'picture_name': picture_name,  # Save the image name
                'picture_path': picture_path  # Save the image path
            })

            flash("Candidate added")
        else:
            flash("Already existing candidate")

    else:
        return redirect(url_for('login'))
    return render_template('candidateManagement.html')

@app.route('/candidateManagement', methods = ['GET', 'POST'])
def candidateManagement():
    if "user" in session:
        user = session["user"]
        flash(f"{user}", "error")
        return render_template('candidateManagement.html')

    else:
        return redirect(url_for('login'))

@app.route('/userPage')
def userPage():
    if "user" in session:
        user = session["user"]
        flash(f"{user}", "error")
        print(blockchain.Identity_contestants)
        identity_contestants=blockchain.Identity_contestants
        for key, contestants in identity_contestants.items():
            # Iterați prin fiecare element din lista asociată cu cheia
            for contestant in contestants:
                # Atribuiți variabilelor valorile corespunzătoare
                name = contestant['name']
                public_key = contestant['public_key']
                party = contestant['party']
                picture_path = contestant['picture_path']
                picture_name = contestant['picture_name']

                # Puteți folosi aceste variabile aici sau le puteți stoca în alt mod, de exemplu, într-o listă sau altă structură de date
                print(f"Name: {name}, Public Key: {public_key}, Party: {party}, Picture_path: {picture_path}, Picture_name: {picture_name}")





    else:
        return redirect(url_for('login'))
    return render_template('userPage.html', identity_contestants=blockchain.Identity_contestants)

@app.route('/create_account', methods=['GET', 'POST'])
def create_accout():
    if request.method == 'POST':
        private_key = request.form.get('private_key')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm_password')
        # Verifică dacă cheia privată este deja în uz
        if private_key not in blockchain.Identity_dict and private_key not in blockchain.Identity_admin:
            print(blockchain.Identity_dict)
            print(blockchain.Identity_admin)
            flash("The Private Key is wrong", "error")
            return render_template('create.html')
        
        # Verifică dacă parola este prea scurtă
        if len(password) < 10:
            flash("Password is too short, please enter at least 10 characters", "error")
            return render_template('create.html')

        # Verifică dacă parolele corespund
        if password != confirmPassword:
            flash("Passwords do not match, check your passwords", "error")
            return render_template('create.html')

        # Dacă nu există erori, creează un cont nou
        blockchain.Users[private_key] = Blockchain.hash_password(password)  
        Blockchain.save_data(blockchain.Users, "credentials.json")
        return redirect(url_for('login'))
    
    return render_template('create.html')

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
        
    # Adaugă leaf-urile în procesul de probă de lucru
    proof = blockchain.proof_of_work(previous_proof)
    
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)