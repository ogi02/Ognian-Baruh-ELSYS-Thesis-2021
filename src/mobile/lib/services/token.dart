import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:mobile/services/secure_storage.dart';

class TokenService {

  final String _tokenKey = "token";
  final SecureStorage _storage = SecureStorage();

  Future generateToken() async {
    var request = http.Request('POST', Uri.parse('https://access.bosch-iot-suite.com/token HTTP/1.1'));
    request.bodyFields = {
      'grant_type': 'client_credentials',
      'client_id': '3955633f-9d1e-47c9-8dfe-49551b25c66a',
      'client_secret': 'd0346840-76ad-11eb-9439-0242ac130002',
      'scope': 'service:iot-manager:a5c5ad43-9fe1-4b32-af99-092f74e594eb_iot-manager/full-access service:iot-hub-prod:ta5c5ad439fe14b32af99092f74e594eb_hub/full-access service:iot-things-eu-1:a5c5ad43-9fe1-4b32-af99-092f74e594eb_things/full-access'
    };

    http.StreamedResponse response = await request.send();

    if (response.statusCode == 200) {
      var body = await response.stream.bytesToString();
      var token = json.decode(body)["access_token"];
      _storage.write(_tokenKey, token);
    }
    else {
      print(response.reasonPhrase);
    }
  }

  String decodeToken() {
    return 
  }

  Future getToken() async {
    String token = await _storage.get(_tokenKey);
    print(token);
  }
}