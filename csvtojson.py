import argparse, csv, json

#Initialise Arguments using argparse module, allows for easy argument handling and automated -h functionality
parser = argparse.ArgumentParser()
parser.description = "description: convert CSV to JSON"
parser.add_argument("file",         help="input file eg. sample.csv (or relative path)")
parser.add_argument("-k", "--key",  help="specify a primary key to use, 'auto'=index starting at 0")
parser.add_argument("outdir",       help="output directory eg. c:/users/bob/desktop")
parser.add_argument("outfile",      help="output filename eg. sample.json")
args = parser.parse_args()

def convertJSON(file, outdir, outfile, key):
    print(f"Converting {file} to {outdir}\{outfile}")                                       
    with open(file, "r", encoding='utf-8-sig') as file:     #Open CSV file and remove embedded BOM, BOM causes issues when specifying primary key
        fileCSV = csv.DictReader(file)                      #Read CSV file with DictReader method, allows easier converting to JSON
        if (key is None):                                   #Check if there is a -k argument  
            data = [row for row in fileCSV]                 #If no key specified, append dictionaries without primary key
                    
        elif key == "auto":                                 #If key is set to auto, use i from enumerate() tuple as the primary key
            data = {}                                           
            for i,row in enumerate(fileCSV):
                data[i+1] = row   
                                                        
        else:   
            data = {}                                                    
            try:
                for row in fileCSV:                             
                    data[row[key]] = row                    #Use -k argument as primary key, validate input
            except KeyError:
                print(f"Invalid Key, valid keys are:")
                print([key for key in next(fileCSV).keys()])
                exit()
                
#Try create a new json file and write json data
    try:
        with open(f"{outdir}/{outfile}", 'x') as newFile:               
            newFile.write(json.dumps(data, indent=4, ensure_ascii=False))  
                      
#If file already exists, check if the file should be overwritten, validate input
    except FileExistsError:                                    
        while((option:=input("File already exists, overwrite?[n/Y] ").lower()) not in ["", "y", "n", "yes"]):
            print(f"Invalid option: {option}")    
                    
#Overwrite contents of existing .JSON file
        if (option in ["", "y", "yes"]):
            with open(f"{outdir}/{outfile}", 'w') as newFile:
                newFile.write(json.dumps(data, indent=4, ensure_ascii=False))  
            print(f"{outfile} overwritten successfully") 
            
#Call convert function with arguments
convertJSON(args.file, args.outdir, args.outfile, args.key)
