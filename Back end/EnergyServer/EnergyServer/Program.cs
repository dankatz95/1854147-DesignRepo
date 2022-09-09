using EnergyServer.Models;
using EnergyServer.Services;
using Microsoft.Extensions.Options;
using MongoDB.Driver;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<VehicleEnergyDatabaseSettings>(
    builder.Configuration.GetSection(nameof(VehicleEnergyDatabaseSettings)));

builder.Services.AddSingleton<IVehicleEnergyDatabaseSettings>(sp =>
    sp.GetRequiredService<IOptions<VehicleEnergyDatabaseSettings>>().Value);
builder.Services.AddSingleton<IMongoClient>(sp =>
    new MongoClient(builder.Configuration.GetValue<string>("VehicleEnergyDatabaseSettings:ConnectionString")));

builder.Services.AddScoped<ICarService, CarService>();

builder.Services.AddScoped<ITimeSeriesService, TimeSeriesService>();

builder.Services.AddScoped<ITripService, TripService>();

builder.Services.AddScoped<IStopService, StopService>();
// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
