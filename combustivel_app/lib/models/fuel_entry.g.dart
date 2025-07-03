// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'fuel_entry.dart';

// **************************************************************************
// TypeAdapterGenerator
// **************************************************************************

class FuelEntryAdapter extends TypeAdapter<FuelEntry> {
  @override
  final int typeId = 0;

  @override
  FuelEntry read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return FuelEntry(
      date: fields[0] as DateTime,
      liters: fields[1] as double,
      price: fields[2] as double,
      kilometers: fields[3] as double,
    );
  }

  @override
  void write(BinaryWriter writer, FuelEntry obj) {
    writer
      ..writeByte(4)
      ..writeByte(0)
      ..write(obj.date)
      ..writeByte(1)
      ..write(obj.liters)
      ..writeByte(2)
      ..write(obj.price)
      ..writeByte(3)
      ..write(obj.kilometers);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is FuelEntryAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
