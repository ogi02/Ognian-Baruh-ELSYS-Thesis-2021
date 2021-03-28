// material
import 'package:flutter/material.dart';

// firebase
import 'package:cloud_firestore/cloud_firestore.dart';

// project
import 'package:mobile/screens/locks/components/lock_appbar.dart';
import 'package:mobile/screens/locks/components/lock_button.dart';
import 'package:mobile/screens/locks/components/unlock_button.dart';

class Lock extends StatefulWidget {
  // lock object
  final DocumentSnapshot lock;

  // constructor
  Lock({this.lock});

  @override
  State<StatefulWidget> createState() {
    return _LockState();
  }
}

class _LockState extends State<Lock> {
  // keys for lock object
  final String _lockNameKey = "name";
  final String _lockUidKey = "lock_uid";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: LockAppbar(lockName: widget.lock.get(_lockNameKey)),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            UnlockButton(lockUid: widget.lock.get(_lockUidKey)),
            LockButton(lockUid: widget.lock.get(_lockUidKey)),
          ],
        ),
      ),
    );
  }
}