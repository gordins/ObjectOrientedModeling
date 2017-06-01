using System.Collections.Generic;
using Model.SchemaModel;

namespace CodeGenerator.Generators
{
    public interface IGenerator
    {
        Dictionary<string, string> GenerateProcessedText(ProcessedText processedText);
        string GenerateEntity(Entity entity);
        string GenerateVariable(Variable variable);
        string GenerateMethod(Method method, bool isEntityInterface);
        string GenerateParameter(Parameter parameter);
        string GenerateConstructor(Constructor constructor, string entityName);
        string GenerateEnumValue(EnumerationElement enumValue);
    }
}