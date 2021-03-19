// material
import 'package:flutter/material.dart';

// others
import 'package:intl/intl.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/services/database.dart';
import 'package:mobile/screens/notifications/notification.dart';

class NotificationsList extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _NotificationsListState();
  }
}

class _NotificationsListState extends State<NotificationsList> {
  // database service
  final CloudFirestoreService _dbService = new CloudFirestoreService();

  @override
  Widget build(BuildContext context) {
    return Container(
      child: FutureBuilder(
        future: _dbService.getNotifications(),
        builder: (_, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Text("Loading ..");
          } else {
              return ListView.builder(
                itemCount: snapshot.data.length,
                itemBuilder: (_, index) {
                  // get timestamp from firestore
                  var timestamp = snapshot.data[index].data["time"];
                  // get date from timestamp
                  var date = DateTime.fromMillisecondsSinceEpoch(timestamp).toLocal();
                  // get formatted date
                  String dateText = DateFormat().add_MMMMEEEEd().add_Hms().format(date);

                  // get detected names
                  var names = snapshot.data[index].data["names"];
                  // generate message
                  String message = names.join(", ");

                  // get camera uid
                  String cameraUid = snapshot.data[index].data["camera_uid"];

                  // get notification id
                  String notificationId = snapshot.data[index].data["notification_id"];

                  return Container(
                    margin: EdgeInsets.only(
                      top: 6.0,
                      left: 24.0,
                      right: 24.0,
                    ),
                    padding: EdgeInsets.zero,
                    child: OutlinedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => NotificationPage(
                            dateText, message, cameraUid, notificationId
                          )),
                        );
                      },
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
                            Icons.notifications_outlined,
                            color: blue,
                            size: 32.0,
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Container(
                                padding: EdgeInsets.symmetric(
                                  horizontal: 6.0,
                                  vertical: 2.0
                                ),
                                child: Text(message,
                                  style: TextStyle(
                                    fontSize: 16,
                                    color: blue,
                                  ),
                                ),
                              ),
                              Container(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 6.0,
                                    vertical: 2.0
                                ),
                                child: Text(dateText,
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: blue,
                                  ),
                                ),
                              ),
                            ],
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