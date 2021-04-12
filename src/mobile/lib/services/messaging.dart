import 'dart:convert';
import 'dart:io' show Platform;
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:mobile/colors.dart';
import 'package:mobile/services/storage.dart';
import 'package:overlay_support/overlay_support.dart';

class PushNotificationService {
  final FirebaseMessaging _fcm;
  final SecureStorage _storage = SecureStorage();

  PushNotificationService(this._fcm);

  Future initialise() async {
    if (Platform.isIOS) {
      _fcm.requestPermission(alert: true, badge: true, provisional: true, sound: true);
    }

    // get token for notifications
    getNotificationToken();

    // on notification receive handler
    FirebaseMessaging.onMessage.listen((RemoteMessage message) => onNotificationReceive(message));

    // on notification open handler
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) => onNotificationOpen(message));
  }

  Future getNotificationToken() async {
    // get token
    String token = await _fcm.getToken();

    // save token to storage
    await _storage.write("notificationToken", token);
  }

  void onNotificationReceive(RemoteMessage message) {
    // get notification details
    RemoteNotification notification = message.notification;

    // get time from body
    final timestamp = int.parse(notification.body);
    // get time from timestamp
    final time = DateTime.fromMillisecondsSinceEpoch(timestamp).toLocal();

    // show pop up window on top
    showSimpleNotification(
      Container(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(notification.title,
              style: TextStyle(
                color: black,
                fontSize: 16.0
              ),
            ),
            Text(DateFormat().add_MMMMEEEEd().add_Hms().format(time),
              style: TextStyle(
                color: black,
                fontSize: 12.0
              ),
            )
          ]
        ),
      ),
      position: NotificationPosition.top,
      background: yellow
    );
  }

  void onNotificationOpen(RemoteMessage message) {
    print('A new onMessageOpenedApp event was published!');
  }
}