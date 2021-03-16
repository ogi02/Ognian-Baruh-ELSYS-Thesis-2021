// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/screens/authenticate/components/components.dart';

class Authenticate extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: white,
      appBar: AuthenticateAppbar(),
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
                margin: EdgeInsets.symmetric(vertical: 16.0),
                child: Column(
                  children: [
                    // Sign in
                    SignInButton(),
                    // Register
                    RegisterButton(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}