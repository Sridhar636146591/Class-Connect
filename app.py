from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import json
import os

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey-change-in-production')

# JSON files
USERS_FILE = 'users.json'
LOST_FILE = 'lostfound.json'
EVENTS_FILE = 'events.json'
BOOK_FILE = 'bookexchange.json'
TEACHERS_FILE = 'teachers.json'
BLOOD_FILE = 'blooddonors.json'
NOTES_FILE = 'notes.json'

# --- Create files if they don't exist ---
for file in [USERS_FILE, LOST_FILE, EVENTS_FILE, BOOK_FILE, TEACHERS_FILE, BLOOD_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

if not os.path.exists(NOTES_FILE):
    initial_notes = [
        {
            "title": "🐍 Python Programming",
            "description": "Comprehensive lecture notes, syntactical reference guides, and sample codes for introductory and intermediate Python courses.",
            "file_path": "https://drive.google.com/file/d/1Bv2yW7PWDUFspMFku_KHxrPbUh9GBvdG/view?usp=drivesdk",
            "file_type": "PDF Document"
        },
        {
            "title": "🌐 Web Technology",
            "description": "Curated learning resources covering semantic HTML5, CSS3 typography transitions, client-side Javascript, and dynamic responsive site structures.",
            "file_path": "https://drive.google.com/file/d/1v-f6W3QlWl0SQgpjI8tt1_yRlmQ-FIFA/view?usp=drivesdk",
            "file_type": "PDF Document"
        },
        {
            "title": "📖 Story of an Introvert",
            "description": "A beautifully penned creative non-fiction essay exploring social dynamics, self-reflections, and unique introverted experiences on campus.",
            "file_path": "https://drive.google.com/file/d/1Xr6Yj7k-vMdjAdbrlWqWDZwkprRi2_V6/view?usp=drivesdk",
            "file_type": "PDF Document"
        }
    ]
    with open(NOTES_FILE, 'w') as f:
        json.dump(initial_notes, f, indent=2)
# --- HOME ROUTE ---
@app.route('/')
def pp():
    return redirect('/pp.html')


# --- SIGNUP ROUTE ---
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirmpassword = request.form.get('confirmpassword', '')
    gender = request.form.get('gender', '')
    classyear = request.form.get('classyear', '')
    department = request.form.get('department', '')
    bio = request.form.get('bio', '')

    if password != confirmpassword:
        return "Passwords do not match! <a href='/reg.html'>Try again</a>"

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    for user in users:
        if user['email'] == email:
            return "User already exists! <a href='/login.html'>Login</a>"

    new_user = {
        'username': username,
        'email': email,
        'password': password,
        'gender': gender,
        'classyear': classyear,
        'department': department,
        'bio': bio
    }

    users.append(new_user)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

    return "Account created successfully! <a href='/login.html'>Login Now</a>"


# --- LOGIN ROUTE ---
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    for user in users:
        if user['email'] == email and user['password'] == password:
            session['user'] = user
            return redirect('/main.html')

    return "Invalid email or password! <a href='/login.html'>Try again</a>"


# --- PROFILE ROUTE ---
@app.route('/profile.html')
def profile():
    if 'user' not in session:
        return redirect('/login.html')
    return render_template('profile.html', user=session['user'])


# --- EDIT PROFILE ROUTE ---
@app.route('/edit_profile')
def edit_profile():
    if 'user' not in session:
        return redirect('/login.html')
    return render_template('edit_profile.html', user=session['user'])


# --- UPDATE PROFILE ROUTE ---
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        return redirect('/login.html')

    email = session['user']['email']
    updated_data = {
        'username': request.form['username'],
        'email': email,
        'password': session['user']['password'],
        'gender': request.form['gender'],
        'classyear': request.form['classyear'],
        'department': request.form['department'],
        'bio': request.form['bio']
    }

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    for i, user in enumerate(users):
        if user['email'] == email:
            users[i] = updated_data
            break

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

    session['user'] = updated_data
    return redirect('/profile.html')


# --- LOST & FOUND ---
@app.route('/lostfound.html')
def lostfound():
    with open(LOST_FILE, 'r') as f:
        items = json.load(f)
    return render_template('lostfound.html', items=items)


@app.route('/add_lostfound', methods=['POST'])
def add_lostfound():
    title = request.form['title']
    description = request.form['description']
    contact = request.form['contact']

    with open(LOST_FILE, 'r') as f:
        items = json.load(f)

    items.append({
        'title': title,
        'description': description,
        'contact': contact
    })

    with open(LOST_FILE, 'w') as f:
        json.dump(items, f, indent=2)

    return redirect('/lostfound.html')


# --- EVENTS ---
@app.route('/events.html')
def events():
    with open(EVENTS_FILE, 'r') as f:
        events = json.load(f)
    return render_template('events.html', events=events)


@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form['title']
    date = request.form['date']
    description = request.form['description']
    contact = request.form['contact']

    with open(EVENTS_FILE, 'r') as f:
        events = json.load(f)

    events.append({
        'title': title,
        'date': date,
        'description': description,
        'contact': contact
    })

    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=2)

    return redirect('/events.html')


