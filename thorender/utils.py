import random
import cPickle


def createCertificate(path,msg,tol=10000000000):
    F = open(path,'w')
    F.write(msg + ' Random certificate: ' + str(random.randint(0,tol)))
    F.close()
    
def createCertificateDict(path,d,tol=10000000000):
    d['__certificate__'] = random.randint(0,tol)
    F = open(path,'w')
    cPickle.dump(d,F)
    F.close()
    

def wget(getpath,savepath,opstring=''):
    os.system('wget ' + opstring + ' "' + getpath + '" -O "' + savepath + '"')
