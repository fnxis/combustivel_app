import 'package:flutter/material.dart';
import 'package:hive/hive.dart';
import '../models/fuel_entry.dart';

class NewEntryPage extends StatefulWidget {
  @override
  _NewEntryPageState createState() => _NewEntryPageState();
}

class _NewEntryPageState extends State<NewEntryPage> {
  final _formKey = GlobalKey<FormState>();
  final _litersController = TextEditingController();
  final _priceController = TextEditingController();
  final _kmController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Novo Abastecimento')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _litersController,
                decoration: InputDecoration(labelText: "Litros"),
                keyboardType: TextInputType.number,
              ),
              TextFormField(
                controller: _priceController,
                decoration: InputDecoration(labelText: "Valor (R\$)"),
                keyboardType: TextInputType.number,
              ),
              TextFormField(
                controller: _kmController,
                decoration: InputDecoration(labelText: "Quilometragem"),
                keyboardType: TextInputType.number,
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  final liters = double.parse(_litersController.text);
                  final price = double.parse(_priceController.text);
                  final km = double.parse(_kmController.text);

                  final entry = FuelEntry(
                    date: DateTime.now(),
                    liters: liters,
                    price: price,
                    kilometers: km,
                  );

                  Hive.box<FuelEntry>('fuelBox').add(entry);
                  Navigator.pop(context);
                },
                child: Text("Salvar"),
              )
            ],
          ),
        ),
      ),
    );
  }
}
