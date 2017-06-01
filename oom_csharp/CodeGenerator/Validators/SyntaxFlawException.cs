using System;

namespace CodeGenerator.Validators
{
    public class SyntaxFlawException : Exception
    {
        public SyntaxFlawException()
        {
        }

        public SyntaxFlawException(string message) : base(message)
        {
        }

        public SyntaxFlawException(string message, Exception innerException) : base(message, innerException)
        {
        }
    }
}