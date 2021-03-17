// material
import 'package:flutter/material.dart';

// custom
import 'package:intl/intl.dart';

// firebase
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:mobile/colors.dart';

// project
import 'package:mobile/services/storage.dart';
import 'package:mobile/screens/cameras/components/camera_appbar.dart';

class Camera extends StatefulWidget {
  // camera object
  final DocumentSnapshot camera;

  // constructor
  Camera({this.camera});

  @override
  State<StatefulWidget> createState() {
    return _CameraState(camera);
  }
}

class _CameraState extends State<Camera> {
  // parameters
  String _cameraName, _cameraUid;
  StorageReference _cloudStorageRef;
  Future<String> _url;
  Future<String> _userId;

  // constructor
  _CameraState(camera) {
    this._cameraName = camera.data["name"];
    this._cameraUid = camera.data["camera_uid"];

    // reference to firebase storage
    this._cloudStorageRef = FirebaseStorage.instance
        .ref()
        .child("/imagesOnDemand")
        .child(_cameraUid);
  }

  @override
  initState() {
    super.initState();
    _url = _getSnapshotUrl();
    _userId = SecureStorage().get("userID");
  }

  void _update() {
    setState(() {
      _url = _getSnapshotUrl();
    });
  }

  Future<String> _getSnapshotUrl() async {
    String url = await _cloudStorageRef.child("image_on_demand.jpg").getDownloadURL();
    return url;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CameraAppbar(cameraName: _cameraName),
      body: Center(
        child: Column(
          children: [
            FutureBuilder<String>(
              future: _url,
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
            FutureBuilder<String>(
              future: _userId,
              builder: (_, snapshot) {
                if (!snapshot.hasData) {
                  return Center(child: CircularProgressIndicator());
                } else {
                  String userId = snapshot.data;
                  return StreamBuilder(
                    // get stream for the document of the camera
                    stream: Firestore.instance
                        .collection('user_devices')
                        .document(userId)
                        .collection('cameras')
                        .where('camera_uid', isEqualTo: _cameraUid)
                        .snapshots(),
                    builder: (_, AsyncSnapshot<QuerySnapshot> snapshot) {
                      if (!snapshot.hasData) {
                        return Text("Loading ..");
                      } else {
                        // update image
                        WidgetsBinding.instance.addPostFrameCallback((_) => _update());

                        // get timestamp from firestore
                        var timestamp = snapshot.data.documentChanges.first.document.data["time"];

                        // get date from timestamp
                        var date = DateTime.fromMillisecondsSinceEpoch(timestamp).toLocal();

                        // return formatted date
                        return Text(DateFormat().add_MMMMEEEEd().add_Hms().format(date));
                      }
                    },
                  );
                }
              },
            ),
          ],
        ),
      ),
      floatingActionButton: ElevatedButton(
        onPressed: () {},
        child: Text("Get Image",
          style: TextStyle(
              fontSize: 20,
              color: black
          ),
        ),
        style: ElevatedButton.styleFrom(
          primary: yellow,
          padding: EdgeInsets.symmetric(
            horizontal: 36.0,
            vertical: 12.0,
          ),
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}
