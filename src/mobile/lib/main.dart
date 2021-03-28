import 'package:flutter/material.dart';
import 'package:mobile/services/messaging.dart';
import 'package:overlay_support/overlay_support.dart';
import 'package:provider/provider.dart';
import 'package:mobile/models/user.dart';
import 'package:mobile/services/auth.dart';
import 'package:mobile/screens/wrapper.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';


void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // firebase messaging
  static final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: Firebase.initializeApp(),
      builder: (_, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          final pushNotificationService = PushNotificationService(_firebaseMessaging);
          pushNotificationService.initialise();

          return StreamProvider<AppUser>.value(
            value: AuthService().user,
            initialData: null,
            child: OverlaySupport(
              child: MaterialApp(
                home: Wrapper(),
              ),
            ),
          );
        }
        return MaterialApp(
          home: Center(
            child: Text("Loading .."),
          )
        );
      }
    );
  }
}


