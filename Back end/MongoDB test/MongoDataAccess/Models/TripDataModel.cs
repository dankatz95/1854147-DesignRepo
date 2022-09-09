using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MongoDataAccess.Models;

namespace MongoDataAccess.Models
{
    public class TripDataModel
    {
        public TripDataModel(TripSummaryModel trip)
        {
            this.Id = $"{trip.VehicleRegistration}_{trip.start.Year}-{trip.start.Month}-{trip.start.Day}_{trip.tripNumber}";
        }
        public string Id { get; set; }
        public List<TimeStampModel> velocityStamps { get; set; }
        public List<TimeStampModel> latitudeStamps { get; set; }
        public List<TimeStampModel> longitudeStamps { get; set; }
        public List<TimeStampModel> powerStamps { get; set; }
        public List<TimeStampModel> accelerationStamps { get; set; }

        private List<double> getValues(Parameters param)
        {
            List<TimeStampModel> temp = new List<TimeStampModel>();
            
            switch (param)
            {
                case Parameters.Velocity:
                    temp = this.velocityStamps;
                    break;
                case Parameters.Latitude:
                    temp = this.latitudeStamps;
                    break;
                case Parameters.Longitude:
                    temp = this.longitudeStamps;
                    break;
                case Parameters.Power:
                    temp = this.powerStamps;
                    break;
                case Parameters.Acceleration:
                    temp = this.accelerationStamps;
                    break;
                default:
                    throw new InvalidOperationException();
            }
            var values = new List<double>();

            foreach(var x in temp)
            {
                values.Add(x.value);
            }

            return values;
        }

        private List<DateTime> getTime()
        {
            var time = new List<DateTime>();

            foreach(var x in this.velocityStamps)
            {
                time.Add(x.timestamp);
            }
            return time;
        }



    }
}
