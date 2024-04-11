using PROJET.Models;
using System.ComponentModel.DataAnnotations;


namespace PROJET.Models
{
    public class Methode
    {
        public int Id { get; set; }
        [Required]
        
        public string? Nom { get; set; }

        public int? NbrHParam { get; set; }

        public ICollection <Hyperparamètres>? Hyperparams { get; set;}
        public ICollection<Sauvegarde>? Sauvegardes { get; set; }

    }

}



