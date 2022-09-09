namespace EnergyServer.Models
{
    public class VehicleEnergyDatabaseSettings : IVehicleEnergyDatabaseSettings
    {
        public string DatabaseName { get; set ; }
        public string CarCollection { get ; set ; }
        public string ProcessedCollection { get ; set ; }
        public string TripCollection { get ; set ; }
        public string StopCollection { get ; set ; }
        public string ConnectionString { get ; set ; }


    }
}
