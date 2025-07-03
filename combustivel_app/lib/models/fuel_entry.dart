import 'package:hive/hive.dart';

part 'fuel_entry.g.dart';

@HiveType(typeId: 0)
class FuelEntry extends HiveObject {
  @HiveField(0)
  DateTime date;

  @HiveField(1)
  double liters;

  @HiveField(2)
  double price;

  @HiveField(3)
  double kilometers;

  FuelEntry({
    required this.date,
    required this.liters,
    required this.price,
    required this.kilometers,
  });

  double get kmPerLiter => kilometers = liters;
}
