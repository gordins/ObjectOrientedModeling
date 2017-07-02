using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Model.SchemaModel;

namespace CodeGenerator.Validators
{
    public class SemanticValidator : IValidator
    {
        private readonly HashSet<string> _createdTypes = new HashSet<string>();

        private readonly HashSet<string> _predefinedTypes = new HashSet<string>
        {
            "bool",
            "byte",
            "char",
            "double",
            "float",
            "int",
            "long",
            "object",
            "short",
            "string"
        };

        public void Validate(ProcessedText processedText)
        {
            foreach (var entity in processedText.Entities)
            {
                if (_createdTypes.Contains(entity.Name))
                    throw new SemanticFlawException("The name " + entity.Name + " is used more than once.");
                _createdTypes.Add(entity.Name);
            }

            foreach (var entity in processedText.Entities)
            {
                if (entity.Inherits.Length > 0)
                {
                    if (entity.Inherits.Equals(entity.Name))
                        throw new SemanticFlawException("An entity can not inherit from itself. (" + entity.Name + ")");
                    if (!_createdTypes.Contains(entity.Inherits))
                        throw new SemanticFlawException(entity.Inherits + " is not a defined entity.");
                    var inheritedEntity = processedText.RetriveByName(entity.Inherits);
                    foreach (var inheritedMethod in inheritedEntity.Methods)
                    {
                        if (!inheritedMethod.IsAbstract || inheritedMethod.AccessModifier == "private") continue;
                        var method = new Method
                        {
                            Name = inheritedMethod.Name,
                            AccessModifier = inheritedMethod.AccessModifier,
                            IsAbstract = false,
                            IsReturnCollection = inheritedMethod.IsReturnCollection,
                            IsSealed = false,
                            IsStatic = false,
                            ReturnType = inheritedMethod.ReturnType,
                            Parameters = inheritedMethod.Parameters.Select(parameter => new Parameter
                            {
                                Name = parameter.Name,
                                IsCollection = parameter.IsCollection,
                                Type = parameter.Type
                            }).ToList()
                        };
                        entity.Methods.Add(method);
                    }
                }

                var variables = new List<string>();
                foreach (var variable in entity.Variables)
                {
                    if (!IsValidType(variable.Type))
                        throw new SemanticFlawException(variable.Type + " is not a valid type.");
                    variables.Add(variable.Name);
                }
                if (variables.Count != variables.Distinct().Count())
                    throw new SemanticFlawException(
                        "It is not possible to have two properties with the same name in the same entity.");

                var methods = new List<string>();
                foreach (var method in entity.Methods)
                {
                    if (!IsValidType(method.ReturnType) && method.ReturnType != "void")
                        throw new SemanticFlawException(method.ReturnType + " is not a valid type.");
                    if (method.Name == entity.Name)
                        throw new SemanticFlawException("An entity can not have a method name the same as it is. (" +
                                                        entity.Name + ")");
                    var currentMethod = new StringBuilder();
                    currentMethod.Append(method.Name);

                    var parameters = new List<string>();
                    foreach (var parameter in method.Parameters)
                    {
                        if (!IsValidType(parameter.Type))
                            throw new SemanticFlawException(parameter.Type + " is not a valid type.");
                        parameters.Add(parameter.Name);
                        currentMethod.Append(parameter.Type);
                    }
                    if (parameters.Count != parameters.Distinct().Count())
                        throw new SemanticFlawException(
                            "It is not possible to have parameters with the same in the same method.");
                    methods.Add(currentMethod.ToString());
                }
                if (methods.Count != methods.Distinct().Count())
                    throw new SemanticFlawException(
                        "It is not possible to have two methods with the same name and the same signature in the same entity.");


                foreach (var constructor in entity.Constructors)
                {
                    var parameters = new List<string>();
                    foreach (var parameter in constructor.Parameters)
                    {
                        if (!IsValidType(parameter.Type))
                            throw new SemanticFlawException(parameter.Type + " is not a valid type.");
                        parameters.Add(parameter.Name);
                    }
                    if (parameters.Count != parameters.Distinct().Count())
                        throw new SemanticFlawException(
                            "It is not possible to have parameters with the same in the same constructor.");
                }
            }
        }

        private bool IsValidType(string type)
        {
            return
                _createdTypes.Contains(type) || _predefinedTypes.Contains(type);
        }
    }
}