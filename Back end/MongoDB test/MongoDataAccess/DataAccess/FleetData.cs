using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MongoDB.Driver;
using MongoDataAccess.Models;

namespace MongoDataAccess.DataAccess
{
    public class FleetData
    {
        private const string ConnectionString = "mongodb://localhost:27017";
        private const string DatabaseName = "fleet";
        private const string CarCollection = "Cars";
        private const string ProcessedCollection = "Clean";
        private const string TripCollection = "Trips";

        private IMongoCollection<T> ConnectToMongo<T>(in string collection)
        {
            var client = new MongoClient(ConnectionString);
            var db = client.GetDatabase(DatabaseName);
            return db.GetCollection<T>(collection);
        }

        public async Task<List<CarModel>> GetAllCars()
        {
            var carsCollection = ConnectToMongo<CarModel>(CarCollection);
            var results = await carsCollection.FindAsync(_ => true);
            return results.ToList();
        }

        public async Task<List<CarModel>> GetCarByReg(string VehReg)
        {
            var carsCollection = ConnectToMongo<CarModel>(CarCollection);
            var results = await carsCollection.FindAsync(c => c.VehicleRegistration == VehReg);
            return results.ToList();
        }

        public Task CreateCar(CarModel car)
        {
            var carsCollection = ConnectToMongo<CarModel>(CarCollection);
            return carsCollection.InsertOneAsync(car);
        }

        public Task UpdateCar(CarModel car)
        {
            var carsCollection = ConnectToMongo<CarModel>(CarCollection);
            var filter = Builders<CarModel>.Filter.Eq("VehicleRegistration", car.VehicleRegistration);
            return carsCollection.ReplaceOneAsync(filter, car, new ReplaceOptions { IsUpsert = true });
        }

        public async Task<List<TripSummaryModel>> GetAllTrips()
        {
            var tripCollection = ConnectToMongo<TripSummaryModel>(TripCollection);
            var results = await tripCollection.FindAsync(_ => true);
            return results.ToList();
        }
        
        public async Task<List<TripSummaryModel>> GetTripsForCar(string vehReg)
        {
            var tripCollection = ConnectToMongo<TripSummaryModel>(TripCollection);
            var results = await tripCollection.FindAsync(c => c.VehicleRegistration == vehReg);
            return results.ToList();
        }


        public async Task<List<TripSummaryModel>> GetTripDay(string vehReg, DateTime day)
        {
            var tripCollection = ConnectToMongo<TripSummaryModel>(TripCollection);
            var builder = Builders<TripSummaryModel>.Filter;
            var filter = builder.Eq("VehicleRegistration", vehReg) & builder.Gte("start", day) & builder.Lt("end", day.AddDays(1));
            var results = await tripCollection.FindAsync(filter);
            return results.ToList();
        }


        public async Task<List<TimeStampModel>> GetVelocityTrip(string vehReg, DateTime start, DateTime end)
        {
            string tag = vehReg + "_V";

            Console.WriteLine(tag);

            var TimeSeriesCollections = ConnectToMongo<TimeStampModel>(ProcessedCollection);
            var builder = Builders<TimeStampModel>.Filter;
            var filter = builder.Eq("tag", tag) & builder.Gte("timestamp", start.AddHours(2)) & builder.Lte("timestamp", end.AddHours(2));
            var results = await TimeSeriesCollections.FindAsync(filter);
            return results.ToList();
        }
        public async Task<List<TimeStampModel>> GetCar(string vehReg)
        {
            string tag = vehReg + "_V";
            var TimeSeriesCollections = ConnectToMongo<TimeStampModel>(ProcessedCollection);
            var results = await TimeSeriesCollections.FindAsync((c) => c.tag.Equals(tag));

            return results.ToList();
        }
        
        public async Task<TripDataModel> GetTripData(TripSummaryModel trip)
        {
            var tag = new TagModel(trip.VehicleRegistration);
            var velocity = tag.GetTag(Parameters.Velocity);
            var latitude = tag.GetTag(Parameters.Latitude);
            var longitude = tag.GetTag(Parameters.Longitude);
            var power = tag.GetTag(Parameters.Power);
            var acceleration = tag.GetTag(Parameters.Acceleration);

            var paramList = new List<string>() { velocity, latitude, longitude, power, acceleration };



            var clean = ConnectToMongo<TimeStampModel>(ProcessedCollection);
            var builder = Builders<TimeStampModel>.Filter;

            var resultArray = new List<List<TimeStampModel>>();

            TripDataModel export = new TripDataModel(trip);

            foreach(var param in paramList)
            {
                var filter = builder.Eq("tag", param) & builder.Gte("timestamp", trip.start.AddHours(2)) & builder.Lte("timestamp", trip.end.AddHours(2));
                var results = await clean.FindAsync(filter);
                resultArray.Add(results.ToList());

            }

            for(var i = 0; i < resultArray.Count; i++)
            {
                switch (i)
                {
                    case 0:
                        export.velocityStamps = resultArray[i];
                        break;
                    case 1:
                        export.latitudeStamps = resultArray[i];
                        break;
                    case 2:
                        export.longitudeStamps = resultArray[i];
                        break;
                    case 3:
                        export.powerStamps = resultArray[i];
                        break;
                    case 4:
                        export.accelerationStamps = resultArray[i];
                        break;
                    default:
                        break;
                }
            }  
            
            return export;

        } 



    }


}
