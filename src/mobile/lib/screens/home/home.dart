import 'package:flutter/material.dart';
import 'package:mobile/colors.dart';
import 'package:mobile/services/auth.dart';

class Home extends StatelessWidget {

  final AuthService _auth = AuthService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: white,
      body: FlatButton(
        onPressed: () async {
          await _auth.signOut();
        },
        child: Text("Log Out!"),
      ),
    );
  }

}