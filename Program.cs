using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using PROJET.Data;
using Microsoft.Extensions.DependencyInjection;
using PROJET.Models;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;


var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<PROJETContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("PROJETContext") ?? throw new InvalidOperationException("Connection string 'PROJETContext' not found.")));
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("PROJETContext") ?? throw new InvalidOperationException("Connection string 'PROJETContext' not found.")));

// Add services to the container.
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection") ?? throw new InvalidOperationException("Connection string 'DefaultConnection' not found.");
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));
builder.Services.AddDatabaseDeveloperPageExceptionFilter();

builder.Services.AddDefaultIdentity<IdentityUser>(options => options.SignIn.RequireConfirmedAccount = true)
    .AddEntityFrameworkStores<ApplicationDbContext>();
builder.Services.AddControllersWithViews();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseMigrationsEndPoint();
}
else
{
    app.UseExceptionHandler("/Home/Error");
}
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();




app.UseRouting();

app.UseEndpoints(endpoints =>
{
    endpoints.MapControllerRoute(
        name: "default",
        pattern: "{controller=Home}/{action=Index}/{id?}");
});

app.MapControllerRoute(
    name: "SaveResults",
    pattern: "/SaveResults",
    defaults: new { controller = "SaveResults", action = "SaveResults" });

app.MapControllerRoute(
    name: "SaveResults2",
    pattern: "/SaveResults2",
    defaults: new { controller = "SaveResults2", action = "SaveResults2" });




app.MapRazorPages();
using (var serviceScope = app.Services.GetService<IServiceScopeFactory>().CreateScope())
{
var context = serviceScope.ServiceProvider.GetRequiredService<PROJETContext>();
    //context.Database.EnsureDeleted();
    context.Database.EnsureCreated();
}






app.Run();
