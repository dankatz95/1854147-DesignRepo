using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using EnergyServer.Models;

namespace EnergyServer.Models
{
    public class TripDataModel
    {
        public TripDataModel(TripSummaryModel trip)
        {
            this.Id = $"{trip.VehicleRegistration}_{trip.start.Year}_{trip.start.Month}_{trip.start.Day}_{trip.tripNumber}";
        }
        public TripDataModel(CarDate carDate)
        {
            this.Id = $"{carDate.CarReg}_{carDate.start.Year}_{carDate.start.Month}_{carDate.start.Day}";
        }

        public string Id { get; set; }
        public List<double> velocityStamps { get; set; }  
        public List<double> latitudeStamps { get; set; }
        public List<double> longitudeStamps { get; set; }
        public List<double> powerStamps { get; set; }
        public List<double> accelerationStamps { get; set; }

        public List<DateTime> timestamps { get; set; }


        public static List<double> getValues(List<TimeSeriesModel> column)
        {
            var values = new List<double>();

            foreach (var x in column)
            {
                values.Add(x.value);
            }

            return values;
        }

        public static List<DateTime> getTime(List<TimeSeriesModel> column)
        {
            var values = new List<DateTime>();

            foreach (var x in column)
            {
                values.Add(x.timestamp);
            }

            return values;
        }

    }
}
