using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace Model.SchemaModel
{
    public class Method
    {
        [NotKeyword]
        [Required]
        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid method name.")]
        public string Name { get; set; }

        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid return type for a method.")]
        [DefaultValue("void")]
        public string ReturnType { get; set; } = "void";

        [RegularExpression("^public$|^protected$|^private$|^$", ErrorMessage = "Invalid access modifier.")]
        [DefaultValue("")]
        public string AccessModifier { get; set; } = "";

        [DefaultValue(false)]
        public bool IsReturnCollection { get; set; } = false;

        [DefaultValue(false)]
        public bool IsSealed { get; set; } = false;

        [DefaultValue(false)]
        public bool IsStatic { get; set; } = false;

        [DefaultValue(false)]
        public bool IsAbstract { get; set; } = false;

        public List<Parameter> Parameters { get; set; } = new List<Parameter>();
    }
}