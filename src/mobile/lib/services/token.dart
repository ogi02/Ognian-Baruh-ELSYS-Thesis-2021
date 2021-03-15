import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:mobile/services/storage.dart';

class TokenService {

  final String _tokenKey = "token";
  final SecureStorage _storage = SecureStorage();

  // generate token for Bosch IoT Suite
  Future _generateToken() async {
    // initialize request
    var request = http.Request('POST', Uri.parse('https://access.bosch-iot-suite.com/token HTTP/1.1'));

    // add body
    request.bodyFields = {
      'grant_type': 'client_credentials',
      'client_id': '3955633f-9d1e-47c9-8dfe-49551b25c66a',
      'client_secret': 'd0346840-76ad-11eb-9439-0242ac130002',
      'scope': 'service:iot-manager:a5c5ad43-9fe1-4b32-af99-092f74e594eb_iot-manager/full-access service:iot-hub-prod:ta5c5ad439fe14b32af99092f74e594eb_hub/full-access service:iot-things-eu-1:a5c5ad43-9fe1-4b32-af99-092f74e594eb_things/full-access'
    };

    // send request and wait for response
    http.StreamedResponse response = await request.send();

    // check if request is successful
    if (response.statusCode == 200) {
      // get access token from response body
      var body = await response.stream.bytesToString();
      var token = json.decode(body)["access_token"];

      // add token to secure storage
      _storage.write(_tokenKey, token);
    }
    else {
      // print error message
      print(response.reasonPhrase);
    }
  }

  // decode base 64 string
  String _decodeBase64(String str) {
    // modify token
    String output = str.replaceAll("-", "+").replaceAll("_", "/");
    switch (output.length % 4) {
      case 0:
        break;
      case 2:
        output += "==";
        break;
      case 3:
        output += "=";
        break;
      default:
        throw Exception("Illegal base64url string!");
    }

    // return decoded token
    return utf8.decode(base64Url.decode(output));
  }

  // function for decoding jwt token
  Map<String, dynamic> _decodeToken(String token) {

    // split the token into 3 parts
    final parts = token.split('.');

    // check if token is valid
    if (parts.length != 3) {
      throw Exception("Invalid token!");
    }

    // decode part 1 (where the information needed by the app is stored)
    final payload = _decodeBase64(parts[1]);
    // json decode the payload
    final payloadMap = json.decode(payload);
    // check if payload is valid
    if (payloadMap is! Map<String, dynamic>) {
      throw Exception("Invalid payload!");
    }

    // return payload map
    return payloadMap;
  }

  // get token or generate if the previous one has expired
  Future<String> getToken() async {
    // get token from storage
    String token = await _storage.get(_tokenKey);

    // check if token exists
    if (token == null) {
      // generate token
      await _generateToken();
      // get new token
      token = await _storage.get(_tokenKey);
      return token;
    }

    // decode token
    final decoded = _decodeToken(token);

    // get expiry date
    DateTime exp = DateTime.fromMicrosecondsSinceEpoch(decoded["exp"]).toUtc();
    // get now
    DateTime now = DateTime.now().toUtc();

    // check if token has expired
    if (exp.isBefore(now)) {
      // generate new token
      await _generateToken();
      // get new token
      token = await _storage.get(_tokenKey);
    }

    return token;
  }
}