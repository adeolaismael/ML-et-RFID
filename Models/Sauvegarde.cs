using NuGet.Packaging.Signing;
using PROJET.Models;
using System.ComponentModel.DataAnnotations;
using static IronPython.Modules._ast;

namespace PROJET.Models
{
    public class Sauvegarde
    {
        [Key]
        public int IdSauvegarde { get; set; }
        [Required]
        public float Accuracy { get; set; }
      
        public DateTime Heure { get; set; }
        
        public  int methodeId { get; set; }

        public ICollection<Histo_Hparam>? histoHparam { get; set; }

       
    }
}
