import 'package:flutter/material.dart';

class BodyTitle extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text(
        "Control your IoT Devices",
        style: TextStyle(
          color: Colors.white70,
          fontSize: 24.0,
          fontWeight: FontWeight.bold,
        ),
      ),
      padding: EdgeInsets.all(20.0),
      margin: EdgeInsets.only(
        top: 16.0,
      ),
    );
  }
}