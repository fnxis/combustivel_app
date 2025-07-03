import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../models/fuel_entry.dart';
import 'new_entry_page.dart';

class HomePage extends StatelessWidget {
  final Box<FuelEntry> fuelBox = Hive.box<FuelEntry>('fuelBox');

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Gastos com Combustível')),
      body: ValueListenableBuilder(
        valueListenable: fuelBox.listenable(),
        builder: (context, Box<FuelEntry> box, _) {
          if (box.values.isEmpty) {
            return Center(child: Text("Nenhum abastecimento registrado."));
          }

          return ListView.builder(
            itemCount: box.length,
            itemBuilder: (context, index) {
              final entry = box.getAt(index)!;
              return ListTile(
                title: Text(
                    "${entry.liters.toStringAsFixed(1)} L - R\$ ${entry.price.toStringAsFixed(2)}"),
                subtitle: Text(
                    "${entry.date.day}/${entry.date.month} - ${entry.kmPerLiter.toStringAsFixed(2)} km/L"),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(context,
              MaterialPageRoute(builder: (_) => NewEntryPage()));
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
