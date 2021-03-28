import 'package:firebase_auth/firebase_auth.dart';
import 'package:mobile/models/user.dart';
import 'package:mobile/services/storage.dart';

class AuthService {

  // private property
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final SecureStorage _storage = SecureStorage();
  final String _userIdKey = "userID";

  // create user from firebaseUser
  AppUser _userFromFirebaseUser(User user) {
    return user != null ? AppUser(uid: user.uid) : null;
  }

  // auth change user stream
  Stream<AppUser> get user {
    return _auth.authStateChanges().map(_userFromFirebaseUser);
  }

  // sign in
  Future signIn(String email, String password) async {
    try {
      // call firebase function
      UserCredential res = await _auth.signInWithEmailAndPassword(email: email, password: password);

      // get user
      User user = res.user;

      // add user id to storage
      await _storage.write(_userIdKey, user.uid);

      return _userFromFirebaseUser(user);
    } catch(e) {
      return e.message;
    }
  }

  // register
  Future register(String email, String password) async {
    try {
      // call firebase functions
      UserCredential res = await _auth.createUserWithEmailAndPassword(email: email, password: password);

      // get user
      User user = res.user;

      // add user id to storage
      await _storage.write(_userIdKey, user.uid);

      return _userFromFirebaseUser(user);
    } catch(e) {
      return e.toString();
    }
  }

  // sign out
  Future signOut() async {
    try {
      // remove user from storage
      await _storage.delete(_userIdKey);

      // call firebase function
      return await _auth.signOut();
    } catch(e) {
      return e.toString();
    }
  }
}