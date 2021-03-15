import 'package:flutter/material.dart';
import 'package:mobile/colors.dart';
import 'package:mobile/services/auth.dart';
import 'package:mobile/services/lock.dart';
import 'package:mobile/services/secure_storage.dart';
import 'package:mobile/services/token.dart';

class Home extends StatelessWidget {

  final AuthService _auth = AuthService();
  final TokenService _tokenService = TokenService();
  final LockService _lockService = LockService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: white,
      body: Row(
        children: [
          FlatButton(
            onPressed: () async {
              await _auth.signOut();
            },
            child: Text("Log Out!"),
          ),
          FlatButton(
            onPressed: () async {
              await _lockService.sendLockMessage();
            },
            child: Text("Lock!"),
          ),
          FlatButton(
            onPressed: () async {
              await _lockService.sendUnlockMessage();
            },
            child: Text("Unlock!"),
          ),
        ],
      ),
    );
  }

}