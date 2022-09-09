using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Bson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections;

namespace EnergyServer.Models
{
    public class TripSummaryModel
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string? Id { get; set; }
        public string VehicleRegistration { get; set; }
        [BsonRepresentation(BsonType.DateTime)]
        public DateTime start { get; set; }
        [BsonRepresentation(BsonType.DateTime)]
        public DateTime end { get; set; }
        public int duration {get; set; }
        [BsonRepresentation(BsonType.Double, AllowTruncation =true)]
        public double distance { get; set; }
        public double energy { get; set; }
        public int tripNumber { get; set; }


    }
}
