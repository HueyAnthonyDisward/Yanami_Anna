import sqlite3

# Connect to the database (or create it if it doesn't exist)
con = sqlite3.connect("storage.db")
cursor = con.cursor()

# Create the sys_command table if it doesn't exist
query = "CREATE TABLE IF NOT EXISTS sys_command(sys_id INTEGER PRIMARY KEY, sys_name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# Create the web_command table if it doesn't exist
query = "CREATE TABLE IF NOT EXISTS web_command(web_id INTEGER PRIMARY KEY, web_name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# List of applications
apps = [
    ("OneNote", "C:/Program Files/Microsoft Office/root/Office16/ONENOTE.EXE"),
    ("Word", "C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE"),
    ("Excel", "C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE"),
    ("Chrome", "C:/Program Files/Google/Chrome/Application/chrome.exe"),
    ("Paint", "C:/Windows/System32/mspmsn.exe"),
    ("Calculator", "C:/Windows/System32/calc.exe"),
    ("Clock", "C:/Windows/System32/timedate.cpl"),
    ("ThisPC", "explorer.exe shell:::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"),
    ("RecycleBin", "explorer.exe shell:::{645FF040-5081-101B-9F08-00AA002F954E}"),
    ("Settings", "explorer.exe ms-settings:")
]

# List of popular websites
websites = [
    ("Google", "https://www.google.com"),
    ("Facebook", "https://www.facebook.com"),
    ("YouTube", "https://www.youtube.com"),
    ("Twitter", "https://www.twitter.com"),
    ("Instagram", "https://www.instagram.com"),
    ("LinkedIn", "https://www.linkedin.com"),
    ("Reddit", "https://www.reddit.com"),
    ("Wikipedia", "https://www.wikipedia.org"),
    ("Amazon", "https://www.amazon.com"),
    ("GitHub", "https://www.github.com")
]

# Insert the application list into the database
for app in apps:
    query = "INSERT INTO sys_command (sys_name, path) VALUES (?, ?)"
    cursor.execute(query, app)

# Insert the list of websites into the database
for website in websites:
    query = "INSERT INTO web_command (web_name, url) VALUES (?, ?)"
    cursor.execute(query, website)

# Commit changes to the database
con.commit()

# Close the connection
con.close()
