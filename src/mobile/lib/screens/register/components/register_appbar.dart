// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';

class RegisterAppbar extends StatelessWidget implements PreferredSizeWidget {
  @override
  Size get preferredSize => const Size.fromHeight(60);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: Text("Register",
        style: TextStyle(color: white),
      ),
      backgroundColor: green,
    );
  }
}