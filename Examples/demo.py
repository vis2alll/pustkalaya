import os,sys
a= os.getcwd().split("/")[:-1].join("/")
for i in a:
    
    b=os.path.join(a[i],a[i+1])
print current_dir
#current_dir.split
sys.path.append("/home/suman/vishal RBD/sugam_pustkalay/pustakalay")