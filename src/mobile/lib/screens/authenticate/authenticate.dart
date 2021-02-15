import 'package:flutter/material.dart';
import 'package:mobile/colors.dart';

import 'package:mobile/screens/authenticate/components/components.dart';

class Authenticate extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: white,
      appBar: AppBar(
        title: Text(
          "IoT Home System",
          style: TextStyle(
            color: white,
          ),
        ),
        backgroundColor: blue,
      ),
      body: Container(
        child: Center(
          child: Column(
            children: [
              // Body Title
              BodyTitle(),
              // Body Icon
              BodyIcon(),
              // Login and Register
              Container(
                child: Column(
                  children: [
                    // Sign in
                    SignInButton(),
                    // Register
                    RegisterButton(),
                  ],
                ),
                margin: EdgeInsets.symmetric(
                  vertical: 16.0,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}