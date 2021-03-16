// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/services/auth.dart';
import 'package:mobile/screens/signin/components/sign_in_appbar.dart';
import 'package:mobile/screens/signin/components/not_have_an_account.dart';

class SignIn extends StatefulWidget {
  @override
  _SignInState createState() => _SignInState();
}

class _SignInState extends State<SignIn> {
  // authentication service
  final AuthService _auth = AuthService();
  final _formKey = GlobalKey<FormState>();

  // placeholders
  String email = '';
  String password = '';
  String error = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: white,
      appBar: SignInAppbar(),
      body: Center(
        child: Container(
          padding: EdgeInsets.symmetric(
            vertical: 30.0,
            horizontal: 50.0,
          ),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                SizedBox(height: 20.0),

                // Email
                TextFormField(
                  validator: (val) => val.isEmpty ? "Email is required!" : null,
                  onChanged: (val) => setState(() => email = val),
                  decoration: InputDecoration(labelText: 'Email'),
                ),

                SizedBox(height: 10.0),

                // Password
                TextFormField(
                  obscureText: true,
                  validator: (val) => val.isEmpty ? "Password is required!" : null,
                  onChanged: (val) => setState(() => password = val),
                  decoration: InputDecoration(labelText: 'Password'),
                ),

                SizedBox(height: 30.0),

                // Sign In Button
                RaisedButton(
                  child: Text("Sign In",
                    style: TextStyle(color: white),
                  ),
                  color: orange,
                  onPressed: () async {
                    if (_formKey.currentState.validate()) {
                      // user or null
                      dynamic result = await _auth.signIn(email, password);
                      if (result is String) {
                        setState(() {
                          error = "Wrong credentials!";
                        });
                      } else {
                        Navigator.of(context).pop();
                      }
                    }
                  },
                ),

                SizedBox(height: 12.0),

                // Error field
                Text(error,
                  style: TextStyle(
                    color: Colors.red,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                SizedBox(height: 10.0),

                DoNotHaveAnAccount(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}