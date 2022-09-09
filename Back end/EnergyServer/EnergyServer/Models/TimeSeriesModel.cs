using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EnergyServer.Models
{
    public class TimeSeriesModel
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }
        public string tag { get; set; }
        [BsonRepresentation(BsonType.DateTime)]
        public DateTime timestamp { get; set; }
        public double value { get; set; }

    }
}
