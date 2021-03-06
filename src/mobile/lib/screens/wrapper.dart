import 'package:flutter/material.dart';
import 'package:mobile/models/user.dart';
import 'package:mobile/screens/home/home.dart';
import 'package:mobile/screens/authenticate/authenticate.dart';
import 'package:provider/provider.dart';

class Wrapper extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // get user from provider
    final user = Provider.of<AppUser>(context);

    // show either Home or Authentication
    if (user == null) {
      return Authenticate();
    } else {
      return Home();
    }
  }
}