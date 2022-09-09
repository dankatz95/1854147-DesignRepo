using EnergyServer.Models;
using MongoDB.Driver;
using MongoDB.Driver.Core.Configuration;

namespace EnergyServer.Services
{
    public class TimeSeriesService : ITimeSeriesService
    {
        private readonly IMongoCollection<TimeSeriesModel> _clean;

        public TimeSeriesService(IVehicleEnergyDatabaseSettings settings, IMongoClient mongoClient)
        {
            var db = mongoClient.GetDatabase(settings.DatabaseName);
            _clean = db.GetCollection<TimeSeriesModel>(settings.ProcessedCollection);
        }

        public async Task<List<TimeSeriesModel>> GetParameter(string carReg, DateTime start, DateTime end, Parameters param)
        {
            var tag = new TagModel(carReg).GetTag(param);
            var builder = Builders<TimeSeriesModel>.Filter;
            var filter = builder.Eq("tag",tag) & builder.Gte("timestamp", start.AddHours(2)) & builder.Lte("timestamp", end.AddHours(2));
            var results = await _clean.FindAsync(filter);
            return results.ToList();
        }


        public async Task<TripDataModel> GetTripData(TripSummaryModel tripSummary)
        {
            var tag = new TagModel(tripSummary.VehicleRegistration);
            var velocity = tag.GetTag(Parameters.Velocity);
            var latitude = tag.GetTag(Parameters.Latitude);
            var longitude = tag.GetTag(Parameters.Longitude);
            var power = tag.GetTag(Parameters.Power);
            var acceleration = tag.GetTag(Parameters.Acceleration);

            var paramList = new List<string>() { velocity, latitude, longitude, power, acceleration };



            var builder = Builders<TimeSeriesModel>.Filter;

            var resultArray = new List<List<TimeSeriesModel>>();

            TripDataModel export = new TripDataModel(tripSummary);

            foreach (var param in paramList)
            {
                var filter = builder.Eq("tag", param) & builder.Gte("timestamp", tripSummary.start.AddHours(2)) & builder.Lte("timestamp", tripSummary.end.AddHours(2));
                var results = await _clean.FindAsync(filter);
                resultArray.Add(results.ToList());

            }

            for (var i = 0; i < resultArray.Count; i++)
            {
                switch (i)
                {
                    case 0:
                        export.velocityStamps = TripDataModel.getValues(resultArray[i]);
                        export.timestamps = TripDataModel.getTime(resultArray[i]);
                        break;
                    case 1:
                        export.latitudeStamps = TripDataModel.getValues(resultArray[i]);
                        break;
                    case 2:
                        export.longitudeStamps = TripDataModel.getValues(resultArray[i]);
                        break;
                    case 3:
                        export.powerStamps = TripDataModel.getValues(resultArray[i]);
                        break;
                    case 4:
                        export.accelerationStamps = TripDataModel.getValues(resultArray[i]);
                        break;
                    default:
                        break;
                }
            }

            return export;
        }

 
    }
}
