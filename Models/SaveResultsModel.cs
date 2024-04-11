namespace PROJET.Models
{
    public class SaveResultsModel
    {
        public int IdSauvegarde { get; set; }
        public float Accuracy { get; set; }
        public DateTime Heure { get; set; }
        public int MethodeId { get; set; }
        public List<SRHParam> ListHParam { get; set; }
    }

    public class SRHParam
    {
        public int Id { get; set; }
        public string Value { get; set; }
    }
}
