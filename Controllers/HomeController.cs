using Microsoft.AspNetCore.Mvc;
using PROJET.Models;
using System.Diagnostics;
using Newtonsoft.Json;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Scripting.Hosting;
using PROJET.Data;
using Microsoft.EntityFrameworkCore;
using PROJET;

namespace PROJET.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        [HttpPost]
        public async Task<IActionResult> Analytical()
        {
            using (var client = new HttpClient())
            {

                var content = new StringContent(JsonConvert.SerializeObject(null), System.Text.Encoding.UTF8, "application/json");
                var response = await client.PostAsync("http://localhost:5000/analytical", content);
                var result = await response.Content.ReadAsStringAsync();
                var meth = "Tabry1";

                ViewBag.Result = result;
                ViewBag.Metho = meth;
            }

            return View("Page2");
        }

        [HttpPost]
        public async Task<IActionResult> RFClassifier(string hyperparameter1, string hyperparameter2)
        {
            using (var client = new HttpClient())
            {
                var requestData = new
                {
                   Hyperparameter1 =  hyperparameter1,

                   Hyperparameter2 = hyperparameter2
                };
                
                var content = new StringContent(JsonConvert.SerializeObject(requestData), System.Text.Encoding.UTF8, "application/json");
                var response = await client.PostAsync("http://localhost:5000/RFClassifier", content);
                var result1 = await response.Content.ReadAsStringAsync();
                
                ViewBag.Hyperparameter1 = hyperparameter1;
                ViewBag.Hyperparameter2 = hyperparameter2;
                ViewBag.Result1 = result1; //Resultat Random Forest
            }

            return View("ResultMethode1");
        }


        [HttpPost]
        public async Task<IActionResult> LRClassifier(string selectedItem1, string hyperparameter1, string selectedItem2)
        {
            using (var client = new HttpClient())
            {
                var requestData = new
                {
                    Hyperparameter1 = selectedItem1,

                    Hyperparameter2 = hyperparameter1,

                    Hyperparameter3 = selectedItem2
                };

                var content = new StringContent(JsonConvert.SerializeObject(requestData), System.Text.Encoding.UTF8, "application/json");
                var response = await client.PostAsync("http://localhost:5000/LRClassifier", content);
                var result2 = await response.Content.ReadAsStringAsync();

                ViewBag.Hyperparameter1 = selectedItem1;
                ViewBag.Hyperparameter2 = hyperparameter1;
                ViewBag.Hyperparameter3 = selectedItem2;
                ViewBag.Result2 = result2;
            }

            return View("ResultMethode2");
        }


        [HttpPost]
        public async Task<IActionResult> SVCClassifier(string selectedItem1, string hyperparameter1, string hyperparameter2, string hyperparameter3, string hyperparameter4, string selectedItem2)
        {
            using (var client = new HttpClient())
            {
                var requestData = new
                {
                    Hyperparameter1 = selectedItem1,

                    Hyperparameter2 = hyperparameter1,

                    Hyperparameter3 = hyperparameter2,

                    Hyperparameter4 = hyperparameter3,

                    Hyperparameter5 = hyperparameter4,

                    Hyperparameter6 = selectedItem2
                };

                var content = new StringContent(JsonConvert.SerializeObject(requestData), System.Text.Encoding.UTF8, "application/json");
                var response = await client.PostAsync("http://localhost:5000/SVCClassifier", content);
                var result3 = await response.Content.ReadAsStringAsync();

                ViewBag.Hyperparameter1 = selectedItem1;
                ViewBag.Hyperparameter2 = hyperparameter1;
                ViewBag.Hyperparameter3 = hyperparameter2;
                ViewBag.Hyperparameter4 = hyperparameter3;
                ViewBag.Hyperparameter5 = hyperparameter4;
                ViewBag.Hyperparameter6 = selectedItem2;
                ViewBag.Result3 = result3;
            }

            return View("ResultMethode3");
        }


        [HttpPost]
        public async Task<IActionResult> KNNClassifier(string hyperparameter1, string selectedItem1, string selectedItem2, string selectedItem3)
        {
            using (var client = new HttpClient())
            {
                var requestData = new
                {
                    Hyperparameter1 = hyperparameter1,

                    Hyperparameter2 = selectedItem1,

                    Hyperparameter3 = selectedItem2,

                    Hyperparameter4 = selectedItem3
                };

                var content = new StringContent(JsonConvert.SerializeObject(requestData), System.Text.Encoding.UTF8, "application/json");
                var response = await client.PostAsync("http://localhost:5000/KNNClassifier", content);
                var result4 = await response.Content.ReadAsStringAsync();

                ViewBag.Hyperparameter1 = hyperparameter1;
                ViewBag.Hyperparameter2 = selectedItem1;
                ViewBag.Hyperparameter3 = selectedItem2;
                ViewBag.Hyperparameter4 = selectedItem3;
           
                ViewBag.Result4 = result4;
            }

            return View("ResultMethode4");
        }

        [HttpPost]
        public async Task<IActionResult> Graph(string methode1, string methode2, string hyperparameter1, string hyperparameter2,string methode3, string selectedItem1, string hyperparameter3, string selectedItem2, string methode4, string selectedItem3, string hyperparameter4, string hyperparameter5, string hyperparameter6, string hyperparameter7, string selectedItem4, string methode5, string hyperparameter8, string selectedItem5, string selectedItem6, string selectedItem7)
        {
            using (var client = new HttpClient())
            {
                var requestData = new
                {
                    Hyperparameter1 = methode1,

                    Hyperparameter2 = methode2,

                    Hyperparameter3 = hyperparameter1,

                    Hyperparameter4 = hyperparameter2,

                    Hyperparameter5 = methode3,

                    Hyperparameter6 = selectedItem1,

                    Hyperparameter7 = hyperparameter3,

                    Hyperparameter8 = selectedItem2,

                    Hyperparameter9 = methode4,

                    Hyperparameter10 = selectedItem3,

                    Hyperparameter11 = hyperparameter4,

                    Hyperparameter12 = hyperparameter5,

                    Hyperparameter13 = hyperparameter6,

                    Hyperparameter14 = hyperparameter7,

                    Hyperparameter15 = selectedItem4,

                    Hyperparameter16 = methode5,

                    Hyperparameter17 = hyperparameter8,

                    Hyperparameter18 = selectedItem5,

                    Hyperparameter19 = selectedItem6,

                    Hyperparameter20 = selectedItem7


                };

                var content = new StringContent(JsonConvert.SerializeObject(requestData), System.Text.Encoding.UTF8, "application/json");
                var response = await client.PostAsync("http://localhost:5000/Graph", content);
                var result5 = await response.Content.ReadAsStringAsync();

               

                ViewBag.Result5 = result5;
            }

            return View("Comparegraph");
        }


       




        public IActionResult Index()
        {
             return View();
            
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }

        public IActionResult Page2()
         {
            return View();
        }

        public IActionResult Page3()
        {
            return View();
        }
        public IActionResult Page4()
        {
            return View();
        }

        public IActionResult Page5()
        {
            return View();
        }
        public IActionResult Page6()
        {
            return View();
        }



        public IActionResult ResultMethode1()
        {
          return View();

         }

        public IActionResult ResultMethode2()
        {
            return View();

        }

        public IActionResult ResultMethode3()
        {
            return View();

        }
        public IActionResult ResultMethode4()
        {
            return View();

        }


        public IActionResult Comparaison()
        {
            return View();

        }

  
        public IActionResult Comparegraph()
        {
            return View();

        }

       

        [HttpPost]
        public IActionResult Hyperparameter(Hyperparamètres model)
        {
            //int hyperparameter1Value = model.Hyperparameter1;
            // int hyperparameter2Value = model.Hyperparameter2;

            string? NomHParam = model.NomHParam;
           // Effectuer les traitements nécessaires en fonction des valeurs des hyperparamètres

           // Rediriger l'utilisateur vers une autre vue ou une autre action
            return RedirectToAction("Resultats");
        }

        [HttpPost]
        public ActionResult Action(string selectedItem)
        {
            // Effectuez le traitement nécessaire avec le selectedItem
            // et retournez la vue appropriée avec les résultats
            return View("Result", selectedItem);
        }


    }
}