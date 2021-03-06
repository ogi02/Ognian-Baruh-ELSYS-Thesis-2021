import 'package:http/http.dart' as http;
import 'package:mobile/services/token.dart';

class CameraService {

  final String _apiUrl = "things.eu-1.bosch-iot-suite.com";
  final String _apiPath = "api/2/things";
  final String _subscriptionName = "finalyearproj";
  final String _namespace = "iotSystem";
  final String _getImageMessage = "getScreenshot";
  final int _defaultTimeout = 0;

  final TokenService _tokenService = TokenService();

  Uri _generateUri(String message, String cameraUid) {
    // generate path
    String path = _apiPath + "/" + _subscriptionName + ":" + _namespace + ":" + cameraUid + "/inbox/messages/" + message;

    // generate map with query params
    Map<String, String> queryParameters = { "timeout": _defaultTimeout.toString() };

    // generate uri
    return new Uri.https(_apiUrl, path, queryParameters);
  }

  Map<String, String> _generateHeaders(String token) {
    return {
      "Authorization": "Bearer " + token
    };
  }

  Future sendGetImageMessage(String cameraUid) async {
    // get token
    var token = await _tokenService.getToken();

    // generate uri
    Uri uri = _generateUri(_getImageMessage, cameraUid);

    // init request
    var request = http.Request('POST', uri);

    // add headers to request
    request.headers.addAll(_generateHeaders(token));

    // send request
    http.StreamedResponse response = await request.send();
  }

}