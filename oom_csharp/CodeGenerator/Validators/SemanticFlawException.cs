using System;

namespace CodeGenerator.Validators
{
    public class SemanticFlawException : Exception
    {
        public SemanticFlawException()
        {
        }

        public SemanticFlawException(string message) : base(message)
        {
        }

        public SemanticFlawException(string message, Exception innerException) : base(message, innerException)
        {
        }
    }
}