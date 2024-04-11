using System.ComponentModel.DataAnnotations;
//using static IronPython.Modules._ast;



namespace PROJET.Models
{
    public class Hyperparamètres
    {
    [Key]
    public int IdHParam { get; set; }
    [Required]

    public string? NomHParam { get; set; }
    public string? Type { get; set; }
    public string? DefaultValue { get; set; }
    public ICollection<Histo_Hparam>? histoHparam { get; set; }

    }
}


