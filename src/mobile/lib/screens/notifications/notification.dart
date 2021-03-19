// material
import 'package:flutter/material.dart';

// firebase
import 'package:firebase_storage/firebase_storage.dart';

// others
import 'package:intl/intl.dart';

// project
import 'package:mobile/screens/notifications/components/notification_appbar.dart';

class NotificationPage extends StatefulWidget {

  // notification info
  final String _date;
  final String _message;
  final String _cameraUid;
  final String _notificationId;

  NotificationPage(this._date, this._message, this._cameraUid, this._notificationId);

  @override
  State<StatefulWidget> createState() {
    return _NotificationState(_date, _message, _cameraUid, _notificationId);
  }
}

class _NotificationState extends State<NotificationPage> {
  // notification info
  final String _date;
  final String _message;
  final String _cameraUid;
  final String _notificationId;

  // notification image url
  Future<String> _imageUrl;

  // cloud storage reference
  var _cloudStorageRef;

  // constructor
  _NotificationState(this._date, this._message, this._cameraUid, this._notificationId) {
    print(_date);
    print(_message);
    print(_cameraUid);
    print(_notificationId);
    // reference to firebase storage
    _cloudStorageRef = FirebaseStorage.instance
        .ref()
        .child("/notificationImages")
        .child(_cameraUid);
  }

  @override
  initState() {
    super.initState();
    _imageUrl = _getSnapshotUrl();
  }

  Future<String> _getSnapshotUrl() async {
    String url = await _cloudStorageRef.child(_notificationId + ".jpg").getDownloadURL();
    return url;
  }

  Widget build(BuildContext context) {
    return Scaffold(
      appBar: NotificationAppbar(message: _message),
      body: Center(
        child: Column(
          children: [
            FutureBuilder<String>(
              future: _imageUrl,
              builder: (_, snapshot) {
                if (!snapshot.hasData) {
                  return Center(child: CircularProgressIndicator());
                } else {
                  return Container(
                    margin: EdgeInsets.all(16.0),
                    child: Image.network(snapshot.data),
                  );
                }
              },
            ),
            Text(_date),
          ],
        ),
      ),
    );
  }
}