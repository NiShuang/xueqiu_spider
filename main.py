from spiders.xueqiuSpider import XueqiuSpider
from spiders.tushareAPI import Tushare
from util.database import MongoDB
from util.util import getExchange
from multi_thread.multi_thread import WorkManager
from config.config import thread_num
import pymongo


mongoDB = MongoDB()
client = mongoDB.getClient()
database = client['xueqiu_database']
post_collection = database['post_collection']

user_collection = database['user_collection']

def get_stock_list():
    exist_stock = post_collection.distinct("stock.code")
    tushare = Tushare()
    stock_list = tushare.getStockList()
    i = 0
    while i < len(stock_list):
        code = stock_list[i]['code']
        if code in exist_stock:
            del stock_list[i]
            i -= 1
        i += 1
    return stock_list


def post_spider_func(stock, proxy=''):
    spider = XueqiuSpider()
    code = stock['code']
    full_code = getExchange(code) + code
    print full_code
    stock['full_code'] = full_code
    posts = spider.getPosts(full_code, proxy)
    bulk_post = []
    for post in posts:
        user = {
            'id': post['user']['id'],
            'name': post['user']['screen_name']
        }
        post_doc = {
            'stock': stock,
            'user': user,
            'post_id': post['id'],
            'text': post['text'],
            'source': post['source'],
            'created_at': post['created_at'],
            'like_count': post['like_count'],
            'retweet_count': post['retweet_count'],
            'reward_count': post['reward_count'],
            'reward_user_count': post['reward_user_count'],
            'fav_count': post['fav_count'],
            'reply_count': post['reply_count'],
            'reply_list': []
        }
        bulk_post.append(post_doc)
    post_collection.insert_many(bulk_post)


def post_spider():
    # proxy_list = get_valid_proxy_list()
    # proxy_list.insert(0, '')
    # proxy_num = len(proxy_list)
    stock_list = get_stock_list()
    wm = WorkManager(thread_num)
    for index, i in enumerate(stock_list):
        # proxy = proxy_list[int(index % proxy_num)]
        wm.add_job(index, post_spider_func, i)
    wm.start()
    wm.wait_for_complete()


def get_post_list():
    exist_post = post_collection.distinct('post_id', {'reply_list': [], 'reply_count': { '$gt': 0}})
    print len(exist_post)
    return exist_post

def reply_spider_func(postID):
    spider = XueqiuSpider()
    replies = spider.getReply(postID)
    bulk_reply = []
    for reply in replies:
        user = {
            'id': reply['user']['id'],
            'name': reply['user']['screen_name']
        }
        reply_doc = {
            'reply_id': reply['id'],
            'user': user,
            'created_at': reply['created_at'],
            'text': reply['text'],
            'source': reply['source'],
            'reward_count': reply['reward_count'],
            'reward_user_count': reply['reward_user_count'],
            'like_count': reply['like_count']
        }
        bulk_reply.append(reply_doc)
    post_collection.update_many(
        {"post_id": postID},
        {
            "$set": {"reply_list": bulk_reply},
        }
    )

def reply_spider():
    post_list = get_post_list()
    wm = WorkManager(thread_num)
    for index, i in enumerate(post_list):
        wm.add_job(index, reply_spider_func, i)
    wm.start()
    wm.wait_for_complete()


def get_user_list():
    all_user = post_collection.distinct('user.id')
    exist_user = user_collection.distinct('id')
    user_list = list(set(all_user).difference(set(exist_user)))
    print len(user_list)
    return user_list


def user_spider_func(userID):
    spider = XueqiuSpider()
    user = spider.getUserInfo(userID)
    if user == None:
        return
    user_doc = {
        'id': user['id'],
        'stocks_count': user['stocks_count'],
        'city': user['city'],
        'province': user['province'],
        'verified': user['verified'],
        'verified_realname': user['verified_realname'],
        'donate_count': user['donate_count'],
        'followers_count': user['followers_count'],
        'friends_count': user['friends_count'],
        'verified_type': user['verified_type'],
        'verified_description': user['verified_description'],
        'stock_list': user['stock_list'],
        'cube_count': user['cube_count'],
        'description': user['description'],
        'post_count': user['status_count'],
        'name': user['screen_name'],
        'gender': user['gender']
    }
    user_collection.insert(user_doc)

def user_spider():
    user_list = get_user_list()
    wm = WorkManager(thread_num)
    for index, i in enumerate(user_list):
        wm.add_job(index, user_spider_func, i)
    wm.start()
    wm.wait_for_complete()


def get_all_user_list():
    user_id_list = user_collection.distinct('id',{"stock_list.0": {'$exists': True},"stock_list.0.price": {'$exists': False}})
    print len(user_id_list)
    return user_id_list


def get_stock_trade_func(user_id):
    user = user_collection.find_one({'id': user_id})
    user_id = user['id']
    stock_list = user['stock_list']
    spider = XueqiuSpider()
    stock_list = spider.get_stocks_trade(stock_list)
    if stock_list == None:
        return
    user_collection.update(
        {"id": user_id},
        {
            "$set": {"stock_list": stock_list},
        }
    )


def stock_spider():
    user_id_list = get_all_user_list()
    wm = WorkManager(thread_num)
    for index, i in enumerate(user_id_list):
        wm.add_job(index, get_stock_trade_func, i)
    wm.start()
    wm.wait_for_complete()

if __name__ == '__main__':
    post_spider()
    # reply_spider()
    # user_spider()
    # stock_spider()
