import 'package:flutter/material.dart';

import 'package:mobile/screens/login/login.dart';

class LoginButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: SizedBox(
        width: 150.0,
        child: RaisedButton.icon(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => Login()),
            );
          },
          icon: Icon(
              Icons.people_outline
          ),
          label: Text("Login"),
          color: Colors.amberAccent[400],
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