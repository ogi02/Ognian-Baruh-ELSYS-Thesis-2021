import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:mobile/services/storage.dart';

class CloudFirestoreService {

  // db reference
  final _databaseReference = Firestore.instance;

  // db constants
  final String _userDevicesCollection = "user_devices";
  final String _camerasCollection = "cameras";
  final String _locksCollection = "locks";
  final String _userIdKey = "userID";

  // secure storage
  final SecureStorage _storage = new SecureStorage();

  Future getCameras() async {
    // get user id from secure storage
    String userId = await _storage.get(_userIdKey);

    // get cameras from the collection of the user
    QuerySnapshot qn = await _databaseReference
        .collection(_userDevicesCollection)
        .document(userId)
        .collection(_camerasCollection)
        .getDocuments();

    return qn.documents;
  }

  Future getLocks() async {
    // get user id from secure storage
    String userId = await _storage.get(_userIdKey);

    // get locks from the collection of the user
    QuerySnapshot qn = await _databaseReference
        .collection(_userDevicesCollection)
        .document(userId)
        .collection(_locksCollection)
        .getDocuments();

    return qn.documents;
  }

}