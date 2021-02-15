import 'package:flutter/material.dart';
import 'package:mobile/screens/signin/signin.dart';

import 'package:mobile/colors.dart';

class AlreadyHaveAnAccount extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          "Already have an account? ",
          style: TextStyle(
              color: black
          ),
        ),
        GestureDetector(
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => SignIn()),
            );
          },
          child: Text(
            "Sign in!",
            style: TextStyle(
              color: green,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    );
  }
}