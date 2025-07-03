import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'models/fuel_entry.dart';
import 'pages/home_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  Hive.registerAdapter(FuelEntryAdapter());
  await Hive.openBox<FuelEntry>('fuelBox');

  runApp(MaterialApp(
    home: HomePage(),
    debugShowCheckedModeBanner: false,
  ));
}
