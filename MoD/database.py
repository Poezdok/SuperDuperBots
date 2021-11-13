import json
filename = "database.txt"


def get_profile(id):

    with open(filename, 'r') as db:
        text = db.read()
        print(text)
        try:
            data = json.loads(text)
        except json.decoder.JSONDecodeError:
            print("Getting error")
            print(json.decoder.JSONDecodeError)
            return []
        print(data)

        try:
            profile = data[str(id)]
        except KeyError:
            profile = []
        db.close()

    # print("Getting")
    return profile


def save_profile(id, state):
    data = {}

    with open(filename, 'r') as db:
        try:
            data = json.load(db)
        except json.decoder.JSONDecodeError:
            print("Reading error")
        db.close()

    with open(filename, 'w') as db:
        try:
            data[str(id)] = state
        except KeyError:
            data.append({id: state})
        json.dump(data, db, indent=4)
        db.close()

    print("Saving")
