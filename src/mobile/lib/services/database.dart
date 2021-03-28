import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:mobile/services/storage.dart';

class CloudFirestoreService {

  // db reference
  final _databaseReference = FirebaseFirestore.instance;

  // db constants
  final String _userDevicesCollection = "user_devices";
  final String _notificationsCollection = "notifications";
  final String _camerasCollection = "cameras";
  final String _locksCollection = "locks";
  final String _userIdKey = "userID";

  // secure storage
  final SecureStorage _storage = SecureStorage();

  Future getCameras() async {
    // get user id from secure storage
    String userId = await _storage.get(_userIdKey);

    // get cameras from the collection of the user
    QuerySnapshot qn = await _databaseReference
        .collection(_userDevicesCollection)
        .doc(userId)
        .collection(_camerasCollection)
        .get();

    return qn.docs;
  }

  Future getLocks() async {
    // get user id from secure storage
    String userId = await _storage.get(_userIdKey);

    // get locks from the collection of the user
    QuerySnapshot qn = await _databaseReference
        .collection(_userDevicesCollection)
        .doc(userId)
        .collection(_locksCollection)
        .get();

    return qn.docs;
  }

  Future getNotifications() async {
    // get user id from secure storage
    String userId = await _storage.get(_userIdKey);

    List<String> cameraUids = new List();

    // get all cameras for a certain user
    await _databaseReference
        .collection(_userDevicesCollection)
        .doc(userId)
        .collection(_camerasCollection)
        .get()
        .then((qn) => qn.docs.forEach((doc) => cameraUids.add(doc.get("camera_uid"))));

    // get notifications from the collection of the notification, using the camera uid
    QuerySnapshot qn = await _databaseReference
        .collection(_notificationsCollection)
        .where("camera_uid", whereIn: cameraUids)
        .orderBy("time", descending: true)
        .get();

    return qn.docs;
  }
}