using EnergyServer.Models;
using EnergyServer.Services;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace EnergyServer.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TimeSeriesController : ControllerBase
    {
        private readonly ITimeSeriesService time;

        public TimeSeriesController(ITimeSeriesService time)
        {
            this.time = time;
        }
        // GET: api/<TimeSeriesController>
        [HttpPost]
        public async Task<IActionResult> GetTrip([FromBody] TripSummaryModel _trip)
        {
            var trip = await time.GetTripData(_trip);

            if(trip == null)
            {
                return NotFound();
            }
            return Ok(trip);
        }

        /*
        // GET api/<TimeSeriesController>/5
        [HttpPost]
        public async Task<IActionResult> GetParameter([FromBody] CarDate car)
        {
            var trip = await time.GetParameter(car.CarReg, car.start, car.end, (Parameters) car.param);

            if(trip == null)
            {
                return NotFound();
            }

            return Ok(trip);
        }

        // POST api/<TimeSeriesController>
        */
    }
}
