using System.ComponentModel.DataAnnotations;

namespace Model.SchemaModel
{
    public class EnumerationElement
    {
        [NotKeyword]
        [Required]
        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid enum value name.")]
        public string Value { get; set; }
    }
}