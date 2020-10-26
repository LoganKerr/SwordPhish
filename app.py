import os, re
from flask import Flask, render_template, request
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["PHISHING_DOMAINS"] = "/Users/Logan/Documents/projects/swordphish/libraries/Phishing.Database/ALL-phishing-domains.txt"
app.config["UPLOADS_DIR"] = "/Users/Logan/Documents/projects/swordphish/uploads/"

def readPhishingDomains(domainsFile):
	domains = {}
	for line in open(domainsFile):
		domains[line.rstrip()] = 1
	return domains

phishing_domains = readPhishingDomains(app.config["PHISHING_DOMAINS"])

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/results", methods=["POST"])
def fileUpload():
	email = request.files["email"]

	# Save file to server file system
	email.save(os.path.join(app.config["UPLOADS_DIR"], email.filename))

	matches = processFile(email.filename)

	return render_template("results.html", filename=email.filename, phish=(False, True)[matches > 0])

def processFile(filename):
	# Strip out domains from email
	data = getDomains(app.config["UPLOADS_DIR"]+filename)

	return findMatches(data, app.config["PHISHING_DOMAINS"])

def getDomains(filename):
	domainRegex = r'(?:[a-z0-9][a-z0-9\-]{0,61}[a-z0-9]\.)+[a-z0-9][a-z0-9\-]*[a-z0-9]'
	data = []
	for line in open(filename):
		if line != '':
			matches = re.findall(domainRegex, line)
			for word in matches:
				data.append(word)
	return data

def writeToFile(data, filename):
	with open(filename, 'w') as f:
		for item in data:
			f.write("%s\n" % item)

def findMatches(data, file):
	matches = 0
	for domain in data:
		if domain in phishing_domains:
			print(domain)
			matches = matches + 1
	return matches