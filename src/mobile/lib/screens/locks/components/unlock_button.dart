// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/services/lock.dart';

class UnlockButton extends StatelessWidget {
  // for sending unlock operation
  final LockService _lockService = new LockService();

  // uid of lock
  final String lockUid;

  // constructor
  UnlockButton({this.lockUid});

  @override
  Widget build(BuildContext context) {
    return ConstrainedBox(
      constraints: BoxConstraints.tightFor(width: 150, height: 150),
      child: ElevatedButton.icon(
        icon: Icon(
          Icons.lock_open_outlined,
          size: 24,
          color: Colors.white,
        ),
        label: Text('Unlock',
          style: TextStyle(
            fontSize: 24,
            color: Colors.white,
          ),
        ),
        onPressed: () async {
          await _lockService.sendUnlockMessage(lockUid);
        },
        style: ElevatedButton.styleFrom(
          elevation: 8.0,
          primary: Colors.green,
          shape: CircleBorder(),
        ),
      ),
    );
  }
}