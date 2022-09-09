using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Bson;

namespace EnergyServer.Models
{
    public class StopModel
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string? Id { get; set; }
        public string VehicleRegistration { get; set; }
        [BsonRepresentation(BsonType.DateTime)]
        public DateTime start { get; set; }
        [BsonRepresentation(BsonType.DateTime)]
        public DateTime end { get; set; }
        [BsonRepresentation(BsonType.Double, AllowTruncation = true)]
        public double latitude { get; set; }
        [BsonRepresentation(BsonType.Double, AllowTruncation = true)]
        public double longitude { get; set; }
        public int duration { get; set; }
        [BsonRepresentation(BsonType.Double, AllowTruncation = true)]
        public int stopNumber { get; set; }
    }
}
