// material
import 'package:flutter/material.dart';

// project
import 'package:mobile/colors.dart';
import 'package:mobile/screens/register/components/register_appbar.dart';
import 'package:mobile/services/auth.dart';
import 'package:mobile/screens/register/components/already_have_an_account.dart';

class Register extends StatefulWidget {
  @override
  _RegisterState createState() => _RegisterState();
}

class _RegisterState extends State<Register> {
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
      appBar: RegisterAppbar(),
      body: Center(
        child: Container(
          padding: EdgeInsets.symmetric(
            vertical: 30.0,
            horizontal: 40.0,
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
                  validator: (val) => val.length < 6 ? "Password must be at least 6 characters long!" : null,
                  onChanged: (val) => setState(() => password = val),
                  decoration: InputDecoration(labelText: 'Password'),
                ),

                SizedBox(height: 30.0),

                // Sign in button
                ElevatedButton(
                  child: Text("Register",
                    style: TextStyle(color: white),
                  ),
                  style: ButtonStyle(backgroundColor: MaterialStateProperty.all<Color>(green)),
                  onPressed: () async {
                    if (_formKey.currentState.validate()) {
                      // user or null
                      dynamic result = await _auth.register(email, password);
                      if (result is String) {
                        setState(() {
                          error = result;
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

                AlreadyHaveAnAccount(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
