using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace MongoDataAccess.Models
{
    public class CarModel
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }
        public string VehicleRegistration { get; set; }
        public float Area { get; set; }
        public int Mass { get; set; }
        public float DragCoefficient { get; set; }
        public float Mu { get; set; } = 0.02f;
        public string Make { get; set; }
        public string Model { get; set; }
        public int Year { get; set; }

    }
}
