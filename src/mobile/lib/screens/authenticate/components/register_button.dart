import 'package:flutter/material.dart';
import 'package:mobile/colors.dart';
import 'package:mobile/screens/register/register.dart';

class RegisterButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: SizedBox(
        width: 150.0,
        child: RaisedButton.icon(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => Register()),
            );
          },
          icon: Icon(
            Icons.person_add_alt_1_outlined,
            color: white,
          ),
          label: Text(
            "Register",
            style: TextStyle(
              color: white,
            ),
          ),
          color: blue,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8.0),
          ),
          padding: EdgeInsets.symmetric(
            vertical: 8.0,
            horizontal: 24.0,
          ),
        ),
      ),
      margin: EdgeInsets.only(
          top: 4.0
      ),
    );
  }

}