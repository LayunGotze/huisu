import pymongo


# Collections initialization

origin = db['origin']
parsed = db['parsed']

cor = origin.find({'o_gt':{'$gt':1522512000, '$lt':1533052800 }})


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


