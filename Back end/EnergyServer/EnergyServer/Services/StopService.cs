using EnergyServer.Models;
using MongoDB.Driver;

namespace EnergyServer.Services
{
    public class StopService : IStopService
    {
        private readonly IMongoCollection<StopModel> _stops;

        public StopService(IVehicleEnergyDatabaseSettings settings, IMongoClient mongoClient)
        {
            var db = mongoClient.GetDatabase(settings.DatabaseName);
            _stops = db.GetCollection<StopModel>(settings.StopCollection);
        }

        public async Task<List<StopModel>> GetStops()
        {
            var results = await _stops.FindAsync(_ => true);
            return results.ToList();
        }

        public async Task<List<StopModel>> GetStopCar(string carReg)
        {
            var results = await _stops.FindAsync(c => c.VehicleRegistration == carReg);
            return results.ToList();
        }
        public async Task<List<StopModel>> GetStopCar(string carReg, DateTime start, DateTime end)
        {
            var builder = Builders<StopModel>.Filter;
            var filter = builder.Eq("VehicleRegistration", carReg) & builder.Gte("start", start.AddHours(2)) & builder.Lte("end", end.AddHours(2));
            var results = await _stops.FindAsync(filter);
            return results.ToList();
        }
    }
}
