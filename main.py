import dropbox

access_token = 'xxx'#put your acces token here
files_to_sync = ['./test22.txt', './test2.txt', './test3.txt', './test/nocheintest/eintest.txt']
default_location = "/files" #without '/' at the end!
# file_to = '/dev_test/test.txt'  # The full path to upload the file to, including the file name

class bcolors: #colors
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class TransferData:
    def __init__(self, access_token, default_location):
        self.access_token = access_token
        self.default_location = default_location

    def upload_files(self, files, files_to, filenames): #upload a file to Dropbox using API v2
        print("Starting Upload:\n")
        dbx = dropbox.Dropbox(self.access_token)

        for file, filename in zip(files, filenames):
            #print(file, filename)
            with open(file, 'rb') as f:
                try:
                    joinlist = []
                    joinlist.append(self.default_location)
                    print("Uploading file: '{}'...".format(file), end='')
                    filepath_split = file.split("/")
                    filepath = filepath_split[:-1]

                    if "./" in filepath[0]:
                        filepath[0] = filepath[0][2:] #delete the './' at the beginning
                        # print("We have a './'")
                    else:
                        filepath[0] = filepath[0][1:] # or only the '/'
                        # print("We have a '/'")
                    filepath = list(filter(None, filepath)) #delete empty strings, else it would cause somthing like '///'

                    for i in filepath:
                        joinlist.append(i)
                    joinlist.append(filename)
                    # print("Joinlist:\n", joinlist, filepath_split, filepath, file)
                    files_to = '/'.join(joinlist)
                    dbx.files_upload(f.read(), files_to) #final upload function
                    print(bcolors.OKGREEN + "done" + bcolors.ENDC, end='\n')
                    # print("\n",files_to)
                except Exception as e:
                    print(e)
                    print(bcolors.WARNING + "Couldn't upload file:".format(e) + bcolors.ENDC)

class Scanner():
    def __init__(self, files):
        self.scanfor = files
        self.files = []
        self.filenames = []

    def scan(self, dest_db):
        print("Searching for files:\n")
        for file in self.scanfor:
            print("Searching for file: '{}'...".format(file), end='')
            try:
                open(file, 'r')
            except FileNotFoundError:
                print(bcolors.WARNING + "File not found: '{}'".format(file) + bcolors.ENDC)
            else:
                print(bcolors.OKGREEN + "done" + bcolors.ENDC)
                filename = file.split("/").pop() #splits the full filename and gets the last element from the list

                self.files.append(file)
                self.filenames.append(filename)

        print() #just for some space (creates a newline)
        return self.files, self.filenames

def main():
    files_to = '/dev_test/'
    scanner = Scanner(files_to_sync)
    files, filenames = scanner.scan(files_to)
    transferData = TransferData(access_token, default_location)
    transferData.upload_files(files, files_to, filenames)
    # file_from = './test.txt'
    #
    # transferData.upload_file(file_from, file_to)
    # print("Uploadet file!")

if __name__ == '__main__':
    main()
