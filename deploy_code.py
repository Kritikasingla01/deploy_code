import os
import shutil
import zipfile
from zipfile import ZipFile
import pathlib


root_path = "C:\project_clone\deploy_code"

codeFolder_path = os.path.join(root_path,"code")
config_env_path = os.path.join(root_path,"config_env")
deploy_path = os.path.join(root_path,"deployment_package")

#if deployment-package path doesn't exist then it will create one
if not os.path.exists(deploy_path):
    os.mkdir(deploy_path)
else:
    shutil.rmtree(deploy_path)           
    os.mkdir(deploy_path)


#get code folder name from the code folder path
code_folder_path = pathlib.PurePath(codeFolder_path)
code_folder_name = code_folder_path.name

#getting user input
inp = input('Enter a type: ')

#to get configuration path according to user input
input_env_path = os.path.join(config_env_path, inp)

#creating user input deployment package path(dev,uat,prd)
input_deploy_path = os.path.join(deploy_path,inp)
os.mkdir(input_deploy_path)


#copying files from the user defined(input) folder to the code folder
shutil.copytree(input_env_path, codeFolder_path, dirs_exist_ok=True)


#creating extension folder at root path
extension_folder_path = os.path.join(root_path,"extension")
os.mkdir(extension_folder_path)


#moving all the code files to the extension folder
source = codeFolder_path
destination = extension_folder_path
allfiles = os.listdir(source)
for file in allfiles:
    src_path = os.path.join(source, file)
    dst_path = os.path.join(destination, file)
    shutil.move(src_path, dst_path)


#moving extension folder inside code folder
source = extension_folder_path
destination = codeFolder_path
shutil.move(source, destination)

#renaming the extension folder with the code folder name
os.chdir(codeFolder_path)
os.rename("extension", code_folder_name)

#getting the path of the renamed code folder
New_codeFolder_Path = os.path.join(codeFolder_path, code_folder_name)

#path where zip file will be created

#function used to create the zip file from code folder to user defined deployment package folder
def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for dir,subfolder, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(dir, file)
                zipf.write(file_path, file_path[len_dir_path:]) 
zip_directory(codeFolder_path, os.path.join(input_deploy_path,'ManualExtensionPublishPackage.zip'))

zip_directory(New_codeFolder_Path, os.path.join(input_deploy_path,'StoreExtensionPublishPackage.zip'))


#moving files from new created code(renamed from extension folder) folder at base code folder
source = New_codeFolder_Path
destination = codeFolder_path
allfiles = os.listdir(source)
for f in allfiles:
    src_path = os.path.join(source, f)
    dst_path = os.path.join(destination, f)
    shutil.move(src_path, dst_path)

#deleting the new created code folder
os.rmdir(New_codeFolder_Path)




