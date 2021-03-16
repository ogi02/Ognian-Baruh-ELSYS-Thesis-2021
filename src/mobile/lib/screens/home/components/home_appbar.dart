// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/services/auth.dart';

class HomeAppbar extends StatelessWidget implements PreferredSizeWidget {

  // auth service
  final AuthService _auth = AuthService();

  @override
  Size get preferredSize => const Size.fromHeight(60);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: blue,
      title: Text("IoT Home System",
        style: TextStyle(color: white),
      ),
      actions: <Widget>[
        IconButton(
          icon: Icon(
            Icons.logout,
            color: white,
          ),
          onPressed: () async {
            await _auth.signOut();
          },
        )
      ],
    );
  }
}