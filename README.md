### Group Accommodation Allocation Web Application
This web application facilitates the digitalization of the hospitality process for group accommodation in hostels. It allows users to upload two CSV files containing group information and hostel room details. The application then allocates rooms based on specified criteria and provides allocation details.

## Features
Upload CSV Files: Users can upload two CSV files:

# Group Information CSV: Contains details about groups such as group ID, number of members, and gender.
Hostel Information CSV: Contains information about hostel rooms including hostel name, room number, capacity, and gender accommodation.
Room Allocation Algorithm: Allocates rooms based on the following criteria:

# Members of the same group (same ID) stay in the same room whenever possible.
Boys and girls stay in their respective hostels.
Room capacity is not exceeded.
Output: Displays allocated rooms with details such as group ID, hostel name, and room number. Also provides a downloadable CSV file with allocation details.

# Technologies Used
Frontend: HTML, CSS, JavaScript (Fetch API)
Backend: Python (Flask)
Data Processing: Pandas library for Python

## Requirements 

Make sure you have Python 3.x installed.
```pip3 install Flask pandas```

#### Usage Run the Flask Server:
``` python3 app.py ```

Access the Application:
Open your web browser and go to http://localhost:5000/

# Upload CSV Files:

Choose your Group Information CSV and Hostel Information CSV files using the file input fields.
Click on the "Upload" button to process the files.

# View Results:

Once files are uploaded, allocated rooms will be displayed on the web page.
You can download the allocation details as a CSV file using the provided link.

Example CSV files (groups.csv and hostels.csv) are provided in the repository for testing purposes.

## Troubleshooting
Cross-Origin Request Blocked: If you encounter CORS issues during development, ensure that the frontend (`index.html`) is served by Flask (`app.py`). Check the Flask server logs and browser console for any error messages.

