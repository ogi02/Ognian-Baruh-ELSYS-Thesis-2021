// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/services/database.dart';
import 'package:mobile/screens/cameras/components/loading_screen.dart';

class CamerasList extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _CamerasListState();
  }
}

class _CamerasListState extends State<CamerasList> {
  // database service
  final CloudFirestoreService _dbService = new CloudFirestoreService();

  // camera object key constants
  final String _cameraNameKey = "name";

  @override
  Widget build(BuildContext context) {
    return Container(
      child: FutureBuilder(
        future: _dbService.getCameras(),
        builder: (_, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return LoadingScreen();
          } else {
            return ListView.builder(
                itemCount: snapshot.data.length,
                itemBuilder: (_, index) {
                  return Container(
                    margin: EdgeInsets.only(
                      top: 6.0,
                      left: 24.0,
                      right: 24.0,
                    ),
                    padding: EdgeInsets.zero,
                    child: OutlinedButton(
                      onPressed: () {},
                      style: OutlinedButton.styleFrom(
                        side: BorderSide(
                          color: blue,
                          width: 1.6,
                        ),
                        padding: EdgeInsets.symmetric(
                            vertical: 8.0,
                            horizontal: 6.0
                        ),
                      ),
                      child: Row(
                          mainAxisAlignment: MainAxisAlignment.start,
                          children: <Widget>[
                            Icon(
                              Icons.camera_alt_outlined,
                              color: blue,
                              size: 24.0,
                            ),
                            Text("  " + snapshot.data[index].data[_cameraNameKey],
                              style: TextStyle(
                                fontSize: 16,
                                color: blue,
                              ),
                            ),
                          ]
                      ),
                    ),
                  );
                }
            );
          }
        },
      ),
    );
  }

}