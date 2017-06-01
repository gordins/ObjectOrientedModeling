using System.Collections.Generic;
using System.Linq;
using Model.SchemaModel;

namespace CodeGenerator.Generators
{
    public abstract class AbstractGenerator : IGenerator
    {
        public Dictionary<string, string> GenerateProcessedText(ProcessedText processedText)
        {
            return processedText.Entities.ToDictionary(entity => entity.Name, GenerateEntity);
        }

        public abstract string GenerateEntity(Entity entity);

        public abstract string GenerateVariable(Variable variable);

        public abstract string GenerateMethod(Method method, bool isEntityInterface);

        public abstract string GenerateParameter(Parameter parameter);

        public abstract string GenerateConstructor(Constructor constructor, string entityName);

        public string GenerateEnumValue(EnumerationElement enumValue)
        {
            return enumValue.Value;
        }
    }
}