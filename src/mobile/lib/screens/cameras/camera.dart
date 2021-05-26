// material
import 'package:flutter/material.dart';

// others
import 'package:intl/intl.dart';

// firebase
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_storage/firebase_storage.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/services/camera.dart';
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
  Future<String> _url;
  Future<String> _userId;

  // camera service
  final CameraService _cameraService = CameraService();

  // constructor
  _CameraState(camera) {
    this._cameraName = camera.get("name");
    this._cameraUid = camera.get("camera_uid");
  }

  @override
  initState() {
    super.initState();
    _url = FirebaseStorage.instance
        .ref()
        .child("/imagesOnDemand")
        .child(_cameraUid)
        .child("image_on_demand.jpg")
        .getDownloadURL();
    _userId = SecureStorage().get("userID");
  }

  // Future<String> _getSnapshotUrl() async {
  //   String url = await FirebaseStorage.instance
  //       .ref()
  //       .child("/imagesOnDemand")
  //       .child(_cameraUid)
  //       .child("image_on_demand.jpg")
  //       .getDownloadURL();
  //   return url;
  // }

  void _updateImageUrl() {
    setState(() {
      _url = FirebaseStorage.instance
          .ref()
          .child("/imagesOnDemand")
          .child(_cameraUid)
          .child("image_on_demand.jpg")
          .getDownloadURL();
    });
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
                    stream: FirebaseFirestore.instance
                        .collection('user_devices')
                        .doc(userId)
                        .collection('cameras')
                        .where('camera_uid', isEqualTo: _cameraUid)
                        .snapshots(),
                    builder: (_, AsyncSnapshot<QuerySnapshot> snapshot) {
                      if (!snapshot.hasData) {
                        return Text("Loading ..");
                      } else {
                        // update image
                        Future.delayed(Duration.zero, () async {
                          _updateImageUrl();
                        });

                        // get timestamp from firestore
                        var timestamp = snapshot.data.docChanges.first.doc.get("time");

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
        onPressed: () {
          _cameraService.sendGetImageMessage(_cameraUid);
        },
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
