namespace CodeGenerator.Generators
{
    public class GeneratorFactory
    {
        public static IGenerator CreateGenerator(string language)
        {
            IGenerator generator;
            switch (language)
            {
                case "java":
                    generator = new JavaGenerator();
                    break;
                case "csharp":
                    generator = new CsGenerator();
                    break;
                default:
                    throw new LanguageNotSupportedException();
            }
            return generator;
        }
    }
}