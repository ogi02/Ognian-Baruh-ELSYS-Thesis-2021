// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/screens/signin/signin.dart';

class SignInButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.only(top: 4.0),
      child: SizedBox(
        width: 150.0,
        child: RaisedButton.icon(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => SignIn()),
            );
          },
          icon: Icon(
            Icons.people_outline,
            color: white,
          ),
          label: Text("Sign In",
            style: TextStyle(color: white),
          ),
          color: blue,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8.0)),
          padding: EdgeInsets.symmetric(
            vertical: 8.0,
            horizontal: 24.0,
          ),
        ),
      ),
    );
  }
}