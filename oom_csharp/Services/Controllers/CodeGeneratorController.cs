using CodeGenerator.Generators;
using CodeGenerator.Validators;
using Microsoft.AspNetCore.Mvc;
using Model.SchemaModel;

namespace Services.Controllers
{
    [Route("codeGenerator")]
    public class CodeGeneratorController : Controller
    {
        [HttpPost("{language}")]
        public IActionResult GenerateCode(string language, [FromBody] ProcessedText processedText)
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
                case "json":
                    return Ok(processedText);
                default:
                    return NotFound();
            }

            if (processedText?.Entities == null)
                return BadRequest();
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            IValidator validator = new SyntaxValidator();
            try
            {
                validator.Validate(processedText);
            }
            catch (SyntaxFlawException e)
            {
                return BadRequest(e.ToString());
            }
            validator = new SemanticValidator();
            try
            {
                validator.Validate(processedText);
            }
            catch (SemanticFlawException e)
            {
                return BadRequest(e.ToString());
            }

            return Ok(generator.GenerateProcessedText(processedText));
        }
    }
}