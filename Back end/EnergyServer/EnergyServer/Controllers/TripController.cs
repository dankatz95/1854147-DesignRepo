using EnergyServer.Models;
using EnergyServer.Services;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace EnergyServer.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TripController : ControllerBase
    {
        private readonly ITripService tripService;

        public TripController(ITripService tripService)
        {
            this.tripService = tripService;
        }

        // GET: api/<TripController>
        [HttpGet]
        public async Task<IActionResult> Get()
        {
           var trips = await tripService.GetTrips();

            if(trips == null)
            {
                return NotFound();
            }

            return Ok(trips);
        }

        // GET api/<TripController>/5
        [HttpGet("{id}")]
        public async Task<IActionResult> Get(string id)
        {
            var trip = await tripService.GetTripsForCar(id);
            if(trip == null)
            {
                return NotFound();
            }

            return Ok(trip);
        }

        [HttpPost]
        public async Task<IActionResult> GetTripDate([FromBody] CarDate tripInfo)
        {
            var results = await tripService.GetTripsForCar(tripInfo.CarReg, tripInfo.start, tripInfo.end);

            if(results == null) { return NotFound(); }
            return Ok(results);
        }

        // PUT api/<TripController>/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE api/<TripController>/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }
    }
}
