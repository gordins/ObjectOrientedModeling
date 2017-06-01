using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace Model.SchemaModel
{
    public class Constructor
    {
        [RegularExpression("^public$|^protected$|^private$|^$", ErrorMessage = "Invalid access modifier.")]
        [DefaultValue("")]
        public string AccessModifier { get; set; } = "";

        public List<Parameter> Parameters { get; set; } = new List<Parameter>();
    }
}