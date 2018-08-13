from console.logger import logger
import traceback

download_folder=r'Downloads/'
def downloaded_files():
    try:
        _logger = logger('downloaded_files')
        import os
        import datetime
        current_directory = os.getcwd()
        _dir= os.path.join(current_directory, r'Downloads')
        if not os.path.exists(_dir):
           os.makedirs(_dir)
        ext=[".epub",".py",".pdf",".docx",".zip"]
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
            info.append("size:"+str(os.stat(path).st_size)+" bytes")
            info.append("modified:"+str(datetime.datetime.fromtimestamp(os.stat(path).st_mtime))[:-10]+"")
            file_details.append(info)
    
        if file_details==[]:
            file_details=[["No Book in Downloads"]]
        return file_details
        
    except:
        _logger.error('application exited with exception: %r' % traceback.format_exc())
        raise
    finally:
        pass 
    