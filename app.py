from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'groupFile' not in request.files or 'hostelFile' not in request.files:
            return jsonify(error="No file part"), 400
        
        group_file = request.files['groupFile']
        hostel_file = request.files['hostelFile']
        
        # Check if the files are empty
        if group_file.filename == '' or hostel_file.filename == '':
            return jsonify(error="No selected file"), 400
        
        # Read CSV files
        group_df = pd.read_csv(group_file)
        hostel_df = pd.read_csv(hostel_file)
        
        print("CSV files read successfully")
        
        # Process allocations
        allocations = allocate_rooms(group_df, hostel_df)
        
        # Save allocation results to CSV
        allocation_df = pd.DataFrame(allocations)
        allocation_df.to_csv('allocations.csv', index=False)
        
        print("Allocations processed successfully")
        
        return jsonify(allocations)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error=str(e)), 500

def allocate_rooms(group_df, hostel_df):
    allocations = []
    
    # Separate hostels by gender
    boys_hostels = hostel_df[hostel_df['Gender'] == 'Boys'].copy()
    girls_hostels = hostel_df[hostel_df['Gender'] == 'Girls'].copy()
    mixed_hostels = hostel_df[hostel_df['Gender'] == 'Mixed'].copy()
    
    # Separate groups by gender
    boys_groups = group_df[group_df['Gender'] == 'Boys']
    girls_groups = group_df[group_df['Gender'] == 'Girls']
    mixed_groups = group_df[group_df['Gender'].str.contains('&')]
    
    # Function to allocate a group to available hostels
    def allocate_group(group, hostels, allocations):
        allocated = False
        for i, room in hostels.iterrows():
            if room['Capacity'] >= group['Members']:
                allocations.append({
                    'Group ID': group['Group ID'],
                    'Hostel Name': room['Hostel Name'],
                    'Room Number': room['Room Number'],
                    'Members Allocated': group['Members']
                })
                hostels.at[i, 'Capacity'] -= group['Members']
                allocated = True
                break
        if not allocated:
            allocations.append({
                'Group ID': group['Group ID'],
                'Hostel Name': 'Not Allocated',
                'Room Number': 'N/A',
                'Members Allocated': group['Members']
            })
    
    # Allocate boys groups
    for _, group in boys_groups.iterrows():
        allocate_group(group, boys_hostels, allocations)
    
    # Allocate girls groups
    for _, group in girls_groups.iterrows():
        allocate_group(group, girls_hostels, allocations)
    
    # Allocate mixed groups
    for _, group in mixed_groups.iterrows():
        members = int(group['Members'])
        allocate_group(pd.Series({
            'Group ID': group['Group ID'],
            'Members': members,
            'Gender': 'Mixed'
        }), mixed_hostels, allocations)
    
    return allocations

@app.route('/download', methods=['GET'])
def download_file():
    try:
        return send_file('allocations.csv', as_attachment=True)
    except Exception as e:
        print(f"Error: {e}")
        return str(e), 500

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
