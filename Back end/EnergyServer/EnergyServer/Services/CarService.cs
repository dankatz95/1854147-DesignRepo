using EnergyServer.Models;
using MongoDB.Driver;

namespace EnergyServer.Services
{
    public class CarService : ICarService
    {
        private readonly IMongoCollection<CarModel> _cars;

        public CarService(IVehicleEnergyDatabaseSettings settings, IMongoClient mongoClient)
        {
            var db = mongoClient.GetDatabase(settings.DatabaseName);
            _cars = db.GetCollection<CarModel>(settings.CarCollection);
        }
        public async Task Post(CarModel car)
        {
            await _cars.InsertOneAsync(car);
        }

        public async Task<CarModel> Get(string VehReg)
        {
            var results = await _cars.FindAsync(c => c.VehicleRegistration == VehReg);
            return results.FirstOrDefault();
           
        }

        public async Task<List<CarModel>>Get()
        {
            var results = await _cars.FindAsync(_ => true);
            return results.ToList();
        }

        public async Task Put(CarModel car)
        {
            var filter = Builders<CarModel>.Filter.Eq("VehicleRegistration", car.VehicleRegistration);
            await _cars.ReplaceOneAsync(filter, car, new ReplaceOptions { IsUpsert = true });
        }
    }
}
