using EnergyServer.Models;
using EnergyServer.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace EnergyServer.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class StopController : ControllerBase
    {
        private readonly IStopService stopService;

        public StopController(IStopService stopService)
        {
            this.stopService = stopService;
        }
        // GET: api/<StopController>
        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var stops = await stopService.GetStops();

            if(stops == null)
            {
                return NotFound();
            }

            return Ok(stops);
        }

        // GET api/<StopController>/5
        [HttpGet("{carReg}")]
        public async Task<IActionResult> Get(string carReg)
        {
            var stops = await stopService.GetStopCar(carReg);

            if(stops == null)
            {
                return NotFound();
            }

            return Ok(stops);
        }

        // POST api/<StopController>
        [HttpPost]  
        public async Task<IActionResult> GetStopDate([FromBody] CarDate stopInfo)
        {
            var stops = await stopService.GetStopCar(stopInfo.CarReg, stopInfo.start, stopInfo.end);
            if (stops == null) { return NotFound(); }
            return Ok(stops);

        }

        // PUT api/<StopController>/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE api/<StopController>/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }
    }
}
