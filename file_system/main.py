from MainWindow import MainWindow


fileWrite = open("test_file.txt","w")
fileWrite.write("hello files")
fileWrite.close()
fileRead = open("test_file.txt","r")
text = fileRead.read()
print(text)


with open("test_file.txt","w") as fileWrite:
    fileWrite.write("hello files")

with open("test_file.txt","r") as fileRead:
    print(fileRead.read())


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
