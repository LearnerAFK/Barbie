import os


def dirr():
    for file in os.listdir():
        if file.endswith(".jpg"):
            os.remove(file)
            
    for file in os.listdir():
        if file.endswith(".jpeg"):
            os.remove(file)

    if "downloads" not in os.listdir():
        os.mkdir("downloads")
        
    if "cache" not in os.listdir():
        os.mkdir("cache")
    
