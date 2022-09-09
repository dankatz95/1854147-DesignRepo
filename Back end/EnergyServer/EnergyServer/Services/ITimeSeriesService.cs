using EnergyServer.Models;

namespace EnergyServer.Services
{
    public interface ITimeSeriesService
    {
        Task<TripDataModel> GetTripData(TripSummaryModel trip);
        Task <List<TimeSeriesModel>> GetParameter(string carReg, DateTime start, DateTime end, Parameters param);

    }
}
