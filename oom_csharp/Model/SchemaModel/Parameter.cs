using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace Model.SchemaModel
{
    public class Parameter
    {
        [NotKeyword]
        [Required]
        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid parameter name.")]
        public string Name { get; set; }

        [Required]
        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid parameter type.")]
        public string Type { get; set; }

        [DefaultValue(false)]
        public bool IsCollection { get; set; } = false;
    }
}