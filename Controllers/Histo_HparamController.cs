using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PROJET.Data;
using PROJET.Models;

namespace PROJET.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class Histo_HparamController : ControllerBase
    {
        private readonly PROJETContext _dbContext;

        public Histo_HparamController(PROJETContext context)
        {
            _dbContext = context;
        }

        /*
        // GET: api/Histo_Hparam
        [HttpPost]
        public IActionResult SaveResults(Histo_Hparam model)
        {
            if (int.TryParse(Request.Form["Hparam1"], out int hParamL))
            {
                // Assign the value of accuracyR to accuracy
                model.IdHParam = hParamL;
            }

            // Get the last generated IdSauvegarde
            int lastIdSauvegarde = _dbContext.Sauvegarde.OrderByDescending(s => s.IdSauvegarde).Select(s => s.IdSauvegarde).FirstOrDefault();

            // Increment the IdSauvegarde by 1
            int newIdSauvegarde = lastIdSauvegarde + 1;

            // Create an instance of Histo_Hparam entity
            var histoHparam = new Histo_Hparam
            {
                IdSauvegarde = newIdSauvegarde,
                IdHParam = model.IdHParam,
                SelectedValue = model.SelectedValue
            };

            // Add the histoHparam entity to the DbSet of your context
            _dbContext.Histo_Hparam.Add(histoHparam);

            // Save changes to the database
            _dbContext.SaveChanges();

            DateTime currentTime = DateTime.Now;
            // Create a string representation of the data
            string data = $"\nHParam IdSauvegarde: {newIdSauvegarde}\nTime: {currentTime}\n________\n";
            // Save the data to a .txt file
            string filePath = "C:\\Users\\cafes\\Documents\\Visual Studio 2022\\SaveResultsFile.txt"; // Provide the actual file path
            using (StreamWriter writer = new StreamWriter(filePath, true))
            {
                writer.WriteLine(data);
            }


            // Redirect back to the homepage or any other page
            return RedirectToAction("Index", "Home");
        }*/
    }
}
