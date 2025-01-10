import requests
from datetime import datetime

# Your Google Apps Script web app URL
web_app_url = "https://script.google.com/macros/s/AKfycbytm525C472abzDgybx2mwIT7UNmVrM9qJhoqBb5kOd_6D9k0pHYkxx4U3IciRxPnedBg/exec"

# Fetch data from the web app
response = requests.get(web_app_url)
if response.status_code == 200:
    entries = response.json()  # Assuming the response is in JSON format
    print(entries)  # Check the output
else:
    print(f"Error fetching data: {response.status_code}")

# Sort Entries by Date in Descending Order (Newest First)
entries_sorted = sorted(entries, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%dT%H:%M:%S.%fZ"), reverse=True)

# Sample HTML entry template
entry_template = """
    <div class="entry" data-date="{date}">
        <span class="trade-date">{date}</span>
        <div class="trade-details">
            <p><strong>Stock:</strong> {stock}</p>
            <p><strong>Action:</strong> {action}</p>
            <p><strong>Reason:</strong> {reason}</p>
            <img src="{imageUrl}" alt="{stock} trade screenshot" class="trade-image">
        </div>
    </div>
"""

# Create the entries HTML from the sorted list
entries_html = ""
for entry in entries_sorted:
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

# Replace the entire `entries` content
updated_html = html_content.replace(
    '<div id="entries">', 
    f'<div id="entries">{entries_html}'
)

# Print the updated HTML to check
print(updated_html)  # Check the output before saving

# Save the updated index.html
with open('index.html', 'w') as file:
    file.write(updated_html)

print("HTML file updated successfully!")
