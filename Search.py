from tinydb import TinyDB,Query
import Preprocessing

db = TinyDB('db.json')
qr = Query()
def search(sentence):
    result={}
    words = Preprocessing.Clean(sentence)

    for word in words:
        q = db.search(qr.Word == word)
        rating =[]

        try:
            for i in range(len(q[0]['Count'])):
                rating.append(q[0]['Place'][i] - q[0]['Count'][i])
            documents=q[0]['Documents']
            rating, documents = (list(t) for t in zip(*sorted(zip(rating, documents))))
            result[word]=documents
        except:
            pass
    if  sentence.startswith('"') and sentence.endswith('"'):
        res=()
        if len(words)>1 and result:
            for r in result:
                if res:
                    res=res.intersection(result[r])
                else:
                    res=set(result[r])
            return{'result':list(res)}
        else:
            return result
    else:
        return result

