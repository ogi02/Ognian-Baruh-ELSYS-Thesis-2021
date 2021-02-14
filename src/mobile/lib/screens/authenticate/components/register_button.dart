import 'package:flutter/material.dart';

class RegisterButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: SizedBox(
        width: 150.0,
        child: RaisedButton.icon(
          onPressed: () {},
          icon: Icon(
              Icons.person_add_alt_1_outlined
          ),
          label: Text("Register"),
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