using EnergyServer.Models;

namespace EnergyServer.Services
{
    public interface IStopService
    {
        Task<List<StopModel>> GetStops();

        Task<List<StopModel>> GetStopCar(string carReg);

        Task<List<StopModel>> GetStopCar(string carReg, DateTime start, DateTime end);
    }
}
