import os, shlex, subprocess, re, datetime, sys
import msbuilder

class Perforce:
	def __init__(self, client, host):
		self.client = client
		self.host = host

	def sync(self):
		globArg1 = '-c'
		globArg2 = self.client
		globArg3 = '-p'
		globArg4 = self.host
		
		cmdArg1 = 'sync'

		procResult = subprocess.run(["p4", globArg1, globArg2, globArg3, globArg4, cmdArg1], stdout=subprocess.PIPE, universal_newlines=True)

		if procResult.returncode == 1:
			return False	# exit early
		
		return True

	def resolve(self):
		globArg1 = '-c'
		globArg2 = self.client
		globArg3 = '-p'
		globArg4 = self.host

		cmdArg1 = 'resolve'
		cmdArg2 = '-am'

		resolveResult = subprocess.run(["p4", globArg1, globArg2, globArg3, globArg4, cmdArg1, cmdArg2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

		if resolveResult.returncode == 1:
			return False

		if resolveResult.stderr != "No file(s) to resolve.\n":
			return False
		
		return True







useAlternateWorkspace = True


##################################################################################
##
##		Regular Workspace
##
##################################################################################
if useAlternateWorkspace == False:
	codeClient		= r'onward-main-prog-scarroll'
	codePort		= r'tor-snowdrop-proxy:4716'

	dataClient		= r'onward-main-data-scarroll'
	dataPort		= r'p4-tor-onward-main.ubisoft.org:3726'

	sharpMakeFile	= r'F:/projects/onward/main/code/sharpmakeprojects/generate_sharpmake_projects_onward_no_pause.bat'

	solutionFile	= r'F:/projects/onward/main/code/sharpmakeprojects/generated/Onward_win64_vs2012.sln'


##################################################################################
##
##		Alternate Workspace
##
##################################################################################
else:
	codeClient		= r'onward-main-prog-scarroll-alternate'
	codePort		= r'tor-snowdrop-proxy:4716'

	dataClient		= r'onward-main-data-scarroll-alternate'
	dataPort		= r'p4-tor-onward-main.ubisoft.org:3726'

	sharpMakeFile	= r'F:/projects/onward-alternate/main/code/sharpmakeprojects/generate_sharpmake_projects_onward_no_pause.bat'

	solutionFile	= r'F:/projects/onward-alternate/main/code/sharpmakeprojects/generated/Onward_win64_vs2012.sln'






codeP4 = Perforce(codeClient, codePort)


print("Syncing Code...")
if codeP4.sync()==False:
	print ("ERROR: P4 code syncing failed")
	sys.exit()


print("Resolving Code...")
if codeP4.resolve() == False:
	print ("ERROR: P4 code resolving failed")
	sys.exit()

print("Syncing Data...")
dataP4 = Perforce(dataClient, dataPort)
if dataP4.sync() == False:
	print ("ERROR: P4 data syncing failed")
	sys.exit()



print("Sharpmaking...")
subprocess.run([sharpMakeFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


print("Compiling...")
codeBuilder = msbuilder.MsBuilder()
codeBuilder.run(solutionFile)