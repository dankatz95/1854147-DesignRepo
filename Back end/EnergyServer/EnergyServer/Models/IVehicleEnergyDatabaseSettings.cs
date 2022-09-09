namespace EnergyServer.Models
{
    public interface IVehicleEnergyDatabaseSettings
    {
        string DatabaseName { get; set; }
        string CarCollection { get; set; }
        string ProcessedCollection { get; set; }
        string TripCollection { get; set; }

        string StopCollection { get; set; }
        string ConnectionString { get; set; }
    }
}
