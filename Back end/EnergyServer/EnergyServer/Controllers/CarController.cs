using EnergyServer.Models;
using EnergyServer.Services;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace EnergyServer.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CarController : ControllerBase
    {
        private readonly ICarService carService;

        public CarController(ICarService carService)
        {
            this.carService = carService;
        }
        // GET: api/<CarController>
        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var cars = await carService.Get();

            if(cars == null)
            {
                return NotFound();
            }

            return Ok(cars);
        }

        // GET api/<CarController>/5
        [HttpGet("{carReg}")]
        public async Task<IActionResult> Get(string carReg)
        {
            var car = await carService.Get(carReg);
            if(car == null)
            {
                return NotFound();
            }

            return Ok(car);
        }

        // POST api/<CarController>
        [HttpPost]
        public async Task<IActionResult> Post([FromBody] CarModel car)
        {
            await carService.Post(car);

            return CreatedAtAction(nameof(Get), new { id = car.VehicleRegistration }, car);
        }

        // PUT api/<CarController>/5
        [HttpPut]
        public async Task<IActionResult> Put([FromBody] CarModel car)
        {
            var res = await carService.Get(car.VehicleRegistration);

            if (res is null)
            {
                return NotFound();
            }

            await carService.Put(car);

            return NoContent();
        }

        // DELETE api/<CarController>/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }
    }
}
