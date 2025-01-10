import requests

# Your Google Apps Script web app URL
web_app_url = "https://script.google.com/macros/s/AKfycbytm525C472abzDgybx2mwIT7UNmVrM9qJhoqBb5kOd_6D9k0pHYkxx4U3IciRxPnedBg/exec"

# Fetch the data from the Google Sheets via Apps Script
response = requests.get(web_app_url)
entries = response.json()  # Assuming the response is in JSON format

# Sample HTML entry template for each journal entry
entry_template = """
    <div class="trade-entry">
        <span class="trade-date">{date}</span>
        <div class="trade-details">
            <p><strong>Stock:</strong> {stock}</p>
            <p><strong>Action:</strong> {action}</p>
            <p><strong>Reason:</strong> {reason}</p>
            <img src="{imageUrl}" alt="{stock} trade screenshot" class="trade-image">
        </div>
    </div>
"""

# Create the entries HTML by iterating over the fetched entries
entries_html = ""
for entry in entries:
    entries_html += entry_template.format(
        date=entry["date"],
        stock=entry["stock"],
        action=entry["action"],
        reason=entry["reason"],
        imageUrl=entry["imageUrl"]
    )

# Read the existing index.html
with open('index.html', 'r') as file:
    html_content = file.read()

# Find the start and end of the entries container
start_marker = '<div id="entries-container">'
end_marker = '</div>'  # Closing tag of the container

# Find the positions in the HTML file
start_pos = html_content.find(start_marker) + len(start_marker)
end_pos = html_content.find(end_marker, start_pos)

# If the markers are found, replace the entries between them
if start_pos != -1 and end_pos != -1:
    # Insert new entries HTML between the markers
    new_html_content = html_content[:start_pos] + entries_html + html_content[end_pos:]
    
    # Write the updated HTML back to the file
    with open('index.html', 'w') as file:
        file.write(new_html_content)
else:
    print("Error: Could not find the entries container in the HTML file.")
