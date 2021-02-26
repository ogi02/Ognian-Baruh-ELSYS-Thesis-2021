import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorage {

  // storage
  final _storage = new FlutterSecureStorage();

  Future<String> get(String key) async {
    String value = await _storage.read(key: key);
    return value;
  }

  Future write(String key, String value) async {
    await _storage.write(key: key, value: value);
  }

  Future delete(String key) async {
    await _storage.delete(key: key);
  }

}