import os, re
from flask import Flask, render_template, request
app = Flask(__name__)

# Reload html without re-running server
app.config['TEMPLATES_AUTO_RELOAD'] = True

# File system locations
app.config["PHISHING_DOMAINS"] = "libraries/Phishing.Database/ALL-phishing-domains.txt"
app.config["UPLOADS_DIR"] = "uploads/"

# Store a snapshot of the database in a dictionary when the server starts
def readPhishingDomains(domainsFile):
	domains = {}
	for line in open(domainsFile):
		domains[line.rstrip()] = 1
	return domains

phishing_domains = readPhishingDomains(app.config["PHISHING_DOMAINS"])

# Main Page
@app.route("/")
def index():
	return render_template("index.html")

# On Upload
@app.route("/results", methods=["POST"])
def fileUpload():
	# Get the file from the request
	email = request.files["email"]

	# Save file to server file system
	email.save(os.path.join(app.config["UPLOADS_DIR"], email.filename))

	# Strip out domains from saved file
	domains = getDomains(app.config["UPLOADS_DIR"]+email.filename)

	# Get a subset of phishy domains as a map
	phishy_domains = getPhishyDomains(domains)

	phish = (False, True)[len(phishy_domains) > 0]

	return render_template("results.html", filename=email.filename, phish=phish, phishy_domains=phishy_domains)

# Returns list of all domains found in file
def getDomains(filename):
	domainRegex = r'(?:[a-z0-9][a-z0-9\-]{0,61}[a-z0-9]\.)+[a-z0-9][a-z0-9\-]*[a-z0-9]'
	domainsInFile = []
	for line in open(filename):
		# Find all domains line by line
		domainsInLine = re.findall(domainRegex, line)
		# Flatten list of domains at each line
		for domain in domainsInLine:
			domainsInFile.append(domain)
	return domainsInFile

# Match list of domains with known phishy domains. Return dictionary of phishy domains (to ensure uniqueness)
def getPhishyDomains(domains):
	found_phishy_domains = {}
	for domain in domains:
		if domain in phishing_domains:
			found_phishy_domains[domain] = 1
	return found_phishy_domains