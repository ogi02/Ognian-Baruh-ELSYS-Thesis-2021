// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/services/auth.dart';

class LockAppbar extends StatelessWidget implements PreferredSizeWidget {
  // auth service
  final AuthService _auth = AuthService();

  // name of the lock
  final String lockName;

  // constructor
  LockAppbar({this.lockName});

  @override
  Size get preferredSize => const Size.fromHeight(60);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: yellow,
      title: Text(lockName,
        style: TextStyle(color: black),
      ),
      actions: <Widget>[
        IconButton(
          icon: Icon(
            Icons.logout,
            color: black,
          ),
          onPressed: () async {
            await _auth.signOut();
          },
        )
      ],
    );
  }
}