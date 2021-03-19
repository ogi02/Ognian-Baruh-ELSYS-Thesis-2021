// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/services/lock.dart';

class LockButton extends StatelessWidget {
  // for sending lock operation
  final LockService _lockService = new LockService();

  // uid of lock
  final String lockUid;

  // constructor
  LockButton({this.lockUid});

  @override
  Widget build(BuildContext context) {
    return ConstrainedBox(
      constraints: BoxConstraints.tightFor(width: 150, height: 150),
      child: OutlinedButton.icon(
        icon: Icon(
          Icons.lock_outlined,
          size: 24,
          color: Colors.white,
        ),
        label: Text('Lock',
          style: TextStyle(
            fontSize: 24,
            color: Colors.white,
          ),
        ),
        onPressed: () async {
          await _lockService.sendLockMessage(lockUid);
        },
        style: OutlinedButton.styleFrom(
          backgroundColor: Colors.red,
          shape: CircleBorder(),
        ),
      ),
    );
  }
}