using Microsoft.AspNetCore.Mvc;
using PROJET.Models;
using PROJET.Data;
using System;
using System.IO;
using System.Linq;

namespace PROJET.Controllers
{
    public class SaveResultsController : Controller
    {
        private readonly PROJETContext _dbContext;

        public SaveResultsController(PROJETContext dbContext)
        {
            _dbContext = dbContext;
        }

        [HttpPost]
        public IActionResult SaveResults(SaveResultsModel model)
        {
            DateTime currentTime = DateTime.Now;
            model.Heure = currentTime;

            if (float.TryParse(Request.Form["accuracyR"], out float accuracyR))
            {
                // Assign the value of accuracyR to accuracy
                model.Accuracy = accuracyR;
                if (model.Accuracy<=1)
                {
                    model.Accuracy = model.Accuracy * 100;
                }
            }

            if (int.TryParse(Request.Form["idM"], out int idM))
            {
                // Assign the value of idM to MethodeId
                model.MethodeId = idM;
            }

            

            // Create an instance of Sauvegarde entity
            var sauvegarde = new Sauvegarde
            {
                Accuracy = model.Accuracy,
                Heure = currentTime,
                methodeId = model.MethodeId
            };

            // Add the sauvegarde entity to the DbSet of your context
            _dbContext.Sauvegarde.Add(sauvegarde);
            _dbContext.SaveChanges(); // Save changes to get the generated IdSauvegarde

            // Get the generated IdSauvegarde
            int newIdSauvegarde = sauvegarde.IdSauvegarde;

            // Create a string representation of the data
            string data = $"\n__________\nIdSauvegarde: '{model.MethodeId}' and '{newIdSauvegarde}\nAccuracy: {model.Accuracy}\nTime: {model.Heure}\n";

            // Save the data to a .txt file
            string fileName = "SaveResultsFile.txt";
            string desktopFolder = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            string filePath = Path.Combine(desktopFolder, fileName);

            using (StreamWriter writer = new StreamWriter(filePath, true))
            {
                writer.WriteLine(data);
            }

            // Create instances of Histo_Hparam entities and add them to the context
            if (model.MethodeId != 1)
            {
                foreach (var hParam in model.ListHParam)
                {
                    var histoHparam = new Histo_Hparam
                    {
                        IdSauvegarde = newIdSauvegarde,
                        IdHParam = hParam.Id,
                        SelectedValue = hParam.Value
                    };
                    data = $"\nIdS : '{newIdSauvegarde}' and IDHP : '{hParam.Id} & Value: {hParam.Value}";
                    using (StreamWriter writer = new StreamWriter(filePath, true))
                    {
                        writer.WriteLine(data);
                    }
                    _dbContext.Histo_Hparam.Add(histoHparam);
                }

                _dbContext.SaveChanges(); // Save changes to add Histo_Hparam records
            }
            


            // Redirect back to the homepage or any other page
            return RedirectToAction("Index", "Home");
        }
    }
}
