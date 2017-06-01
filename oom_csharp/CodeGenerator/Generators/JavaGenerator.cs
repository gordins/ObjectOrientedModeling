using System.Text;
using Model.SchemaModel;

namespace CodeGenerator.Generators
{
    public class JavaGenerator : AbstractGenerator
    {
        public override string GenerateEntity(Entity entity)
        {
            var generatedEntity = new StringBuilder();
            if (!entity.AccessModifier.Equals(""))
                generatedEntity.Append(entity.AccessModifier).Append(' ');
            if (entity.IsSealed)
                generatedEntity.Append("final ");
            if (entity.IsAbstract)
                generatedEntity.Append("abstract ");
            generatedEntity.Append(entity.Type).Append(' ').Append(entity.Name);
            if (!entity.Inherits.Equals(""))
                generatedEntity.Append(" extends ").Append(entity.Inherits);
            generatedEntity.Append(" {");

            //Variables
            foreach (var variable in entity.Variables)
                generatedEntity.Append("\n\t").Append(GenerateVariable(variable)).Append(";");
            //Constructors
            foreach (var constructor in entity.Constructors)
                generatedEntity.Append("\n\t")
                    .Append(GenerateConstructor(constructor, entity.Name))
                    .Append(" {\n\t}");
            //Methods
            var isEntityInterface = entity.Type == "interface";
            foreach (var method in entity.Methods)
                generatedEntity.Append("\n\t").Append(GenerateMethod(method, isEntityInterface));
            //Enum values
            foreach (var enumerationElement in entity.Enumeration)
                generatedEntity.Append("\n\t").Append(GenerateEnumValue(enumerationElement)).Append(",");
            if (entity.Enumeration.Count > 0)
                generatedEntity.Length -= 1;

            generatedEntity.Append("\n}");
            return generatedEntity.ToString();
        }

        public override string GenerateVariable(Variable variable)
        {
            var generatedVariable = new StringBuilder();
            if (!variable.AccessModifier.Equals(""))
                generatedVariable.Append(variable.AccessModifier).Append(' ');
            if (variable.IsConst)
                generatedVariable.Append("final ");
            if (variable.IsStatic)
                generatedVariable.Append("static ");
            variable.Type = CheckForAlternateTypes(variable.Type);
            generatedVariable.Append(variable.Type);
            generatedVariable.Append(variable.IsCollection ? "[] " : " ");
            generatedVariable.Append(variable.Name);
            return generatedVariable.ToString();
        }

        public override string GenerateMethod(Method method, bool isEntityInterface)
        {
            var generatedMethod = new StringBuilder();
            if (!method.AccessModifier.Equals(""))
                generatedMethod.Append(method.AccessModifier).Append(' ');
            if (method.IsSealed)
                generatedMethod.Append("final").Append(' ');
            if (method.IsAbstract)
                generatedMethod.Append("abstract").Append(' ');
            if (method.IsStatic)
                generatedMethod.Append("static").Append(' ');
            method.ReturnType = CheckForAlternateTypes(method.ReturnType);
            generatedMethod.Append(method.ReturnType);
            generatedMethod.Append(method.IsReturnCollection ? "[] " : " ");
            generatedMethod.Append(method.Name);

            generatedMethod.Append('(');
            //parameters
            foreach (var parameter in method.Parameters)
                generatedMethod.Append(GenerateParameter(parameter)).Append(", ");
            if (method.Parameters.Count > 0)
                generatedMethod.Length -= 2;
            generatedMethod.Append(')');

            if (method.IsAbstract || isEntityInterface)
                generatedMethod.Append(';');
            else
                generatedMethod.Append(" {\n\t\tthrow new NotImplementedException();\n\t}");

            return generatedMethod.ToString();
        }

        public override string GenerateParameter(Parameter parameter)
        {
            var generatedParameter = new StringBuilder();
            parameter.Type = CheckForAlternateTypes(parameter.Type);
            generatedParameter.Append(parameter.Type)
                .Append(parameter.IsCollection ? "[] " : " ")
                .Append(parameter.Name);

            return generatedParameter.ToString();
        }

        public override string GenerateConstructor(Constructor constructor, string entityName)
        {
            var generatedConstructor = new StringBuilder();
            if (!constructor.AccessModifier.Equals(""))
                generatedConstructor.Append(constructor.AccessModifier).Append(' ');

            generatedConstructor.Append(entityName);

            generatedConstructor.Append('(');
            //parameters
            foreach (var parameter in constructor.Parameters)
                generatedConstructor.Append(GenerateParameter(parameter)).Append(", ");
            if (constructor.Parameters.Count > 0)
                generatedConstructor.Length -= 2;
            generatedConstructor.Append(')');
            return generatedConstructor.ToString();
        }

        private static string CheckForAlternateTypes(string type)
        {
            switch (type)
            {
                case "string":
                    return "String";
                case "bool":
                    return "boolean";
                case "object":
                    return "Object";
                default:
                    return type;
            }
        }
    }
}