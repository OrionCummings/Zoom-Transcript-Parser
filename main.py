#!/usr/bin/python
import os
import platform
import re
import tkinter as tk
from tkinter import filedialog

#import Window

#Global Variables
OPERATING_SYSTEM = ""
VALID_FILE_SUFIX = ".vtt"
VALID_FILE = 0
SOURCE_PATH = ""
DEST_PATH = ""
FIX_COMMON_SPELLING_ERRORS = 0

class Application(tk.Frame):
	path = ""

	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		#Create File File Button
		self.findFile = tk.Button(self)
		self.findFile["text"] = "Find File"
		self.findFile["command"] = self.openFileBrowser
		self.findFile["height"] = 10
		self.findFile["width"] = 20
		self.findFile.config(font='bold')
		self.findFile.pack(side="left")

		#Create Confirm Button
		self.quit = tk.Button(self, text = "Confirm")
		self.quit["height"] = 10
		self.quit["width"] = 10
		self.quit["command"] = self.master.destroy
		self.quit.config(font='bold')
		self.quit.pack()

	def openFileBrowser(self):
		root.filename = filedialog.askopenfilename(	initialdir = "/", 
													title = "Select vtt file",
													filetypes = (("vtt files","*.vtt"), ("txt files","*.txt")))
		self.path = root.filename
		#print(root.filename)
		#return root.filename
		#updateButtons(self)

	def updateButtons(self):
		tk.StringVar().set("File Found: " + root.filename)
		pass

root = tk.Tk()
root.title("Minutes Parser")
root.geometry("300x200")
root.resizable(0, 0)
app = Application(master=root)
app.mainloop()

#Returns the operating system
#Used to correct paths, if necessary
def getOperatingSystem():
	return platform.system()
	pass	

#Function definitions
#Checks if the given file is valid
def validate():
	pattern = "(((\.)(\w+)))$"
	fileSufix = re.search(pattern, sourceName)
	if fileSufix:
		if (fileSufix.group() == VALID_FILE_SUFIX):
			VALID_FILE = 1
		else:
			dest.write("Invalid source file. Given file must end in \"" + VALID_FILE_SUFIX + "\".")
			exit()

#Fixes commonly spelling mistakes
def fixSpelling():
	pass

#Clean up file and write to destination
def clean():
	lines = source.readlines(0)
	#removes the first line
	lines.pop(0)
	#removes single instances of newline
	lines = [i for i in lines if i != '\n']
	#removes strings that start with numbers
	lines = list(filter(lambda v: re.match('^\D+', v), lines))
	
	names = []
	content = []
	output = []
	currentName = ""
	previousName = ""

	for line in lines:
		#removes unatributed lines
		if(':' not in line):
			lines.remove(line)

		#finds lines with names
		if(':' in line):
			namePattern = "^.+: "
			contentPattern = ":\s.+"
			#isolate the name
			n = re.search(namePattern, line)
			#check to see if a name was found properly
			if n:
				#remove trailing colon and add it to names
				currentName = n.group().replace(':', '')
				if(currentName != previousName):
					#print(currentName)
					output.append("\n" + currentName)

				#isolate content
				c = re.search(contentPattern, line).group().replace(':', '')
				names.append(currentName)
				content.append(c)
				output.append(c)

				#does the current name match the previous name or is this the
				#first line, in which case there is no previous name
				if(currentName == previousName):
					line = line.replace(currentName, "", 1)
					#dest.write(line)

		previousName = currentName
		 #end of file iterator

	names = set(list(names))
	numParticipants = len(names)
	#print("There were " + str(numParticipants) + " participants at this meeting.")

	#write lines to destination file
	for line in output:
		dest.write(line + "\n")

#Close opened files
def closeFiles():
	source.close()
	dest.close()

#####################################################################################

#Names of each file
SOURCE_PATH = app.path
sourceName = os.path.basename(SOURCE_PATH)
replacement = sourceName
DEST_PATH = app.path.replace(replacement, "")
destName = sourceName.replace(".vtt", "")
destName = destName + "FORMATED.txt"
DEST_PATH = DEST_PATH + destName

#converts windows paths into unix paths
if(getOperatingSystem() != "Windows"):
	SOURCE_PATH = SOURCE_PATH.replace("\\", "/")

#File objects
source = open(SOURCE_PATH, "r")
dest = open(DEST_PATH, "w")

#Validate file and operating system
validate()

#Clean up source file
#Removes newlines and timestamps
#Concatenates names and paragraphs
#Outputs to destination file
clean()

#Closing opened files
closeFiles()

#Close the program
exit()
