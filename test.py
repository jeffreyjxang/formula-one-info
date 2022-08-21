import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("formula-1-database-8667e-firebase-adminsdk-5nb6j-fb676ac809.json")
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()

firestore_db.collection(u'songs').add({'song': 'Imagine', 'artist': 'John Lennon'})
snapshots = list(firestore_db.collection(u'songs').get())
for snapshot in snapshots:
    print(snapshot.to_dict())