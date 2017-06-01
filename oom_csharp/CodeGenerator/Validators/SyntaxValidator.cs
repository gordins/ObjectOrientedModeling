using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using Model.SchemaModel;

namespace CodeGenerator.Validators
{
    public class SyntaxValidator : IValidator
    {
        private StringBuilder _errors;

        public void Validate(ProcessedText processedText)
        {
            foreach (var entity in processedText.Entities)
            {
                if (!IsValidItem(entity))
                    throw new SyntaxFlawException(_errors.ToString() + entity);
                if (entity.Variables.Any(variable => !IsValidItem(variable)))
                    throw new SyntaxFlawException(_errors.ToString());
                if (entity.Enumeration.Any(enumeration => !IsValidItem(enumeration)))
                    throw new SyntaxFlawException(_errors.ToString());
                foreach (var method in entity.Methods)
                {
                    if (!IsValidItem(method))
                        throw new SyntaxFlawException(_errors.ToString());
                    if (method.Parameters.Any(parameter => !IsValidItem(parameter)))
                        throw new SyntaxFlawException(_errors.ToString());
                }
                foreach (var constructor in entity.Constructors)
                {
                    if (!IsValidItem(constructor))
                        throw new SyntaxFlawException(_errors.ToString());
                    if (constructor.Parameters.Any(parameter => !IsValidItem(parameter)))
                        throw new SyntaxFlawException(_errors.ToString());
                }
            }
        }

        private bool IsValidItem(object item)
        {
            var context = new ValidationContext(item, null, null);
            var results = new List<ValidationResult>();
            if (Validator.TryValidateObject(item, context, results, true))
                return true;
            _errors = new StringBuilder();
            foreach (var validationResult in results)
                _errors.Append(validationResult.ErrorMessage).Append("\n");
            return false;
        }
    }
}