using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Linq;

namespace Model.SchemaModel
{
    public class Entity
    {
        [NotKeyword]
        [Required]
        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid entity name.")]
        public string Name { get; set; }

        [RegularExpression("^class$|^interface$|^enum$", ErrorMessage = "Invalid entity type.")]
        [DefaultValue("class")]
        public string Type { get; set; } = "class";

        [RegularExpression("^public$|^protected$|^private$|^$", ErrorMessage = "Invalid access modifier.")]
        [DefaultValue("")]
        public string AccessModifier { get; set; } = "";

        [DefaultValue(false)]
        public bool IsSealed { get; set; } = false;

        [DefaultValue(false)]
        public bool IsAbstract { get; set; } = false;

        [NotKeyword]
        [RegularExpression("[_a-zA-Z][_a-zA-Z0-9]*", ErrorMessage = "Invalid inherits name.")]
        [DefaultValue("")]
        public string Inherits { get; set; } = "";

        public List<Variable> Variables { get; set; } = new List<Variable>();
        public List<Method> Methods { get; set; } = new List<Method>();
        public List<Constructor> Constructors { get; set; } = new List<Constructor>();
        public List<EnumerationElement> Enumeration { get; set; } = new List<EnumerationElement>();

        public Variable RetriveVariableByName(string name)
        {
            var variableToRetrive = Variables.SingleOrDefault(variable => variable.Name == name);
            if (variableToRetrive != null)
                return variableToRetrive;
            var newVariable = new Variable {Name = name};
            Variables.Add(newVariable);
            return newVariable;
        }

        public Method RetriveMethodByName(string name)
        {
            var methodToRetrive = Methods.SingleOrDefault(method => method.Name == name);
            if (methodToRetrive != null)
                return methodToRetrive;
            var newMethod = new Method {Name = name};
            Methods.Add(newMethod);
            return newMethod;
        }
    }
}