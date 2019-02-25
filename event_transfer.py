import pymongo


# Collections initialization
client=pymongo.MongoClient(host='111.205.121.89',port=14201)
db=client.en_event
db.authenticate("gyc", "123456")
events_tracking=db.events_tracking
origin=db.origin
origin = db['origin']
parsed = db['parsed']

cor = origin.find({'o_gt':{'$gt':1538323200, '$lt':1541001600 }})


while True:
    try:
        rec = cor.next()
        try:
            o_gt = rec['o_gt']
            try:
                s_parsed = rec['s_parsed']
            except:
                s_parsed = {}
            new_rec = {'o_gt': o_gt,
                       's_parsed': s_parsed}
            print(o_gt)
            parsed.insert_one(new_rec)
        except:
            continue;
    except StopIteration:
        print('finished')
        break
    except Exception as e:
        print(e)
print("finish")