using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EnergyServer.Models
{
    public enum Parameters
    {
        Velocity,
        Latitude,
        Longitude,
        Power,
        Acceleration,
        Displacement,
        Cumulative,
        Angles,
        Elevation
    }


    public class TagModel
    {
        public TagModel(string vehicleRegistration)
        {
            this.VehicleRegistration = vehicleRegistration;
        }

        private string VehicleRegistration{ get; set; }



        public string GetTag(Parameters param)
        {
            switch (param)
            {
                case Parameters.Velocity:
                    return this.VehicleRegistration + "_V";
                case Parameters.Latitude:
                    return this.VehicleRegistration + "_lat";
                case Parameters.Longitude:
                    return this.VehicleRegistration + "_lng";
                case Parameters.Power:
                    return this.VehicleRegistration + "_pow";
                case Parameters.Acceleration:
                    return this.VehicleRegistration + "_acc";
                case Parameters.Displacement:
                    return this.VehicleRegistration + "_disp";
                case Parameters.Cumulative:
                    return this.VehicleRegistration + "_cum";
                case Parameters.Angles:
                    return this.VehicleRegistration + "_ang";
                case Parameters.Elevation:
                    return this.VehicleRegistration + "_elv";
                default:
                    return "Incorrect Tag type";
            }
        }













        /*
        public string GetType()
        {
            string[] components = tag.Split("_");
            string type = components[1];
            switch (type)
            {
                case "V":
                    return "velocity";
                case "lat":
                    return "latitude";
                case "lng":
                    return "longitude";
                case "acc":
                    return "acceleration";
                case "pow":
                    return "power";
                default:
                    return "None";

            }
        }*/



    }
}