# --- DELETE EVENT ---
@app.route('/delete_event/<int:index>', methods=['POST'])
def delete_event(index):
    with open(EVENTS_FILE, 'r') as f:
        events = json.load(f)
    if 0 <= index < len(events):
        events.pop(index)
        with open(EVENTS_FILE, 'w') as f:
            json.dump(events, f, indent=2)
    return redirect('/events.html')


# --- BOOK EXCHANGE ---
@app.route('/bookexchange.html')
def bookexchange():
    with open(BOOK_FILE, 'r') as f:
        books = json.load(f)
    return render_template('bookexchange.html', books=books)


@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    contact = request.form['contact']

    with open(BOOK_FILE, 'r') as f:
        books = json.load(f)

    books.append({
        'title': title,
        'author': author,
        'description': description,
        'contact': contact
    })

    with open(BOOK_FILE, 'w') as f:
        json.dump(books, f, indent=2)

    return redirect('/bookexchange.html')


# --- TEACHERS CABIN ---
@app.route('/teacherscabin.html')
def teacherscabin():
    with open(TEACHERS_FILE, 'r') as f:
        teachers = json.load(f)
    return render_template('teacherscabin.html', teachers=teachers)


@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    name = request.form['name']
    department = request.form['department']
    cabin = request.form['cabin']
    contact = request.form['contact']

    with open(TEACHERS_FILE, 'r') as f:
        teachers = json.load(f)

    teachers.append({
        'name': name,
        'department': department,
        'cabin': cabin,
        'contact': contact
    })

    with open(TEACHERS_FILE, 'w') as f:
        json.dump(teachers, f, indent=2)

    return redirect('/teacherscabin.html')


# --- BLOOD DONATION ---
@app.route('/blooddonation.html')
def blooddonation():
    with open(BLOOD_FILE, 'r') as f:
        donors = json.load(f)
    return render_template('blooddonation.html', donors=donors)


@app.route('/register_donor', methods=['POST'])
def register_donor():
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']
    bloodgroup = request.form['bloodgroup']
    condition = request.form.get('condition', '')

    with open(BLOOD_FILE, 'r') as f:
        donors = json.load(f)

    donors.append({
        'name': name,
        'age': age,
        'email': email,
        'bloodgroup': bloodgroup,
        'condition': condition
    })

    with open(BLOOD_FILE, 'w') as f:
        json.dump(donors, f, indent=2)

    return render_template('thanks.html', name=name)


# --- LOGOUT ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/home.html')


# --- ACADEMIC NOTES ---
@app.route('/notes.html')
def notes():
    with open(NOTES_FILE, 'r') as f:
        notes_list = json.load(f)
    return render_template('notes.html', notes=notes_list)


@app.route('/upload_notes', methods=['POST'])
def upload_notes():
    title = request.form['title']
    description = request.form['description']
    
    if 'file' not in request.files:
        return "No file uploaded! <a href='/notes.html'>Try again</a>"
        
    file = request.files['file']
    if file.filename == '':
        return "No file selected! <a href='/notes.html'>Try again</a>"
        
    # Validate file type
    allowed_extensions = {'.pdf', '.doc', '.docx'}
    _, ext = os.path.splitext(file.filename.lower())
    if ext not in allowed_extensions:
        return "Invalid file type! Only PDF and Word documents (.pdf, .doc, .docx) are allowed. <a href='/notes.html'>Try again</a>"
        
    # Ensure uploads folder exists
    upload_folder = os.path.join(app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Secure filename simply
    safe_filename = "".join([c for c in file.filename if c.isalnum() or c in {'.', '_', '-'}])
    # Avoid collisions
    filepath = os.path.join(upload_folder, safe_filename)
    counter = 1
    basename, file_ext = os.path.splitext(safe_filename)
    while os.path.exists(filepath):
        safe_filename = f"{basename}_{counter}{file_ext}"
        filepath = os.path.join(upload_folder, safe_filename)
        counter += 1
        
    file.save(filepath)
    
    # Record in json
    with open(NOTES_FILE, 'r') as f:
        notes_list = json.load(f)
        
    notes_list.append({
        'title': title,
        'description': description,
        'file_path': f'/uploads/{safe_filename}',
        'file_type': ext[1:].upper() + ' Document'
    })
    
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes_list, f, indent=2)
        
    return redirect('/notes.html')


# --- DELETE NOTE ---
@app.route('/delete_note/<int:index>', methods=['POST'])
def delete_note(index):
    with open(NOTES_FILE, 'r') as f:
        notes_list = json.load(f)
    if 0 <= index < len(notes_list):
        # Optionally remove the physical file too
        note = notes_list[index]
        file_path = note.get('file_path', '')
        if file_path.startswith('/uploads/'):
            full_path = os.path.join(app.static_folder, 'uploads', os.path.basename(file_path))
            if os.path.exists(full_path):
                os.remove(full_path)
        notes_list.pop(index)
        with open(NOTES_FILE, 'w') as f:
            json.dump(notes_list, f, indent=2)
    return redirect('/notes.html')


# --- STATIC FILES ---
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(debug=True)
