import 'package:firebase_auth/firebase_auth.dart';
import 'package:mobile/models/user.dart';

class AuthService {

  // private property
  final FirebaseAuth _auth = FirebaseAuth.instance;

  // create user from firebaseUser
  User _userFromFirebaseUser(FirebaseUser user) {
    return user != null ? User(uid: user.uid) : null;
  }

  // auth change user stream
  Stream<User> get user {
    return _auth.onAuthStateChanged.map(_userFromFirebaseUser);
  }

  // sign in
  Future signIn(String email, String password) async {
    try {
      AuthResult res = await _auth.signInWithEmailAndPassword(email: email, password: password);
      FirebaseUser user = res.user;
      return _userFromFirebaseUser(user);
    } catch(e) {
      return e.message;
    }
  }

  // register
  Future register(String email, String password) async {
    try {
      AuthResult res = await _auth.createUserWithEmailAndPassword(email: email, password: password);
      FirebaseUser user = res.user;
      return _userFromFirebaseUser(user);
    } catch(e) {
      return e.message;
    }
  }

  // sign out
  Future signOut() async {
    try {
      return await _auth.signOut();
    } catch(e) {
      print(e.toString());
      return null;
    }
  }
}