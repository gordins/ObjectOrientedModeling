﻿using System.Text;
using Model.SchemaModel;

namespace CodeGenerator.Generators
{
    public class CsGenerator : AbstractGenerator
    {
        public override string GenerateEntity(Entity entity)
        {
            var generatedEntity = new StringBuilder();

            generatedEntity.Append("using System;\nnamespace GeneratedCode\n{\n\t");

            if (!entity.AccessModifier.Equals(""))
                generatedEntity.Append(entity.AccessModifier).Append(' ');
            if (entity.IsSealed)
                generatedEntity.Append("sealed ");
            if (entity.IsAbstract)
                generatedEntity.Append("abstract ");
            generatedEntity.Append(entity.Type).Append(' ').Append(entity.Name);
            if (!entity.Inherits.Equals(""))
                generatedEntity.Append(" : ").Append(entity.Inherits);
            generatedEntity.Append("\n\t{");

            //Variables
            foreach (var variable in entity.Variables)
                generatedEntity.Append("\n\t\t").Append(GenerateVariable(variable)).Append(";");
            //Constructors
            foreach (var constructor in entity.Constructors)
                generatedEntity.Append("\n\t\t")
                    .Append(GenerateConstructor(constructor, entity.Name))
                    .Append("\n\t\t{\n\t\t}");
            //Methods
            var isEntityInterface = entity.Type == "interface";
            foreach (var method in entity.Methods)
                generatedEntity.Append("\n\t\t").Append(GenerateMethod(method, isEntityInterface));
            //Enum values
            foreach (var enumerationElement in entity.Enumeration)
                generatedEntity.Append("\n\t\t").Append(GenerateEnumValue(enumerationElement)).Append(",");
            if (entity.Enumeration.Count > 0)
                generatedEntity.Length -= 1;


            generatedEntity.Append("\n\t}\n}\n");
            return generatedEntity.ToString();
        }

        public override string GenerateVariable(Variable variable)
        {
            var generatedVariable = new StringBuilder();
            if (!variable.AccessModifier.Equals(""))
                generatedVariable.Append(variable.AccessModifier).Append(' ');
            if (variable.IsConst)
                generatedVariable.Append("const ");
            if (variable.IsStatic)
                generatedVariable.Append("static ");
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
                generatedMethod.Append("sealed").Append(' ');
            if (method.IsAbstract)
                generatedMethod.Append("abstract").Append(' ');
            if (method.IsStatic)
                generatedMethod.Append("static").Append(' ');
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
                generatedMethod.Append("\n\t\t{\n\t\t\tthrow new NotImplementedException();\n\t\t}");

            return generatedMethod.ToString();
        }

        public override string GenerateParameter(Parameter parameter)
        {
            var generatedParameter = new StringBuilder();
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
    }
}