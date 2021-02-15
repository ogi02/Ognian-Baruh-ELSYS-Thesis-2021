import 'package:flutter/material.dart';
import 'package:mobile/screens/register/register.dart';

import 'package:mobile/colors.dart';

class DoNotHaveAnAccount extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          "Don't have an account? ",
          style: TextStyle(
              color: black
          ),
        ),
        GestureDetector(
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => Register()),
            );
          },
          child: Text(
            "Register now!",
            style: TextStyle(
              color: orange,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    );
  }
}