from bson.objectid import ObjectId
from datetime import datetime
from connection import get_db

db = get_db()

# ==============================
#  USER MODEL
# ==============================
user_collection = db['User']

class UserModel:
    @staticmethod
    def find_by_username(username):
        return user_collection.find_one({'username': username})

    @staticmethod
    def find_by_email(email):
        return user_collection.find_one({'email': email})

    @staticmethod
    def find_by_id(user_id):
        return user_collection.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    def insert_user(data):
        return user_collection.insert_one(data)

    @staticmethod
    def update_user(user_id, data):
        return user_collection.update_one({'_id': ObjectId(user_id)}, {'$set': data})

    @staticmethod
    def delete_user(user_id):
        return user_collection.delete_one({'_id': ObjectId(user_id)})

    @staticmethod
    def get_all():
        return list(user_collection.find())


# ==============================
#  STOK MODEL
# ==============================
stok_collection = db['VMS_Stok']

class StokModel:
    @staticmethod
    def find_by_branch(branch_id):
        return list(stok_collection.find({'branch_id': ObjectId(branch_id)}))

    @staticmethod
    def find_by_id(stok_id):
        return stok_collection.find_one({'_id': ObjectId(stok_id)})

    @staticmethod
    def insert_stok(data):
        return stok_collection.insert_one(data)

    @staticmethod
    def update_stok(stok_id, data):
        return stok_collection.update_one({'_id': ObjectId(stok_id)}, {'$set': data})

    @staticmethod
    def delete_stok(stok_id):
        return stok_collection.delete_one({'_id': ObjectId(stok_id)})

    @staticmethod
    def decrement_stok(stok_id, branch_id, qty):
        result = stok_collection.update_one(
            {'_id': ObjectId(stok_id), 'branch_id': ObjectId(branch_id), 'stok': {'$gte': qty}},
            {'$inc': {'stok': -qty}},
        )
        return result.modified_count == 1

    @staticmethod
    def increment_stok(stok_id, qty):
        stok_collection.update_one({'_id': ObjectId(stok_id)}, {'$inc': {'stok': qty}})


# ==============================
#  BRANCH MODEL
# ==============================
branch_collection = db['VMS_Branch']

class BranchModel:
    @staticmethod
    def get_all():
        return list(branch_collection.find())

    @staticmethod
    def get_active():
        return list(branch_collection.find({'activeStatus': 'Y'}))

    @staticmethod
    def find_by_id(branch_id):
        return branch_collection.find_one({'_id': ObjectId(branch_id)})


# ==============================
#  VENDOR MODEL
# ==============================
vendor_collection = db['VMS_Vendor']

class VendorModel:
    @staticmethod
    def get_all():
        return list(vendor_collection.find())

    @staticmethod
    def insert_vendor(data):
        try:
            if 'branch' in data and not isinstance(data['branch'], ObjectId):
                data['branch'] = ObjectId(data['branch'])
            return vendor_collection.insert_one(data)
        except Exception as e:
            print("Error insert_vendor:", e)
            return None

    @staticmethod
    def update_vendor(vendor_id, data):
        return vendor_collection.update_one({'_id': ObjectId(vendor_id)}, {'$set': data})

    @staticmethod
    def delete_vendor(vendor_id):
        try:
            return vendor_collection.delete_one({'_id': ObjectId(vendor_id)})
        except Exception as e:
            print("Error delete_vendor:", e)
            return None

    @staticmethod
    def find_by_id(vendor_id):
        return vendor_collection.find_one({'_id': ObjectId(vendor_id)})

    @staticmethod
    def find_by_branch(branch_id):
        return list(vendor_collection.find({'branch': ObjectId(branch_id)}))

    @staticmethod
    def get_by_branch(branch_id):
        try:
            cursor = vendor_collection.find({'branch': ObjectId(branch_id)})
            return list(cursor)
        except Exception as e:
            print("Error get_by_branch:", e)
            return []


# ==============================
#  TRANSAKSI MODEL
# ==============================
transaksi_collection = db['VMS_Transaksi']

class TransaksiModel:
    @staticmethod
    def insert_transaksi(data):
        data['tanggal'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return transaksi_collection.insert_one(data)

    @staticmethod
    def get_by_branch(branch_id):
        return list(transaksi_collection.find({'branch_id': ObjectId(branch_id)}))
