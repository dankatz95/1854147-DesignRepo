using MongoDB.Driver;
using MongoDataAccess.Models;
using System.Collections;
using MongoDataAccess.DataAccess;


/*
var fleet = new FleetData();
//var velocity = await fleet.GetVelocityTrip("KF44LNGP", new DateTime(2022, 7, 1, 8, 19, 45), new DateTime(2022, 7, 1, 9, 33, 55));
var trip = new TripSummaryModel()
{
    VehicleRegistration = "KF44LNGP",
    start = new DateTime(2022, 07, 01, 8, 19, 45),
    end = new DateTime(2022, 7, 1, 9, 33, 55),
    duration = 4450,
    distance = 78.6053613,
    energy = 14.3508052,
    tripNumber = 0
};

var tripModel = await fleet.GetTripData(trip);

*/



//var velocity = await fleet.GetTripDay("KF44LNGP", new DateTime(2022, 7, 1));
//var velocity = await  fleet.GetTimeStamp(new DateTime(2022, 7, 1, 8, 19, 45));



string connectionString = "mongodb+srv://dankatz95:1234@energycluster.15yrxyi.mongodb.net/?retryWrites=true&w=majority";
string databaseName = "Fleet";
string collectionName = "Cars";

var client = new MongoClient(connectionString);
var db = client.GetDatabase(databaseName);


var collection = db.GetCollection<CarModel>(collectionName);

var KK65WZGP = new CarModel { VehicleRegistration = "KK65WZGP", Area= 2.59f, Mass = 1285, DragCoefficient = 0.29f, Mu = 0.02f, Make = "Toyota", Model = "Corolla", Year = 2022 };
var KF44LNGP = new CarModel { VehicleRegistration = "KF44LNGP", Area = 2.59f, Mass = 1285, DragCoefficient = 0.29f, Mu = 0.02f, Make = "Toyota", Model = "Corolla", Year = 2021 };
var KK65XRGP = new CarModel { VehicleRegistration = "KK65XRGP", Area = 2.59f, Mass = 1285, DragCoefficient = 0.29f, Mu = 0.02f, Make = "Toyota", Model = "Corolla", Year = 2021 };
var KN34FKGP = new CarModel { VehicleRegistration = "KN34FKGP", Area = 2.54f, Mass = 1254, DragCoefficient = 0.28f, Mu = 0.02f, Make = "Nissan", Model = "Almera", Year = 2022 };
var KR87GHGP = new CarModel { VehicleRegistration = "KR87GHGP", Area = 2.54f, Mass = 1254, DragCoefficient = 0.28f, Mu = 0.02f, Make = "Nissan", Model = "Almera", Year = 2022 };
var KR01YWGP = new CarModel { VehicleRegistration = "KR01YWGP", Area = 2.54f, Mass = 1254, DragCoefficient = 0.28f, Mu = 0.02f, Make = "Nissan", Model = "Almera", Year = 2022 };
await collection.InsertOneAsync(KK65WZGP);
await collection.InsertOneAsync(KF44LNGP);
await collection.InsertOneAsync(KK65XRGP);
await collection.InsertOneAsync(KN34FKGP);
await collection.InsertOneAsync(KR87GHGP);
await collection.InsertOneAsync(KR01YWGP);


var results = await collection.FindAsync(_ => true);


foreach(var result in results.ToList())
{
    Console.WriteLine($"{result.Id}: {result.VehicleRegistration}");
}


