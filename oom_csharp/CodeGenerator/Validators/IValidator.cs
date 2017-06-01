using Model.SchemaModel;

namespace CodeGenerator.Validators
{
    public interface IValidator
    {
        void Validate(ProcessedText processedText);
    }
}