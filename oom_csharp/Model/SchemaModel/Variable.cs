using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace Model.SchemaModel
{
    public class Variable
    {
        [NotKeyword]
        [Required]
        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid variable name.")]
        public string Name { get; set; }

        [Required]
        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid variable type.")]
        public string Type { get; set; }

        [DefaultValue(false)]
        public bool IsCollection { get; set; } = false;

        [RegularExpression("^public$|^protected$|^private$|^$", ErrorMessage = "Invalid access modifier")]
        [DefaultValue("")]
        public string AccessModifier { get; set; } = "";

        [DefaultValue(false)]
        public bool IsConst { get; set; } = false;

        [DefaultValue(false)]
        public bool IsStatic { get; set; } = false;
    }
}