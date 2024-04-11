using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PROJET.Models
{
    public class Histo_Hparam
    {
        [Key]
        public int IdHisto_HParam { get; set; }

        [ForeignKey("Sauvegarde")]
        public int IdSauvegarde { get; set; }

        [ForeignKey("Hyperparamètres")]
        public int IdHParam { get; set; }

        [Required]
        [StringLength(255)]
        public string SelectedValue { get; set; }

        public virtual Sauvegarde Sauvegarde { get; set; }

        public virtual Hyperparamètres Hyperparamètres { get; set; }
    }
}
