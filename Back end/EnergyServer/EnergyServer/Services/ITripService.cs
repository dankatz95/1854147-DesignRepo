using EnergyServer.Models;

namespace EnergyServer.Services
{
    public interface ITripService
    {
        Task<List<TripSummaryModel>> GetTrips();
        Task <List<TripSummaryModel>> GetTripsForCar(string carReg);

        Task <List<TripSummaryModel>> GetTripsForCar(string carReg, DateTime start, DateTime end);

    }
}
