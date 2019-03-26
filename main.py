import dropbox
import os.path as ospath
# access_token = 'xxx' #put your acces token here
# files_to_sync = ['./test22.txt', './test2.txt', './test3.txt', './test/nocheintest/eintest.txt']
# default_location = "/files" #without '/' at the end!
# file_to = '/dev_test/test.txt'  # The full path to upload the file to, including the file name
config_file = "./PySyncConf.conf"


class colors: #colors

    BOLD='\033[1m'
    ITALIC='\033[3m'
    RED='\033[91m'
    GREEN='\033[92m'
    END='\033[0m'


class config():
    def __init__(self):
        if ospath.exists(config_file):
            self.conf_exists = True
        else:
            self.conf_exists = False
            #  print(
            return self.conf_exists
        

    def read_config(self):
        self.config_list = list()
        cfile = open(config_file)
        for line in cfile:
            if "#" in line:
                pass # make comments possible
            else:
                self.config_list.append(line)
        #  print(self.config_list)
        
        config_list_tmp = list()
        for s in self.config_list:
            config_list_tmp = [s.replace("\n","") for s in self.config_list]
        config_list_tmp = [x for x in config_list_tmp if x]
        self.config_list = config_list_tmp

        #  print(self.config_list)
        self.configs = dict()
        self.files = list()
        for line in self.config_list:
            key, val = line.split("=")
            if key == "file":
                self.files.append(val)
            else:
                self.configs[key] = val
        self.configs["files"] = self.files
        # print(self.configs)

    def get_config(self):
        if self.configs["access_token"]:
            self.auth_token = self.configs["access_token"]
        else:
            print(colors.RED + "Please specify a access token in the config file!\nConfig file at: ./PySyncConf.conf" + colors.END)
        if self.configs["dbx_folder"]:
            self.dbx_folder = self.configs["dbx_folder"]
        else:
            print(colors.RED + "Please specify the destination folder for dropbox in the config file!\nConfig file at: ./PySyncConf.conf" + colors.END)
        if self.configs["files"]:
            pass # self.files is already a list with all files
        else:
            print(colors.RED + "No files specified! Please specify files in the config file at: ./PySyncConf.conf" + colors.END)


def upload(auth_token, dest_folder, files):
    dbx = dropbox.Dropbox(auth_token)
    for file in files:
        try:
            dest = file.split("/")[-1:]
            # print(dest[-1:], dest_folder)
            destination = dest_folder + dest[0]
            # print(destination)
            ofile = open(file, "rb")
            print("Uploading file:\t\t{}...".format(file), end="")
            dbx.files_upload(ofile.read(), destination)
            print(colors.GREEN + "done!" + colors.END)

            # metadata = dbx.files_list_folder('/data/')
            # flist = []
            # if metadata.has_more == True:
                # m1 = metadata.entries
                # cur = metadata.cursor
                # for i in m1:
                    # if isinstance(i, dropbox.files.FileMetadata):
                        # flist.append([i.name, i.size])
                # m2 = dbx.files_list_folder_continue(cur)
                # while m2.has_more == True:
                    # for i in m2.entries:
                        # if isinstance(i, dropbox.files.FileMetadata):
                            # flist.append([i.name, i.size])
                    # cur = m2.cursor
                    # m2 = dbx.files_list_folder_continue(cur)
            # print(flist)

        except Exception as e:
            print(colors.RED + "failed!\n" + str(e) + colors.END)

def check_config():
    if ospath.exists(config_file):
        if config():
            c = config()
            c.read_config()
            c.get_config()
            return True, c
        else:
            print(colors.RED + "Could not load config file!" + colors.END)
    else:
        print(colors.RED + "Config file is ether not specified or doesn't exits!\nCheck at: ./PySyncConf.conf" + colors.END)
        return False


def main():
    # files_to = '/dev_test/'
    # scanner = Scanner(files_to_sync)
    # files, filenames = scanner.scan(files_to)
    # transferData = TransferData(access_token, default_location)
    # transferData.upload_files(files, files_to, filenames)
    # file_from = './test.txt'
    #
    # transferData.upload_file(file_from, file_to)
    # print("Uploadet file!")
    config_check, config = check_config()
    if config_check is not True:
        exit()
       
    else: #config file exists, prepare for upload
        # print(config.files)
        # print(config.auth_token)
        # print(config.dbx_folder)

        # files = config.files
        # auth_token = config.auth_token
        # dbx_folder = config.dbx_folder
        print("Going to upload following files:\n\n" + colors.BOLD + "Reading file list from config:\n" + colors.END, end="")
        for file in config.files:
            print("\t" + file)
        dec = str(input("\nUpload files? [y/n]: "))
        if dec:
            if dec in ["N", "n", "No", "no"]:
                print(colors.RED + "\nCanceling upload!\nExiting..." + colors.END)
                exit()
            elif dec in ["Y", "y", "Yes", "yes"]:
                print(colors.GREEN + "Starting Upload..." + colors.END)
                upload(config.auth_token, config.dbx_folder, config.files)
                print("Finishing upload\nExiting...")
                exit()
            else:
                print(colors.RED + "\nCanceling upload!\nExiting..." + colors.END)
                exit()

if __name__ == '__main__':
    main()
