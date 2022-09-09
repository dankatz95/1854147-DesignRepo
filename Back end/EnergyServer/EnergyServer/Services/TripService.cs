using EnergyServer.Models;
using MongoDB.Driver;

namespace EnergyServer.Services
{
    public class TripService : ITripService
    {
        private readonly IMongoCollection<TripSummaryModel> _trips;
        private readonly IMongoCollection<TimeSeriesModel> _clean;

        public TripService(IVehicleEnergyDatabaseSettings settings, IMongoClient mongoClient)
        {
            var db = mongoClient.GetDatabase(settings.DatabaseName);
            _trips = db.GetCollection<TripSummaryModel>(settings.TripCollection);

            _clean = db.GetCollection<TimeSeriesModel>(settings.ProcessedCollection);
        }


        public async Task<List<TripSummaryModel>> GetTrips()
        {
            var results = await _trips.FindAsync(_ => true);
            return results.ToList();
        }

        public async Task<List<TripSummaryModel>> GetTripsForCar(string carReg)
        {
            var results = await _trips.FindAsync(c => c.VehicleRegistration == carReg);
            return results.ToList();
        }

        public async Task<List<TripSummaryModel>> GetTripsForCar(string carReg, DateTime start, DateTime end)
        {
            var builder = Builders<TripSummaryModel>.Filter;
            var filter = builder.Eq("VehicleRegistration", carReg) & builder.Gte("start", start.AddHours(2)) & builder.Lte("end", end.AddHours(2));
            var results = await _trips.FindAsync(filter);
            return results.ToList();
        }
    }
}
