from django.shortcuts import render, HttpResponse
import pymongo

m_client = pymongo.MongoClient('192.168.10.65', 27017)
db = m_client['rank']
# Create your views here.
# for i in range(2, 100):
#     db.score.insert_one({'client_id': i, 'score': 1000+i})
# rank = list(db.score.find().sort("score", pymongo.DESCENDING).skip(1).limit(10))
# rank.append(db.score.find_one({'client_id': 3}))
# for loc, data in enumerate(rank):
#     data['rank'] = 1 + loc
#     del data['_id']
# print(rank)
# print(db.score.find_one({'client_id': 44}))
# print(db.score.find().sort("score", pymongo.DESCENDING))
# args = [{"$sort":{"score":-1}},
#         {"$group":{"_id": "$client_id" ,"all": {"$push": "$client_id"}}},
#         {"$project":{"_id": "$client_id", "index": {"$indexOfArray": ["$all",1]}}}]
# print(list(db.score.aggregate(pipeline=args)))

# lis = list(db.score.find().sort("score", pymongo.DESCENDING))
# self_rank = [i["client_id"] for i in lis].index(4)
# print(self_rank)
print(list(db.score.find({"client_id": 1112})))

def index(request):
    return render(request, 'rank/index.html')

def upload_score(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id', None)
        score = request.POST.get('score', None)

        if client_id and score:
            client_id = int(client_id)
            score = int(score)
            if 1<=score<=10000000:
                if list(db.score.find({"client_id": client_id})):
                    db.score.update({"client_id": client_id}, {"$set":{"score": score}})
                    return HttpResponse('200 UPDATE')
                else:
                    ret = db.score.insert_one({"client_id": client_id, "score": score})
                    print(ret.inserted_id)
                    return HttpResponse('200 ADD')
            else:
                return HttpResponse('Invalid score')
        else:
            return HttpResponse('Failed')

def ranking(request, client_id, range):
    if request.method == 'GET':
        # start = request.GET.get('start', 1)
        # end = request.GET.get('end', 10)
        # client_id = request.GET.get('client_id')
        start, end = range.split('-')
        client_id = int(client_id)
        print(start, end, client_id)
        rank = list(db.score.find().sort("score", pymongo.DESCENDING).skip(int(start)-1).limit(int(end)-int(start)+1))


        # add rankNumber to the result-set
        for loc, data in enumerate(rank):
            data['rank'] = int(start)+loc
            del data['_id']

        # get current user's rank
        lis = list(db.score.find().sort("score", pymongo.DESCENDING))
        self_rank = [i["client_id"] for i in lis].index(client_id)
        rank.append(db.score.find_one({'client_id': client_id}))
        rank[-1]['rank'] = self_rank+1
        del rank[-1]['_id']
        # res = {
        #     'code': 1,
        #     'data': rank
        # }
        return render(request, 'rank/ranking.html', {'rank': rank})


