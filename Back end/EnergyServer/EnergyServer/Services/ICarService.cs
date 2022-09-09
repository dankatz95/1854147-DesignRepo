using EnergyServer.Models;

namespace EnergyServer.Services
{
    public interface ICarService
    {
        Task<List<CarModel>> Get();
        Task<CarModel> Get(string VehReg);
        Task Post(CarModel car);
        Task Put(CarModel car);

    }
}
