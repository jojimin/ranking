from django.test import TestCase
import pymongo

m_client = pymongo.MongoClient('192.168.10.65', 27017)
db = m_client['rank']
db.score.aggregate()

# rank.score.aggregate([
#     {$sort:{score:-1}},
#     {$group}
# ]
# )
# Create your tests here.
