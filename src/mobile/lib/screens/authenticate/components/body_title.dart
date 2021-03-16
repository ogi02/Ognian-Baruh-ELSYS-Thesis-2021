// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';

class BodyTitle extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text("Control your IoT Devices",
        style: TextStyle(
          color: blue,
          fontSize: 24.0,
          fontWeight: FontWeight.bold,
        ),
      ),
      padding: EdgeInsets.all(20.0),
      margin: EdgeInsets.only(top: 16.0),
    );
  }
}