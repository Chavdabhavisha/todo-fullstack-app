def find_or_create_user(mongo, email):
    users = mongo.db.users
    user = users.find_one({"email": email})
    if not user:
        users.insert_one({"email": email})
    return users.find_one({"email": email})