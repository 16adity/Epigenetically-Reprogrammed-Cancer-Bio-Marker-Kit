from flask import Flask, render_template, request, redirect, url_for
from predict import predict_cancer
import os

app = Flask(__name__)

# Function to store form data into text file
def store_patient_data(data):
    # Create a directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Write the form data to a text file
    with open('patient_data.txt', 'a') as file:
        file.write(str(data) + '\n')

# Function to read recent patient data from the text file
def read_recent_patient_data():
    # Read the last line from the file
    with open('patient_data.txt', 'r') as file:
        lines = file.readlines()
        if lines:
            data = lines[-1].strip().strip('{}').split(', ')
            recent_patient_data = {}
            for item in data:
                parts = item.split(': ')
                if len(parts) == 2:
                    key, value = parts
                    recent_patient_data[key] = value.strip("'")  # Strip single quotes from the value
                else:
                    recent_patient_data[item] = ''  # Handle cases where splitting results in only one part
        else:
            recent_patient_data = {}
    return recent_patient_data


# Flag to track if start.html has been executed once
start_executed = False

@app.route('/')
def start():
    global start_executed
    if not start_executed:
        start_executed = True
        return render_template('start.html')
    else:
        return redirect(url_for('registration_form'))

@app.route('/login')
def login_page():
    return render_template('login.html')
# Route to handle login form submission
@app.route('/Login', methods=['POST'])
def handle_login():
    # Here, you can add login logic if needed
    # For now, redirecting to the registration form
    return redirect(url_for('registration_form'))

@app.route('/form')
def registration_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Extract form data
    data = {
        'Name': request.form.get('name'),
        'Date of Birth': request.form.get('DOB'),
        'Gender': request.form.get('Gender'),
        'Age': request.form.get('Age'),
        'Address': request.form.get('address'),
        'Pincode': request.form.get('pincode'),
        'Mobile': request.form.get('Mobile'),
        'Email': request.form.get('email'),
        'Emergency Contact Name': request.form.get('emergency_name'),
        'Relation': request.form.get('relation'),
        'Emergency Contact Mobile': request.form.get('emergency_mobile'),
        'Medical History': ', '.join(request.form.getlist('medical_condition')),
        'Surgical History': ', '.join(request.form.getlist('type'))  # Changed to 'type' instead of 'surgical_history'
    }

    # Call function to store data into text file
    store_patient_data(data)

    # Redirect to image upload page after form submission
    return redirect(url_for('upload_page'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        # Extract form data
        patient_data = {
            'Name': request.form.get('name'),
            'Date of Birth': request.form.get('DOB'),
            'Gender': request.form.get('Gender'),
            'Age': request.form.get('Age'),
            'Address': request.form.get('address'),
            'Pincode': request.form.get('pincode'),
            'Mobile': request.form.get('Mobile'),
            'Email': request.form.get('email'),
            'Emergency Contact Name': request.form.get('emergency_name'),
            'Relation': request.form.get('relation'),
            'Emergency Contact Mobile': request.form.get('emergency_mobile'),
            'Medical History': ', '.join(request.form.getlist('medical_condition')),
            'Surgical History': ', '.join(request.form.getlist('type'))  # Changed to 'type' instead of 'surgical_history'
        }

        # Call predict_cancer() function from predict.py to make predictions
        prediction_result, percentage_affected, cancer_stage, original_image = predict_cancer(file)

        # Pass the patient data and prediction results to the template for display
        recent_patient_data = read_recent_patient_data()
        return render_template('predict.html', patient_data=patient_data, prediction=prediction_result, percentage_affected=percentage_affected, cancer_stage=cancer_stage, original_image=original_image, recent_patient_data=recent_patient_data)

    return render_template('upload.html')

@app.route('/click')
def click_page():
    return render_template('click.html')

if __name__ == '__main__':
    app.run(debug=True)
