import 'package:flutter/material.dart';

import 'package:mobile/screens/authenticate/components/components.dart';

class Authenticate extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[800],
      appBar: AppBar(
        title: Text(
          "IoT Home System",
          style: TextStyle(
            color: Colors.amberAccent[400],
          ),
        ),
        backgroundColor: Colors.grey[900],
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
                    // Login
                    LoginButton(),
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