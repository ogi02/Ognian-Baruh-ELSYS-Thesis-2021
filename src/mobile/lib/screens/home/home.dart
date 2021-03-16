// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/screens/locks/locks_list.dart';
import 'package:mobile/screens/cameras/cameras_list.dart';
import 'package:mobile/screens/home/components/home_appbar.dart';
import 'package:mobile/screens/notifications/notifications_list.dart';

class Home extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _HomeState();
  }
}

class _HomeState extends State<Home> {
  // bottom nav bar constants
  int _currentIndex = 0;
  final List<Widget> _children = [
    CamerasList(),
    LocksList(),
    NotificationsList()
  ];

  void onTabTapped(int index) {
    // change state of bottom nav bar
    setState(() {
      _currentIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: white,
      appBar: HomeAppbar(),
      body: _children[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        onTap: onTabTapped,
        currentIndex: _currentIndex,
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.camera_alt_outlined),
            label: "Cameras",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.lock_outline),
            label: "Door Locks",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.notifications_outlined),
            label: "Notifications",
          )
        ],
      ),
    );
  }
}