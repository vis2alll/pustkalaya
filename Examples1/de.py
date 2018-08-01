
def downloaded_files():
    
    import os
    #import glob
    #cwd = os.getcwd()
    #lst=os.listdir("/home/cdh/vishal_iit/UIFramework/")
    #print lst
    #glob.glob()
    _dir="/home/cdh/vishal_iit/UIFramework/examples/"
    ext=[".epub",".py"]
    #files=[fn for fn in os.listdir(path) if fn.endswith(ex) for ex in ext ]
    files=[]
    for fn in os.listdir(_dir):
        for ex in ext:
            if fn.endswith(ex):
                files.append(fn)
                
    file_details=[]
    
    for f in files:
        info=[]
        path=os.path.join(_dir, f)
        info.append(f)
        info.append(str(os.stat(path).st_size)+" bytes")
        info.append(str(os.stat(path).st_mtime)+"")
        file_details.append(info)
        
    return file_details
    