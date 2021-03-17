import 'package:http/http.dart' as http;
import 'package:mobile/services/token.dart';

class LockService {

  final String _apiUrl = "things.eu-1.bosch-iot-suite.com";
  final String _apiPath = "api/2/things";
  final String _subscriptionName = "finalyearproj";
  final String _namespace = "iotSystem";
  final String _lockMessage = "lock";
  final String _unlockMessage = "unlock";
  final int _defaultTimeout = 0;

  final TokenService _tokenService = TokenService();

  Uri generateUri(String message, String lockUid) {
    // generate path
    String path = _apiPath + "/" + _subscriptionName + ":" + _namespace + ":" + lockUid + "/inbox/messages/" + message;

    // generate map with query params
    Map<String, String> queryParameters = { "timeout": _defaultTimeout.toString() };

    // generate uri
    return new Uri.https(_apiUrl, path, queryParameters);
  }

  Map<String, String> generateHeaders(String token) {
    return {
      "Authorization": "Bearer " + token
    };
  }

  Future sendLockMessage(String lockUid) async {
    // get token
    var token = await _tokenService.getToken();

    // generate uri
    Uri uri = generateUri(_lockMessage, lockUid);
    
    // init request
    var request = http.Request('POST', uri);

    // add headers to request
    request.headers.addAll(generateHeaders(token));

    // send request
    http.StreamedResponse response = await request.send();
  }

  Future sendUnlockMessage(String lockUid) async {
    // get token
    var token = await _tokenService.getToken();

    // generate uri
    Uri uri = generateUri(_unlockMessage, lockUid);

    // init request
    var request = http.Request('POST', uri);

    // add headers to request
    request.headers.addAll(generateHeaders(token));

    // send request
    http.StreamedResponse response = await request.send();
  }

}