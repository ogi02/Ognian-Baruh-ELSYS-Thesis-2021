import 'package:flutter/material.dart';
import 'package:mobile/colors.dart';

class BodyIcon extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Icon(
        Icons.home_outlined,
        size: 96.0,
        color: yellow,
      ),
      margin: EdgeInsets.all(24.0),
      padding: EdgeInsets.symmetric(
        vertical: 12.0,
      ),
    );
  }
}