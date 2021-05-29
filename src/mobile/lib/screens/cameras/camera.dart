// material
import 'package:flutter/material.dart';

// others
import 'dart:async';
import 'package:intl/intl.dart';

// firebase
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_storage/firebase_storage.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/services/camera.dart';
import 'package:mobile/screens/cameras/components/camera_appbar.dart';

class Camera extends StatefulWidget {
  // camera object
  final DocumentSnapshot camera;
  final String userId;

  // constructor
  Camera({this.camera, this.userId});

  @override
  State<StatefulWidget> createState() {
    return _CameraState(camera, userId);
  }
}

class _CameraState extends State<Camera> {
  // parameters
  String _cameraName, _cameraUid, _userId;
  Future<String> _url;
  Future<String> _time;

  // camera service
  final CameraService _cameraService = CameraService();

  // stream subscription
  StreamSubscription _streamSubscription;

  // constructor
  _CameraState(camera, userId) {
    this._cameraName = camera.get("name");
    this._cameraUid = camera.get("camera_uid");
    this._userId = userId;

  }

  @override
  initState() {
    super.initState();
    _url = _getImageUrl();
    _time = _getImageTime();
    _streamSubscription = FirebaseFirestore.instance
        .collection('user_devices')
        .doc(_userId)
        .collection('cameras')
        .where('camera_uid', isEqualTo: _cameraUid)
        .snapshots()
        .listen((event) {
          _updateImage();
        });
  }

  void _updateImage() {
    setState(() {
      _url = _getImageUrl();
      _time = _getImageTime();
    });
  }

  Future<String> _getImageUrl() async {
    String url = await FirebaseStorage.instance
        .ref()
        .child("/imagesOnDemand")
        .child(_cameraUid)
        .child("image_on_demand.jpg")
        .getDownloadURL();
    return url;
  }

  Future<String> _getImageTime() async {
    FullMetadata metadata = await FirebaseStorage
        .instance
        .ref()
        .child("/imagesOnDemand")
        .child(_cameraUid)
        .child("image_on_demand.jpg")
        .getMetadata();
    return DateFormat().add_MMMMEEEEd().add_Hms().format(metadata.timeCreated);
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
              future: _time,
              builder: (_, snapshot) {
                if (!snapshot.hasData) {
                  return Container(
                    width: 0.0,
                    height: 0.0
                  );
                } else {
                  return Container(
                    margin: EdgeInsets.all(16.0),
                    child: Text(snapshot.data)
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
