// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/services/lock.dart';

class UnlockButton extends StatelessWidget {
  // for sending unlock operation
  final LockService _lockService = new LockService();

  // uid of lock
  final String lockUidKey;

  // constructor
  UnlockButton({this.lockUidKey});

  @override
  Widget build(BuildContext context) {
    return ConstrainedBox(
      constraints: BoxConstraints.tightFor(width: 150, height: 150),
      child: OutlinedButton.icon(
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
          await _lockService.sendUnlockMessage(lockUidKey);
        },
        style: OutlinedButton.styleFrom(
          backgroundColor: Colors.green,
          shape: CircleBorder(),
        ),
      ),
    );
  }
}